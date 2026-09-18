import re

def chunk_page_text(text: str, target_tokens: int = 400, overlap_tokens: int = 50) -> list[str]:
    """
    Split on paragraph breaks first, then merge small paragraphs up to
    ~target_tokens, so a quantified claim's sentence stays whole.
    Token count approximated as words * 1.3 (close enough for chunk sizing).
    """
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    chunks = []
    current = []
    current_len = 0

    for para in paragraphs:
        para_len = int(len(para.split()) * 1.3)
        if current_len + para_len > target_tokens and current:
            chunks.append(" ".join(current))
            # carry the last paragraph forward as overlap
            current = [current[-1]] if overlap_tokens > 0 else []
            current_len = int(len(current[0].split()) * 1.3) if current else 0
        current.append(para)
        current_len += para_len

    if current:
        chunks.append(" ".join(current))

    return chunks