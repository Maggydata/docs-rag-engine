from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable

from .models import Document
from .markdown_adapter import parse_markdown_file
from .chunking import chunk_document


@dataclass
class IngestReport:
    """Results of a batch ingestion on a folder of source documents."""
    documents : list[Document]
    failures : list[tuple[Path, Exception]]
    
    def summary(self) -> str :
        total = len(self.documents) + len(self.failures)
        lines = [f'{len(self.documents)} OK, {len(self.failures)} failures, out of {total} total.']
        for path, exc in self.failures:
            lines.append(f' - {path.name} : {exc}')
        return '\n'.join(lines)
    
    

def ingest_corpus(corpus_dir: Path, parse_fn: Callable[[Path], Document] = parse_markdown_file,)  -> IngestReport:
    """Ingest all source documents in a folder and return the results."""
    documents : list[Document] = []
    failures : list[tuple[Path, Exception]] = []

    for path in sorted(corpus_dir.rglob("*.mdx")): 
        try:
            doc = parse_fn(path)
            documents.append(doc)
        except Exception as exc:
            failures.append((path, exc))
            
    return IngestReport(documents = documents, failures = failures)  

if __name__ == "__main__":
    report = ingest_corpus(Path("data-source/src/oss/langchain"))
    all_chunks = []
    # for doc in report.documents:
    #     for s in doc.sections:
    #         print(report.summary())
    
    for doc in report.documents:
        all_chunks.extend(chunk_document(doc))
    
    coupes = sum(1 for c in all_chunks if c.content.count("```") % 2 != 0)
    tailles = [len(c.content) for c in all_chunks]
    print(f"{len(all_chunks)} chunks au total")
    print(f"code coupé : {coupes}")
    print(f"min={min(tailles)}, max={max(tailles)}, moyenne={sum(tailles)//len(tailles)}")