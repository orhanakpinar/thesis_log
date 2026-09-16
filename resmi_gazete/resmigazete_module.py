import csv
import os
import time
import re
import unicodedata
import requests
from bs4 import BeautifulSoup, NavigableString
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

        # Skip the "İlanları görmek için tıklayınız" ("click to see announcements")
        # boilerplate link to the day's classified-notices PDF - not a real gazette
        # item. Narrowed from a blanket "\bilan\w*" (skip any word starting with
        # "ilan") after full-year validation diffs against trusted output showed that
        # blanket rule also dropped real titles that just contain "ilan" as a
        # substring - e.g. "Basın-İlan Kurumu" (a real institution name) and "...İlan
        # Edilmiş..."/"...İlanına Dair..." (the verb "to declare/announce" in
        # substantive law titles). Observed variants (case, trailing ".", leading "- ")
        # collected across 2000-2002's trusted files - see
        # agent_note_officialgazete_FSOI.md.
        self.ilan_re = re.compile(
            r"^-?\s*ilanlar[ıi]\s+g[öo]rmek\s+i[çc]in\s+t[ıi]klay[ıi]n[ıi]z\.?$",
            flags=re.IGNORECASE,
        )

        # Skip "Sayfa Başı" ("back to top") in-page nav links - a recurring boilerplate
        # anchor (href like "...htm#T.C.r"), not a real gazette item. Only found in the
        # 2001-2004 fragment-anchor era (one long combined page per day, so "back to
        # top" links appear after every section); 2000/2005/2006 don't have it. Found
        # via full-year validation diffs against trusted output - see
        # agent_note_officialgazete_FSOI.md.
        self.sayfa_basi_re = re.compile(r"^(?:sayfa\s*ba[şs][ıi]\s*)+$", flags=re.IGNORECASE)

        # Skip "Önceki"/"Sonraki" ("Previous"/"Next") in-page nav arrows - found on
        # some 2009/2010 pages with hrefs oddly pointing at 2011 dates (looks like
        # stale/mistemplated site navigation, not a scraper bug) - not real gazette
        # content either way. See agent_note_officialgazete_FSOI.md.
        self.nav_arrow_re = re.compile(r"^(?:önceki|sonraki)$", flags=re.IGNORECASE)

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

        # See _fetch_day: only set True (and only ever once) if this machine actually
        # hits an SSL verification error - not assumed upfront.
        self._ssl_verify_disabled = False

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

        # Omit the "İlanları görmek için tıklayınız" boilerplate link (any case,
        # optional leading "-" / trailing ".")
        if self.ilan_re.search(text):
            return True

        # Omit "Sayfa Başı" back-to-top nav links (repeated one or more times)
        if self.sayfa_basi_re.match(text):
            return True

        # Omit "Önceki"/"Sonraki" prev/next nav arrows
        if self.nav_arrow_re.match(text):
            return True

        return False

    # Older Word-to-HTML export tooling on some pages (mostly 2012-2013) wraps each
    # Turkish diacritic character individually in its own <span>/<font> (apparently to
    # force a font that could render it, e.g. font-family: Times) - one tag per single
    # character, e.g. "T"<span>ü</span>"rk" for "Türk". get_text(" ", strip=True) (used
    # below for everything else) inserted a space at every such boundary regardless,
    # producing "T ü rk" instead of "Türk" - pervasive enough in 2012/2013 (~10% of
    # titles) to be worth a targeted fix, unlike the rarer single-letter kerning-span
    # case (see the comment on the "T oprak" case below, which this does NOT fix -
    # that one is a 3+ char fragment ending in one letter, not an isolated single-char
    # tag, so it doesn't match this rule and is left as documented in
    # agent_note_officialgazete_FSOI.md). Only suppress the separator when at least one
    # side of a tag boundary is, by itself, exactly one character - real multi-word
    # boundaries (e.g. across "Değişiklik Yapılmasına Dair Kanun" boilerplate) still
    # get their space.
    def _get_anchor_text(self, a) -> str:
        pieces = []
        for child in a.contents:
            if isinstance(child, NavigableString):
                pieces.append(str(child))
            else:
                pieces.append(child.get_text())

        if not pieces:
            return ""

        is_single = [len(p.strip()) == 1 for p in pieces]
        result = pieces[0]
        for i in range(1, len(pieces)):
            sep = "" if (is_single[i - 1] or is_single[i]) else " "
            result += sep + pieces[i]
        return result

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

            # href-level check for the "Sayfa Başı" (back-to-top) nav link, in addition
            # to the text-based check below - defense in depth, since it doesn't depend
            # on the visible text matching exactly. Every "Sayfa Başı" anchor observed
            # (2001-2004 fragment-anchor era) points to the same in-page fragment,
            # "#T.C.r" - the masthead/"T.C." header anchor every such link jumps back to,
            # distinct from real item fragments like #1, #2, #3 which are unique per item.
            if resolved.rsplit("#", 1)[-1] == "T.C.r":
                continue

            # Blanket get_text("", strip=True) was tried once and reverted because it
            # fused real word boundaries together across tag splits that don't involve
            # a lone-character span. _get_anchor_text above is the targeted
            # replacement: " " by default, "" only across a tag boundary where one
            # side is a lone character (the per-character font-span pattern, mainly
            # 2012/2013) - see its comment for the full story and
            # agent_note_officialgazette_FSOI.md.
            text_raw = self._get_anchor_text(a)
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
            # Some machines can't validate resmigazete.gov.tr's certificate chain
            # (confirmed on at least one dev machine, 2026-09-12/16: upgrading certifi
            # didn't fix it) - but this is NOT universal, another machine ran the same
            # scrape successfully with no workaround at all. So: try a normal, verified
            # request first, and only fall back to verify=False (with a one-time
            # visible warning) if THIS machine actually needs it - don't assume every
            # environment does. Once we know, skip straight to the fallback instead of
            # re-attempting (and re-failing) the verified request every single call.
            if self._ssl_verify_disabled:
                r = self.session.get(page_url, timeout=20, verify=False)
            else:
                try:
                    r = self.session.get(page_url, timeout=20)
                except requests.exceptions.SSLError:
                    import urllib3
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    print(
                        f"  NOTE: SSL certificate verification failed against "
                        f"{self.base_url} on this machine - falling back to "
                        f"verify=False for the rest of this run."
                    )
                    self._ssl_verify_disabled = True
                    r = self.session.get(page_url, timeout=20, verify=False)
            # These archived pages never declare a charset, so requests falls back to
            # ISO-8859-1 (per RFC default for text/*) even though the real encoding is
            # usually Windows-1254 - the two only disagree on a handful of code points
            # (ı, ş, ğ, İ, Ş, Ğ), so most Turkish text looks fine but those letters
            # silently corrupt. Confirmed via www.resmigazete.gov.tr/eskiler/2006/07/
            # 20060726.htm, whose raw bytes are Windows-1254 (chardet's apparent_encoding
            # agreed) - decoding as ISO-8859-1 turned "Bakanlığına" into "Bakanl\xfd\xf0\xfdna".
            # "if not r.encoding" (the old check here) never fires because requests'
            # ISO-8859-1 fallback is always truthy - it was dead code.
            if "charset" not in (r.headers.get("Content-Type") or "").lower():
                r.encoding = r.apparent_encoding or r.encoding
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
    agro_ministry_news/agroministrynews_scrape.ipynb's scrape_tarimorman_news_fulltext
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
