import csv
import os
import time
from collections import Counter

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class TarimOrmanScraper:
    """Scrapes tarimorman.gov.tr Haber/{number} press releases into a full-text CSV.

    Incremental writes + resume-by-skipping-already-scraped-Number, mirroring the
    pattern resmi_gazete/resmigazete_module.py's ResumableResmiGazeteScraper cites
    this class as the reference for. Article body is scoped to
    soup.find("div", class_="itemBody") - searching the whole page for <p> tags (as
    the original pilot code did) also pulls in footer contact info and site-wide
    accessibility-menu boilerplate present on every page.
    """

    FIELDNAMES = ["Number", "URL", "Title", "Date", "Paragraphs"]
    BASE_URL = "https://www.tarimorman.gov.tr/Haber/{}"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        })
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _fetch_one(self, number: int):
        url = self.BASE_URL.format(number)
        try:
            response = self.session.get(url, timeout=15)
        except requests.RequestException as e:
            print(f"  {number}: failed after retries: {e}")
            return None

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", class_="itemBody")
        h3_tag = soup.find("h3")
        date_tag = soup.find("span", class_="itemDateCreated")

        title_text = h3_tag.get_text(strip=True) if h3_tag else None
        date_text = date_tag.get_text(strip=True).rstrip("/") if date_tag else None

        p_tags = content_div.find_all("p") if content_div else []
        paragraph_texts = [
            text for p in p_tags
            if (text := p.get_text(" ", strip=True))
        ]
        concatenated_paragraphs = "\n".join(paragraph_texts) if paragraph_texts else None

        return {
            "Number": number,
            "URL": url,
            "Title": title_text,
            "Date": date_text,
            "Paragraphs": concatenated_paragraphs,
        }

    def scrape_resumable(self, start_number: int, end_number: int, output_file: str):
        done_numbers = set()
        file_exists = os.path.isfile(output_file)
        if file_exists:
            with open(output_file, "r", encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    done_numbers.add(int(row["Number"]))
            print(f"Resuming: {len(done_numbers)} articles already in {output_file}, skipping those.")

        with open(output_file, "a", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            if not file_exists:
                writer.writeheader()

            for number in range(start_number, end_number + 1):
                if number in done_numbers:
                    continue

                row = self._fetch_one(number)
                if row is not None:
                    writer.writerow(row)
                    f.flush()

                time.sleep(0.3)

        print(f"Finished. CSV saved as: {output_file}")


class ValidationSampleBuilder:
    """Builds and grows the validation sample used for LLM-assisted classification
    (see agent_note_agroministrynews_FSOI.md, "New workflow" section).

    Does NOT call an LLM itself - Orhan has Claude Code Pro access only, no separate
    Anthropic API key, so classification happens via a Claude Code subagent (the
    `Agent` tool) in an interactive session, not a script-driven call to Anthropic's
    API. This class covers everything around that step: growing the sample with a
    mandatory duplicate check, finding what's unclassified so far, building the
    subagent's prompt text, and folding completed labels back into the sample
    labels file. See build_classification_prompt() for the actual prompt text to
    hand to the Agent tool.

    No batch numbering (Orhan, 2026-09-14 - "seems redundant to say it's arbitrary
    and still apply it, we may delete it" - correct call). An earlier version of
    this class tagged every row with a batch_num and required passing it around to
    know what to classify next; that was never actually necessary. What's
    unclassified is just "Numbers present in the sample but not yet in the sample
    labels file" - get_unclassified() computes that directly, so there's nothing to
    number or remember. The 500 rows classified before this redesign (2026-09-14)
    had a Batch column with values 1-5; it's been stripped from both CSVs since it
    carried no information the agent_note's prose doesn't already have (which rows
    used the older TopicGloss/Notes comment style, etc.) and kept every future row
    locked into a numbering scheme nobody needed.

    sample_csv vs. source_csv (Orhan asked, 2026-09-14): source_csv is the full
    scraped corpus (~7,107 articles, the whole population to draw from); sample_csv
    is the smaller, growing set actually drawn out and classified (500 so far).
    Renamed from "cumulative_csv" 2026-09-14 since "sample" says what it actually is
    now that there's no batch structure left to be "cumulative" across.
    """

    SAMPLE_FIELDNAMES = ["Number", "URL", "Title", "Date", "Paragraphs"]
    LABELS_FIELDNAMES = ["Number", "Categories", "Ceremonial_Political", "Comment", "Orhan_Category"]

    # The literature review's actual 44-category codebook
    # (literature_research/literature_annotation.ipynb, cell 1). Categories are
    # multi-label, not mutually exclusive. Re-verify against that notebook if this
    # list is ever suspected stale - don't trust this copy blindly forever.
    CATEGORY_LIST = [
        "Agro_econ", "Agro_international", "Agro_policy", "Agro_tech", "Agroecology",
        "Autonomy", "Big_agro", "Metropolitan_Law", "Collectives", "Cooperatives", "Debt",
        "Deruralization", "Education", "Food_Network", "Food_Security", "Food_Sovereignty",
        "Gender", "Health", "History", "Interdisciplinary", "Land_Consolidation",
        "Land_Policy", "Land_Use", "Migration", "Monoculture", "Monoculture_Poli",
        "Policy_Access", "Risks_Global", "Rural_Development", "Rural_Family",
        "Rural_Livelihood", "Rural_Policy", "Rurban", "Seed", "Shortfood", "Small_holder",
        "Survivorship_bias", "TR_agroEcon", "TR_agroGov", "TR_landUse", "TR_ruralGov",
        "TR_Peasant", "Urbanization", "Variable",
    ]

    # Recurring content types found across batches that don't map cleanly onto the
    # 44-list - kept here (not just in agent_note) so the prompt and the
    # documentation can't silently drift apart. Add to this list as new gap types
    # get confirmed in a batch's Comment fields; update agent_note in the same edit.
    KNOWN_GAP_TYPES = [
        "water security/infrastructure",
        "forestry/wildfire-disaster management",
        "cross-institution/inter-ministry collaboration or policy councils (Şura/forum/commission format)",
        "food-waste/sustainability content",
        "refugee/migration-driven resource demand",
        "overseas farmland leasing/investment",
        "dam-driven cultural-heritage resettlement",
        "wildlife/biodiversity monitoring with only incidental farmland relevance",
        "routine food-safety/inspection announcements",
    ]

    def __init__(self, source_csv: str, sample_csv: str, sample_labels_csv: str):
        self.source_csv = source_csv
        self.sample_csv = sample_csv
        self.sample_labels_csv = sample_labels_csv

    def _read_sample(self):
        if not os.path.isfile(self.sample_csv):
            return []
        with open(self.sample_csv, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def _read_labels(self):
        if not os.path.isfile(self.sample_labels_csv):
            return []
        with open(self.sample_labels_csv, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def check_duplicates(self):
        """Every call to grow_sample() ends with this, printed, not silently
        trusted. Known legacy duplicates from before the exclusion logic existed:
        Number 320 and 1215 - any OTHER duplicate found here means something is
        wrong and should be investigated before classifying anything new.
        """
        rows = self._read_sample()
        counts = Counter(r["Number"] for r in rows)
        dupes = {n: c for n, c in counts.items() if c > 1}
        print(f"Duplicate check: {len(dupes)} duplicated numbers found: {dupes}")
        return dupes

    def grow_sample(self, n: int, seed: int):
        """Plain random sample of n new articles (Orhan, 2026-09-12: "I don't know
        how you batch it. Just randomly select" - no year-stratification), excluding
        Numbers already in the sample. Appends to sample_csv and runs the duplicate
        check. No batch identity - these rows are just "new additions to the pool",
        nothing more needs to be tracked about them.
        """
        import random
        rng = random.Random(seed)

        existing = self._read_sample()
        existing_numbers = {r["Number"] for r in existing}
        print(f"Existing: {len(existing)} rows, {len(existing_numbers)} distinct numbers")

        with open(self.source_csv, "r", encoding="utf-8-sig", newline="") as f:
            all_rows = list(csv.DictReader(f))

        pool = [
            r for r in all_rows
            if (r.get("Paragraphs") or "").strip() and r["Number"] not in existing_numbers
        ]
        print(f"Eligible pool: {len(pool)}")

        new_rows = rng.sample(pool, n)

        file_exists = os.path.isfile(self.sample_csv)
        with open(self.sample_csv, "a", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.SAMPLE_FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            for r in new_rows:
                writer.writerow({
                    "Number": r["Number"], "URL": r["URL"],
                    "Title": r["Title"], "Date": r["Date"], "Paragraphs": r["Paragraphs"],
                })

        print(f"Appended {n} rows. New sample total: {len(existing) + n} rows")
        self.check_duplicates()

    def get_unclassified(self, out_path: str):
        """Writes every sample row that doesn't yet have a matching row (by Number)
        in the sample labels file to out_path, for a classification subagent to
        read next. This is the replacement for batch-based extraction - "what needs
        classifying" is just a set difference, not something that needs a batch
        number to identify.
        """
        sample_rows = self._read_sample()
        classified_numbers = {r["Number"] for r in self._read_labels()}
        unclassified = [r for r in sample_rows if r["Number"] not in classified_numbers]

        with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.SAMPLE_FIELDNAMES)
            writer.writeheader()
            writer.writerows(unclassified)

        print(f"{len(unclassified)} unclassified rows written to {out_path}")
        return out_path

    def build_classification_prompt(self, n_rows: int, input_csv_path: str, output_csv_path: str) -> str:
        """Returns the prompt text to hand to the Agent tool (subagent_type=
        "general-purpose", model="sonnet" - Orhan's explicit preference, see
        agent_note "no separate Anthropic API access"). This does not call anything
        itself - Claude Code has no API key configured, classification only happens
        through an interactive session's own subagent mechanism.
        """
        categories = ", ".join(self.CATEGORY_LIST)
        gaps = ", ".join(self.KNOWN_GAP_TYPES)
        return f"""You are helping with an MA thesis on Turkey's Food Sovereignty Index. Part of the project scrapes press releases from the Turkish Ministry of Agriculture and Forestry (tarimorman.gov.tr) and classifies what each article is about, using a fixed category codebook from a separate literature-review strand (literature_research/literature_annotation.ipynb). This is a batch of {n_rows} newly-added, not-yet-classified articles from an ongoing pilot — the researcher reviews this output and adds his own additional categories on top of it afterward (an `Orhan_Category` column gets added downstream, not by you), so your job is a careful first-pass classification, not a final answer.

Read this CSV file in full ({n_rows} rows, will need multiple Read calls with offset/limit — read every row, don't stop partway):
{input_csv_path}

Columns: Number, URL, Title, Date, Paragraphs.

For EACH row, read Title and Paragraphs and produce:
1. `Categories`: zero or more labels, semicolon-separated, chosen ONLY from this exact 44-category list (do not invent new names, multi-label is normal, 2-3 tags per article is typical):
{categories}

Guidance on recurring content without an obvious single-category home — multi-tag onto the closest existing categories rather than inventing new ones:
- Irrigation/dam/flood-control infrastructure -> TR_ruralGov, Rural_Development, Agro_policy, or Land_Policy depending on framing
- Wildfire/forestry-disaster response -> Risks_Global, TR_agroGov, or leave uncategorized if nothing fits
- Livestock/animal husbandry/veterinary content -> Agro_econ, TR_agroGov, TR_ruralGov, Rural_Livelihood, Agroecology depending on angle
- Ceremonial/political content: don't assume ceremonial framing means no category applies — a ceremonial village visit can still genuinely touch e.g. Rural_Livelihood; tag what's substantively present even if the framing is ceremonial. Only leave zero categories for content with truly no agricultural/rural substance.
- Most of the 44 are literature-review meta-categories that may rarely apply — don't force usage.
- Food_Sovereignty: apply strictly and rarely — near-universally top-down state framing in this corpus, genuine bottom-up content is very rare.
- Watch specifically for Turkey's 2012 Metropolitan Law (büyükşehir belediyesi/belediyeleri gaining new agricultural/rural responsibilities, "6360", or similar) even as a small buried detail in an otherwise unrelated article — this is the single most important category for this thesis, and real hits have been found buried deep in unrelated-seeming articles. Read every article's full text with this specifically in mind, not just its main topic. Tag Metropolitan_Law if found and quote/describe the relevant passage explicitly in the Comment.

2. `Ceremonial_Political`: "yes"/"no" — primarily ceremonial/photo-op/personal messaging with little substantive policy content? Can co-occur with a real category.
3. `Comment`: a few sentences (not just one) covering what the article is actually about, independent of the category list, plus anything ambiguous, low-confidence, or where a category was a stretch to fit, plus explicitly flag topics that don't fit any of the 44 categories well. Known recurring gap types found in prior batches — name these explicitly when you see them: {gaps}. Also flag any NEW gap type not on this list if you see one.

Write output as a CSV to:
{output_csv_path}

Columns: Number, Categories, Ceremonial_Political, Comment

Be deliberate and consistent. Process all {n_rows} rows, no sampling/skipping. When done, report: rows processed, full category tally, count of Ceremonial_Political=yes, how many rows got zero categories, any Metropolitan_Law hits (quote the relevant passage), and a list of rows flagging any of the known gap types or new ones not seen before."""

    def append_labels(self, labels_csv: str):
        """Folds a completed classification CSV (Number, Categories,
        Ceremonial_Political, Comment) into the sample labels file, adding the
        empty Orhan_Category column.
        """
        with open(labels_csv, "r", encoding="utf-8-sig", newline="") as f:
            new_rows = list(csv.DictReader(f))

        file_exists = os.path.isfile(self.sample_labels_csv)
        with open(self.sample_labels_csv, "a", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.LABELS_FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            for r in new_rows:
                writer.writerow({
                    "Number": r["Number"], "Categories": r["Categories"],
                    "Ceremonial_Political": r["Ceremonial_Political"], "Comment": r["Comment"],
                    "Orhan_Category": "",
                })

        with open(self.sample_labels_csv, "r", encoding="utf-8-sig", newline="") as f:
            total = sum(1 for _ in csv.DictReader(f))
        print(f"Appended {len(new_rows)} rows. New sample labels total: {total} rows")
