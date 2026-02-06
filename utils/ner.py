"""
Named Entity Recognition (NER) using spaCy for contract analysis.
"""
import re
from typing import Dict, List, Tuple
from datetime import datetime


class ContractNER:
    """Named Entity Recognizer for contracts."""
    
    def __init__(self):
        """Initialize the NER engine."""
        self.entities = {
            "parties": [],
            "dates": [],
            "amounts": [],
            "jurisdictions": [],
            "emails": [],
            "phone_numbers": [],
            "urls": []
        }
    
    def extract_entities(self, text: str) -> Dict[str, List]:
        """
        Extract named entities from contract text.
        
        Args:
            text: Contract text
            
        Returns:
            Dictionary of extracted entities
        """
        self.entities["dates"] = self._extract_dates(text)
        self.entities["amounts"] = self._extract_amounts(text)
        self.entities["jurisdictions"] = self._extract_jurisdictions(text)
        self.entities["emails"] = self._extract_emails(text)
        self.entities["phone_numbers"] = self._extract_phone_numbers(text)
        self.entities["urls"] = self._extract_urls(text)
        self.entities["parties"] = self._extract_parties(text)
        
        return self.entities
    
    @staticmethod
    def _extract_dates(text: str) -> List[str]:
        """Extract dates from text."""
        dates = []
        
        # Common date patterns
        patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            r'\b\d{4}-\d{1,2}-\d{1,2}\b',  # YYYY-MM-DD
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            dates.extend([m.group(0) for m in matches])
        
        return list(set(dates))  # Remove duplicates
    
    @staticmethod
    def _extract_amounts(text: str) -> List[Tuple[str, str]]:
        """Extract monetary amounts."""
        amounts = []
        
        # Pattern for currency amounts
        pattern = r'\$[\d,]+(?:\.\d{2})?|\b(?:USD|dollars?|euros?|cents?|pounds?)\s*[\d,]+(?:\.\d{2})?'
        
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            amounts.append((match.group(0), "Currency"))
        
        # Pattern for percentages
        pattern = r'\b\d+(?:\.\d{1,2})?\s*%'
        matches = re.finditer(pattern, text)
        for match in matches:
            amounts.append((match.group(0), "Percentage"))
        
        return amounts
    
    @staticmethod
    def _extract_jurisdictions(text: str) -> List[str]:
        """Extract jurisdictions (states, countries)."""
        jurisdictions = []
        
        # US States
        states = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
            "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
            "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
            "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
            "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
            "New Hampshire", "New Jersey", "New Mexico", "New York",
            "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
            "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
            "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
            "West Virginia", "Wisconsin", "Wyoming"
        ]
        
        for state in states:
            if re.search(rf'\b{state}\b', text, re.IGNORECASE):
                jurisdictions.append(state)
        
        # Country patterns
        countries = ["United States", "United Kingdom", "Canada", "Australia", "India"]
        for country in countries:
            if re.search(rf'\b{country}\b', text, re.IGNORECASE):
                jurisdictions.append(country)
        
        return list(set(jurisdictions))
    
    @staticmethod
    def _extract_emails(text: str) -> List[str]:
        """Extract email addresses."""
        emails = []
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.finditer(pattern, text)
        emails.extend([m.group(0) for m in matches])
        return list(set(emails))
    
    @staticmethod
    def _extract_phone_numbers(text: str) -> List[str]:
        """Extract phone numbers."""
        phones = []
        patterns = [
            r'\b\d{3}-\d{3}-\d{4}\b',  # XXX-XXX-XXXX
            r'\b\(\d{3}\)\s*\d{3}-\d{4}\b',  # (XXX) XXX-XXXX
            r'\b\d{10}\b',  # XXXXXXXXXX
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            phones.extend([m.group(0) for m in matches])
        
        return list(set(phones))
    
    @staticmethod
    def _extract_urls(text: str) -> List[str]:
        """Extract URLs."""
        urls = []
        pattern = r'https?://[^\s]+'
        matches = re.finditer(pattern, text)
        urls.extend([m.group(0) for m in matches])
        return list(set(urls))
    
    @staticmethod
    def _extract_parties(text: str) -> List[str]:
        """Extract party names (companies, individuals)."""
        parties = []
        
        # Look for patterns like "Between X and Y" or "Party: X"
        # Simple heuristic: capitalized names followed by keywords
        pattern = r'(?:between|party|parties|Inc\.|LLC|Corp|Corporation|Company|by\s+and\s+between)\s+([A-Z][A-Za-z\s&,]+?)(?:,|\.|\s+and\s+)'
        
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            party = match.group(1).strip().rstrip(',.')
            if len(party) > 2:
                parties.append(party)
        
        return list(set(parties))
