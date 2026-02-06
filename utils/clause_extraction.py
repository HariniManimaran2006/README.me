"""
Clause and sub-clause extraction using regex patterns.
"""
import re
from typing import List, Dict, Tuple


def extract_clauses(text: str) -> List[Dict]:
    """
    Extract clauses and sub-clauses from contract text.
    
    Args:
        text: Contract text
        
    Returns:
        List of clause dictionaries with heading, number, content
    """
    clauses = []
    
    # Pattern for numbered clauses (e.g., "1.", "2.", etc.)
    clause_pattern = r'^(\d+)\.\s+([A-Z][A-Z\s]*?)(?=^\d+\.|$)'
    
    matches = list(re.finditer(clause_pattern, text, re.MULTILINE))
    
    for i, match in enumerate(matches):
        clause_num = match.group(1)
        clause_title = match.group(2).strip()
        
        # Get content until next clause
        start = match.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)
        
        content = text[start:end].strip()
        
        # Extract sub-clauses
        subclauses = _extract_subclauses(content)
        
        clauses.append({
            "number": clause_num,
            "heading": clause_title,
            "content": content[:500],  # First 500 chars
            "full_content": content,
            "subclauses": subclauses
        })
    
    return clauses


def _extract_subclauses(text: str) -> List[Dict]:
    """Extract sub-clauses (e.g., 1.1, 1.2, etc.)."""
    subclauses = []
    
    # Pattern for decimal-point subclauses
    subclause_pattern = r'^(\d+\.\d+)\s+(.+?)(?=^\d+\.\d+|$)'
    
    matches = list(re.finditer(subclause_pattern, text, re.MULTILINE))
    
    for match in matches:
        num = match.group(1)
        content = match.group(2).strip()[:200]
        
        subclauses.append({
            "number": num,
            "content": content
        })
    
    return subclauses


def split_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    # Simple sentence split on periods followed by space
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def extract_definitions(text: str) -> Dict[str, str]:
    """Extract defined terms (words in quotes)."""
    definitions = {}
    
    # Pattern: "Term" or "Term" means/is/shall...
    pattern = r'"([^"]+)"\s*(?:means|is|shall|refers to)\s*([^.]+\.)' 
    
    matches = re.finditer(pattern, text, re.IGNORECASE)
    
    for match in matches:
        term = match.group(1).strip()
        definition = match.group(2).strip()
        definitions[term] = definition
    
    return definitions
