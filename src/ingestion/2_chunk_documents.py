"""
02_chunk_documents.py

Loads page-level extracted JSON files from:
    index/extracted_text/

Splits the text into approximately 300–500 token chunks
with overlap and saves them to:
    index/chunks.jsonl

This script does NOT assign final topic/metric/practice metadata.
That happens in 03_tag_chunks.py.
"""

import json
import re
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

EXTRACTED_TEXT_DIR = PROJECT_ROOT / "index" / "extracted_text"
OUTPUT_PATH = PROJECT_ROOT / "index" / "chunks.jsonl"


# ============================================================
# CHUNKING FUNCTION
# ============================================================

def chunk_page_text(
    text: str,
    target_tokens: int = 400,
    overlap_tokens: int = 50
) -> list[str]:

    """
    Split page text on paragraph breaks and merge paragraphs
    until approximately target_tokens is reached.

    Token count is approximated as:
        words * 1.3
    """

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip()
    ]

    chunks = []

    current = []
    current_len = 0

    for para in paragraphs:

        para_len = int(len(para.split()) * 1.3)

        if current_len + para_len > target_tokens and current:

            chunks.append(" ".join(current))

            # Keep the last paragraph as overlap
            if overlap_tokens > 0:
                current = [current[-1]]
                current_len = int(
                    len(current[0].split()) * 1.3
                )
            else:
                current = []
                current_len = 0

        current.append(para)
        current_len += para_len

    if current:
        chunks.append(" ".join(current))

    return chunks


# ============================================================
# FIND EXTRACTED JSON FILES
# ============================================================

def find_extracted_files():

    files = []

    for pillar_dir in sorted(EXTRACTED_TEXT_DIR.iterdir()):

        if not pillar_dir.is_dir():
            continue

        for json_path in sorted(pillar_dir.glob("*.json")):
            files.append(json_path)

    return files


# ============================================================
# PROCESS ONE DOCUMENT
# ============================================================

def process_document(json_path: Path):

    with open(json_path, "r", encoding="utf-8") as f:
        document = json.load(f)

    source_pdf = document["source_pdf"]
    pillar_folder = document["pillar_folder"]
    pillar_hint = document.get("pillar_hint")

    document_chunks = []

    for page_info in document["pages"]:

        page_number = page_info["page"]
        text = page_info["text"].strip()

        if not text:
            continue

        chunks = chunk_page_text(text)

        for chunk_number, chunk_text in enumerate(chunks, start=1):

            chunk_id = (
                f"{Path(source_pdf).stem}"
                f"_p{page_number}"
                f"_c{chunk_number}"
            )

            document_chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "source_pdf": source_pdf,
                "pillar_folder": pillar_folder,
                "pillar_hint": pillar_hint,
                "page": page_number,
            })

    return document_chunks


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("#" * 80)
    print("              ECOSYNAPSE DOCUMENT CHUNKING")
    print("#" * 80)

    print(f"\nInput directory:")
    print(EXTRACTED_TEXT_DIR)

    print(f"\nOutput:")
    print(OUTPUT_PATH)

    if not EXTRACTED_TEXT_DIR.exists():
        raise FileNotFoundError(
            f"Extracted text directory not found:\n"
            f"{EXTRACTED_TEXT_DIR}\n\n"
            f"Run 01_extract_text.py first."
        )

    json_files = find_extracted_files()

    print(f"\nExtracted documents found: {len(json_files)}")

    if not json_files:
        raise FileNotFoundError(
            "No extracted JSON files found. "
            "Run 01_extract_text.py first."
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    total_chunks = 0

    with open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:

        for json_path in json_files:

            print(f"\nProcessing: {json_path.name}")

            chunks = process_document(json_path)

            print(f"  Chunks created: {len(chunks)}")

            for chunk in chunks:

                output_file.write(
                    json.dumps(
                        chunk,
                        ensure_ascii=False
                    ) + "\n"
                )

            total_chunks += len(chunks)

    print("\n")
    print("#" * 80)
    print("                 CHUNKING SUMMARY")
    print("#" * 80)

    print(f"\nDocuments processed : {len(json_files)}")
    print(f"Total chunks        : {total_chunks:,}")

    print(f"\nSaved to:")
    print(OUTPUT_PATH)

    print("\nNext step: run 03_tag_chunks.py")
    print()


if __name__ == "__main__":
    main()