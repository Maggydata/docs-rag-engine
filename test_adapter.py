"""Manual inspection script for the Markdown adapter."""

from pathlib import Path
from ingestion.markdown_adapter import parse_markdown_file

TARGET_FILE = Path("data-source/src/oss/langchain/retrieval.mdx")

def main() -> None :
    
    doc = parse_markdown_file(TARGET_FILE)
    print(f"File : {doc.source_id}")
    print(f"Title : {doc.title}")
    print(f"Number of sections : {len(doc.sections)}")
    print()
    print("=== Section's List ===")
    for s in doc.sections:
        preview = s.content.replace("\n", " ")
        print(f"[level {s.level}] {s.heading!r}")
        print(f"  -> {preview}")
    print()    
    
    
if __name__ == "__main__":
    main()