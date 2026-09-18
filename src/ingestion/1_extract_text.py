import json
from pathlib import Path

import pdfplumber


# ============================================================
# ECOSYNAPSE - TEXT EXTRACTION
# File: 01_extract_text.py
#
# Purpose:
#   Extract raw per-page text from every PDF under
#   data/knowledge_base/<pillar>/, and save it as JSON so
#   chunking (02_chunk_documents.py) never has to re-run PDF
#   extraction, which is the slowest and most fragile step.
#
# IMPORTANT:
#   This script DOES NOT chunk or tag anything. It only
#   extracts raw text, one JSON file per PDF.
# ============================================================


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"

OUTPUT_DIR = PROJECT_ROOT / "index" / "extracted_text"


# Subfolder name under knowledge_base/ -> default topic hint.
# This is NOT the final topic tag (that happens in 03_tag_chunks.py,
# per chunk, since one PDF can touch more than one pillar) — it's
# just carried along as a hint so tagging starts from a sensible
# default instead of a blank slate.
PILLAR_HINTS = {
    "soil": "soil_health",
    "land_and_ecosystems": "land_use",
    "biodiversity": "biodiversity",
    "climate_and_risks": "climate",
    "pollution": "human_impact",
    "scientific_reports": None,  # mixed pillar — tag per chunk, no default
}


# ============================================================
# 2. FIND ALL PDFS
# ============================================================

def find_all_pdfs(base_dir):
    """
    Walk every subfolder under data/knowledge_base/ and return a
    list of (pdf_path, pillar_folder_name) tuples.
    """

    pdfs = []

    if not base_dir.exists():
        print(f"ERROR: knowledge base directory not found: {base_dir}")
        return pdfs

    for pillar_folder in sorted(base_dir.iterdir()):

        if not pillar_folder.is_dir():
            continue

        for pdf_path in sorted(pillar_folder.glob("*.pdf")):
            pdfs.append((pdf_path, pillar_folder.name))

    return pdfs


# ============================================================
# 3. EXTRACT TEXT FROM ONE PDF
# ============================================================

def extract_pdf_text(pdf_path):
    """
    Extract text page by page from a single PDF.

    Returns a list of dicts: [{"page": int, "text": str}, ...]

    A page with no extractable text (e.g. a scanned image page
    with no OCR layer) gets an empty string, not skipped — so
    page numbers stay aligned with the original document.
    """

    pages = []

    with pdfplumber.open(pdf_path) as pdf:

        for i, page in enumerate(pdf.pages, start=1):

            text = page.extract_text() or ""

            pages.append({
                "page": i,
                "text": text,
                "char_count": len(text),
            })

    return pages


# ============================================================
# 4. SAVE EXTRACTED TEXT
# ============================================================

def save_extracted_text(pdf_path, pillar_folder, pages, output_dir):
    """
    Save extracted pages to a JSON file, mirroring the pillar
    subfolder structure under index/extracted_text/.
    """

    pillar_output_dir = output_dir / pillar_folder
    pillar_output_dir.mkdir(parents=True, exist_ok=True)

    output_path = pillar_output_dir / f"{pdf_path.stem}.json"

    record = {
        "source_pdf": pdf_path.name,
        "pillar_folder": pillar_folder,
        "pillar_hint": PILLAR_HINTS.get(pillar_folder),
        "page_count": len(pages),
        "pages": pages,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    return output_path


# ============================================================
# 5. FLAG LOW-TEXT PAGES
# ============================================================

def flag_low_text_pages(pages, threshold=20):
    """
    Return page numbers with suspiciously little extracted text
    (threshold = character count). Usually means the page is a
    scanned image, a figure/chart with no OCR layer, or a cover
    page — worth a manual look before assuming extraction worked.
    """

    return [
        p["page"] for p in pages
        if p["char_count"] < threshold
    ]


# ============================================================
# 6. PROCESS ONE PDF (WITH ERROR HANDLING)
# ============================================================

def process_pdf(pdf_path, pillar_folder, output_dir):

    print(f"\n{'-' * 80}")
    print(f"PDF: {pdf_path.name}")
    print(f"Pillar folder: {pillar_folder}")
    print(f"{'-' * 80}")

    try:
        pages = extract_pdf_text(pdf_path)

    except Exception as error:
        print("ERROR EXTRACTING TEXT")
        print(error)
        return None

    total_chars = sum(p["char_count"] for p in pages)

    print(f"Pages extracted : {len(pages)}")
    print(f"Total characters: {total_chars:,}")

    low_text_pages = flag_low_text_pages(pages)

    if low_text_pages:
        print(
            f"LOW-TEXT PAGES (< 20 chars, check manually): "
            f"{low_text_pages}"
        )

    output_path = save_extracted_text(
        pdf_path, pillar_folder, pages, output_dir
    )

    print(f"Saved to: {output_path}")

    return output_path


# ============================================================
# 7. MAIN
# ============================================================

def main():

    print("\n")
    print("#" * 80)
    print("              ECOSYNAPSE TEXT EXTRACTION")
    print("#" * 80)

    print(f"\nKnowledge base directory:\n{KNOWLEDGE_BASE_DIR}")
    print(f"\nOutput directory:\n{OUTPUT_DIR}")

    pdfs = find_all_pdfs(KNOWLEDGE_BASE_DIR)

    print(f"\nPDFs found: {len(pdfs)}")

    if not pdfs:
        print("\nNo PDFs found. Check KNOWLEDGE_BASE_DIR path.")
        return

    results = []

    for pdf_path, pillar_folder in pdfs:
        result = process_pdf(pdf_path, pillar_folder, OUTPUT_DIR)
        results.append((pdf_path.name, pillar_folder, result is not None))

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    print("\n\n")
    print("#" * 80)
    print("                 EXTRACTION SUMMARY")
    print("#" * 80)

    succeeded = [r for r in results if r[2]]
    failed = [r for r in results if not r[2]]

    print(f"\nSucceeded: {len(succeeded)} / {len(results)}")

    if failed:
        print(f"\nFAILED ({len(failed)}):")
        for name, pillar, _ in failed:
            print(f"  - {pillar}/{name}")

    print(f"\nNext step: run 02_chunk_documents.py")
    print("\n")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()