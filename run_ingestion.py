from pathlib import Path
from ingestion.batch import ingest_corpus

CORPUS_DIR = Path("data-source/src/oss/langchain")

def main() -> None : 
    report = ingest_corpus(CORPUS_DIR)
    
    total = len(report.documents) + len(report.failures)
    print(f"=== Ingestion Report ===")
    print(f"root folder : {CORPUS_DIR}")
    print(f"total processed files : {total}")
    print(f"successfully ingested : {len(report.documents)}")
    print(f"failed ingestions : {len(report.failures)}")
    print()
    
    print("===successfully ingested documents===")
    for doc in report.documents : 
        total_chars = sum(len(s.content) for s in doc.sections)
        print(f"{doc.source_id:35s} title = {doc.title:35s}"
              f"sections = {len(doc.sections):3d} total chars = {total_chars:6d}")
        
    if report.failures: 
        print()
        print("===failed ingestions===")
        for path, exc in report.failures : 
            print(f"{path.name}")
            print(f"  -> {type(exc).__name__} : {exc}")


if __name__ == "__main__" : 
    main()            