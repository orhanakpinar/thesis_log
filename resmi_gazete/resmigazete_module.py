import csv
import os
import time
import re
import unicodedata
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin
from datetime import datetime


class ResmiGazeteScraper:
    def __init__(self, year: int, base_url: str = "https://www.resmigazete.gov.tr/eskiler"):
        self.year = int(year)
        self.base_url = base_url.rstrip("/")
        self.site_root = "https://www.resmigazete.gov.tr/"  # for resolving "local" hrefs robustly

        self.months = [f"{m:02d}" for m in range(1, 13)]
        self.days = [f"{d:02d}" for d in range(1, 32)]
        self.rows = []

        # Skip any word that starts with "ilan" (ilan, ilanlar, ilanları, ilanın, ilana, ...)
        self.ilan_re = re.compile(r"\bilan\w*", flags=re.IGNORECASE)

        # cleanup map for common "weird" characters / cp1252 artifacts
        self.bad_char_map = {
            "\x96": "-",   # en dash
            "\x97": "-",   # em dash
            "\x91": "'", "\x92": "'",  # curly single quotes
            "\x93": '"', "\x94": '"',  # curly double quotes
            "\xa0": " ",   # nbsp
        }

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; ResmiGazeteScraper/1.0)"
        })
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def _valid_date(self, month: str, day: str) -> bool:
        try:
            datetime(self.year, int(month), int(day))
            return True
        except ValueError:
            return False

    def _page_url(self, month: str, day: str) -> str:
        return f"{self.base_url}/{self.year}/{month}/{self.year}{month}{day}.htm"

    def _pick_container(self, soup: BeautifulSoup):
        for css in ["#html-content", "#AutoNumber1", "body"]:
            node = soup.select_one(css)
            if node is not None:
                return css, node
        return "document", soup

    # Turkish-safe normalize (does NOT remove Turkish letters)
    def _normalize_text_tr(self, text: str) -> str:
        if not text:
            return ""

        t = text.replace("\r", " ").replace("\n", " ")

        for bad, good in self.bad_char_map.items():
            t = t.replace(bad, good)

        # Normalize unicode (keeps Turkish chars like ğ, ş, ı, İ)
        t = unicodedata.normalize("NFKC", t)

        # Remove control characters (but keep letters)
        t = "".join(ch for ch in t if unicodedata.category(ch) not in ("Cc", "Cf"))

        # Collapse whitespace
        t = " ".join(t.split()).strip()
        return t

    def _should_skip_text(self, text: str) -> bool:
        # Omit texts containing Æ or Å (stray nav-arrow glyphs, not real titles)
        if "Æ" in text or "Å" in text:
            return True

        # Omit ilan / ilanlar / ilanları / ilan... (any case)
        if self.ilan_re.search(text):
            return True

        return False

    # resolve hrefs that are local/relative to a proper absolute URL
    def _resolve_href(self, page_url: str, href: str) -> str:
        href = (href or "").strip()
        if not href:
            return ""

        if href.startswith("/"):
            return urljoin(self.site_root, href)

        if href.startswith("http://") or href.startswith("https://"):
            return href

        return urljoin(page_url, href)

    def _parse_links(self, html: str, page_url: str, debug: bool = False):
        soup = BeautifulSoup(html, "html.parser")
        css_used, container = self._pick_container(soup)

        anchors = container.select("a[href]") if hasattr(container, "select") else soup.select("a[href]")

        if debug:
            print(f"  container used: {css_used}, links found: {len(anchors)}")

        out = []
        for a in anchors:
            href_raw = a.get("href") or ""
            resolved = self._resolve_href(page_url, href_raw)
            if not resolved:
                continue

            text_raw = a.get_text(" ", strip=True)
            text = self._normalize_text_tr(text_raw)

            if len(text) < 3:
                continue

            if self._should_skip_text(text):
                continue

            out.append((text, resolved))

        # The site wraps long titles across multiple <a> tags that share the SAME
        # href (one tag per visual line) instead of one anchor with the full text -
        # confirmed by fetching resmigazete.gov.tr/eskiler/2006/01/20060103.htm
        # directly, where the title for 20060103-1.htm is split across two adjacent
        # <a href="20060103-1.htm"> tags. Left unmerged, each fragment becomes its
        # own incomplete row. Merge only ADJACENT same-href entries (not all
        # same-href entries anywhere on the page) so unrelated "see also" links
        # pointing at the same page aren't wrongly concatenated.
        merged = []
        for text, href in out:
            if merged and merged[-1][1] == href:
                merged[-1] = (merged[-1][0] + " " + text, href)
            else:
                merged.append((text, href))

        return merged

    def _fetch_day(self, month: str, day: str, debug: bool = False):
        page_url = self._page_url(month, day)

        try:
            r = self.session.get(page_url, timeout=20)
            if not r.encoding:
                r.encoding = "utf-8"
        except requests.RequestException as e:
            print(f"failed to retrive page {page_url} ({type(e).__name__})")
            return None

        if r.status_code != 200:
            print(f"failed to retrive page {page_url}")
            return None

        return self._parse_links(r.text, page_url, debug=debug)

    def scrape(self, debug: bool = True):
        self.rows = []

        for month in self.months:
            for day in self.days:
                if not self._valid_date(month, day):
                    continue

                print(f"accessing page {self._page_url(month, day)}")
                links = self._fetch_day(month, day, debug=debug)
                time.sleep(1)

                if links is None:
                    time.sleep(1)
                    continue

                if debug and len(links) == 0:
                    print("  NOTE: page returned 200 but no <a href> found in selected container (after filtering).")

                date_str = f"{self.year}-{month}-{day}"
                for text, link in links:
                    self.rows.append({"Datetime": date_str, "Text": text, "Hyperlink": link})

    def to_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.rows, columns=["Datetime", "Text", "Hyperlink"])

    def save_to_csv(self, filepath: str):
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Datetime", "Text", "Hyperlink"])
            writer.writeheader()
            writer.writerows(self.rows)
        return filepath


class ResumableResmiGazeteScraper(ResmiGazeteScraper):
    """Wraps the parent's per-date fetch/parse with incremental CSV writes and
    resume-by-skipping-already-scraped-dates, mirroring the pattern already proven in
    agro_ministry_news/agroministry_news_scrape.ipynb's scrape_tarimorman_news_fulltext
    (append-mode CSV, flush after every record, resume by reading existing output)."""

    FIELDNAMES = ["Datetime", "Text", "Hyperlink"]

    def scrape_resumable(self, output_file: str, debug: bool = False):
        done_dates = set()
        file_exists = os.path.isfile(output_file)
        if file_exists:
            with open(output_file, "r", encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    done_dates.add(row["Datetime"])
            print(f"Resuming: {len(done_dates)} dates already in {output_file}, skipping those.")

        with open(output_file, "a", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            if not file_exists:
                writer.writeheader()

            for month in self.months:
                for day in self.days:
                    if not self._valid_date(month, day):
                        continue

                    date_str = f"{self.year}-{month}-{day}"
                    if date_str in done_dates:
                        continue

                    print(f"accessing page {self._page_url(month, day)}")
                    links = self._fetch_day(month, day, debug=debug)
                    time.sleep(1)

                    if links is None:
                        continue

                    for text, link in links:
                        writer.writerow({"Datetime": date_str, "Text": text, "Hyperlink": link})
                    f.flush()


if __name__ == "__main__":
    scraper = ResumableResmiGazeteScraper(year=2006)
    scraper.scrape_resumable(output_file="resmigazete_all/titles_resmigazete_2006.csv")
