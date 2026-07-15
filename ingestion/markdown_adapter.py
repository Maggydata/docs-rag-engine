import re 
from pathlib import Path
import frontmatter

from .models import Document, Section


#Detects JSX component tags
_JSX_TAG_RE = re.compile(r"</?[A-Z][A-Za-z]*(?:\s[^>]*)?>")
def _clean_jsx_tags(text: str) -> str:
    return _JSX_TAG_RE.sub("", text)

# Detects Markdown title lines
_HEADING_RE= re.compile(r'^(#{1,6})\s+(.*)$')

def _split_into_sections(body : str) -> list[Section] : 
    """Split a Markdown text into sections based on the heading lines."""
    sections : list[Section] = []
    
    #Status of currrent Section
    current_heading = "Introduction"            #default name
    current_level = 1
    current_lines : list[str] = []
    
    def _flush_current_section() -> None : 
        """Saves the current section in the list, if it contains any content."""
        content = _clean_jsx_tags("\n".join(current_lines).strip())
        if content :
            sections.append(Section(heading = current_heading, level = current_level, content = content))
    
    
    in_code_block = False
    for line in body.splitlines() : 
        if line.startswith("```"):
            #Toggle the code block status and add the line to the current section's content
            in_code_block = not in_code_block
            current_lines.append(line)
            continue
        
        if not in_code_block:
            match = _HEADING_RE.match(line)
            if match : 
                #Flush the current section before starting a new one
                _flush_current_section()
                current_level = len(match.group(1))
                current_heading = match.group(2).strip()
                current_lines = []
                continue
        
        current_lines.append(line)

    #Flush the last section after processing all lines
    _flush_current_section()
    return sections

def parse_markdown_file(path : Path) -> Document :
    """Reads an .md/.mdx file and generates a generic document."""
    
    raw = path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)
    
    title = post.metadata.get("title", path.stem)
    sections = _split_into_sections(post.content)
    
    return Document(source_id = path.name, title = title, sections = sections)
                