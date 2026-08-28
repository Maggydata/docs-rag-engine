from langchain_text_splitters import RecursiveCharacterTextSplitter
from .models import Document, Section, Chunk
from dataclasses import dataclass, field

_SPLITTER = RecursiveCharacterTextSplitter(
                chunk_size=800, 
                chunk_overlap=80,
                )


@dataclass
class Segment:
    """A A slice of section content, tagged as code or text."""
    content : str
    kind : str  # "code" or "text"


def chunk_document(document: Document) -> list[Chunk] :
    """Splits a document into smaller chunks based on its sections."""
    
    chunks : list[Chunk] = []
    for section in document.sections :
        for segment in _split_content_into_segments(section.content) :
            
            if segment.kind == "code" :
                #If the segmentis code, we keep as a single Chunk.        
                chunks.append(Chunk(
                                source_id = document.source_id,
                                heading = section.heading,
                                content = segment.content
                            ))
            else :
                #If the segment is text, we split it into smaller chunks.    
                section_chunks = _SPLITTER.split_text(segment.content)
                for chunk_content in section_chunks :
                    chunks.append(Chunk(
                        source_id = document.source_id,
                        heading = section.heading,
                        content = chunk_content
                    ))    
        
    return chunks  


def _split_content_into_segments(content: str) -> list[Segment] : 
    """Splits the content of a section into segments of code and text."""
    
    segments : list[Segment] = []
    
    current_lines:list[str] = []
    current_kind : str = "text"
    
    def _flush_current_lines() -> None : 
        content = "\n".join(current_lines).strip()
        if content :
            segments.append(Segment(content = content, kind = current_kind))
            current_lines.clear()
            
    in_code_block =   False
    for line in content.splitlines() :
        
        if line.strip().startswith("```"):
            
            if not in_code_block :
                _flush_current_lines()
                current_lines.append(line)
                current_kind = "code"
                in_code_block = True
                continue
            
            else:   
                current_lines.append(line)
                _flush_current_lines()
                current_kind = "text"
                in_code_block = False
                continue
            
        current_lines.append(line)
    
    _flush_current_lines()
    return segments   
