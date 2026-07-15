"""
Any adapter, regardless of the source format (Markdown, HTML, PDF, etc.),
must produce Document objects composed of Sections. The engine
recognizes only these two classes; it never recognizes the original format.

"""

from dataclasses import dataclass, field

@dataclass
class Section:
    """A section of a document, consisting of a heading and its content."""
    heading: str
    level: int
    content: str
    
    
@dataclass
class Document : 
    """A document composed of multiple sections."""
    source_id: str
    title: str
    sections: list[Section] = field(default_factory=list)  