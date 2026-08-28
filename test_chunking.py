from ingestion.batch import ingest_corpus
from ingestion.chunking import chunk_document, _split_content_into_segments
from pathlib import Path

report = ingest_corpus(Path("data-source/src/oss/langchain"))
doc = next(d for d in report.documents if d.source_id == "models.mdx")
chunks = chunk_document(doc)
print(f"{len(chunks)} chunks")
coupes = 0
#for i, c in enumerate(chunks):
for c in chunks:
    #print(c.content)
    # if c.content.count("```") % 2 != 0:
    #     coupes += 1
    #     print(f"--- Chunk {i} [{c.heading}] : bloc de code déséquilibré ---")
    #     print("FIN DU CHUNK :", repr(c.content[-150:]))
    #     print()
    
    
    tailles = [len(c.content) for c in chunks]
    if len(c.content) < 30:
        print(f"\n--- [{c.heading}] ({len(c.content)} chars) ---")
        print(f"min={min(tailles)}, max={max(tailles)}, moyenne={sum(tailles)//len(tailles)}")
        print(f"chunks > 800 : {sum(1 for t in tailles if t > 800)}")
        print(c.content)
#print(f"\n{coupes} chunks avec code coupé sur {len(chunks)}")
