from dataclasses import dataclass
from pathlib import Path

from .models import Document
from .markdown_adapter import parse_markdown_file


@dataclass
class IngestReport:
    """Results of a batch ingestion on a folder of source documents."""
    documents : list[Document]
    failures : list[tuple[Path, Exception]]
    
    

def ingest_corpus(corpus_dir: Path)  -> IngestReport:
    """Ingest all source documents in a folder and return the results."""
    documents : list[Document] = []
    failures : list[tuple[Path, Exception]] = []
    
    for path in sorted(corpus_dir.rglob("*.mdx")): 
        try:
            doc = parse_markdown_file(path)
            documents.append(doc)
        except Exception as exc:
            failures.append((path, exc))
            
    return IngestReport(documents = documents, failures = failures)            