"""
Risk detection engine for contract analysis.
"""
import re
from typing import Dict, List, Tuple


class RiskDetectionEngine:
    """Detects risks in contract clauses."""
    
    # Risk keywords and patterns organized by risk type
    RISK_PATTERNS = {
        "Penalty Clauses": {
            "keywords": ["penalty", "fine", "damages", "liquidated", "breach", "indemnify"],
            "risk_level": "high",
            "description": "Clauses imposing penalties for breach"
        },
        "Indemnity Clauses": {
            "keywords": ["indemnify", "indemnification", "hold harmless", "defending", "liability"],
            "risk_level": "high",
            "description": "Clauses requiring indemnification"
        },
        "Termination Clauses": {
            "keywords": ["termination", "terminate", "terminate for cause", "terminate without cause"],
            "risk_level": "medium",
            "description": "Clauses specifying termination rights"
        },
        "Lock-in Period": {
            "keywords": ["lock", "lock-in", "locked in", "exclusive", "no exit", "cannot terminate"],
            "risk_level": "high",
            "description": "Clauses restricting early termination"
        },
        "Auto-Renewal": {
            "keywords": ["auto-renewal", "automatic renewal", "renew", "unless notice", "renewal"],
            "risk_level": "medium",
            "description": "Clauses with automatic renewal"
        },
        "Arbitration": {
            "keywords": ["arbitration", "arbitrator", "binding arbitration", "arbitrate"],
            "risk_level": "medium",
            "description": "Arbitration dispute resolution clauses"
        },
        "Intellectual Property": {
            "keywords": ["intellectual property", "patent", "copyright", "trademark", "ip", "proprietary", "work made for hire"],
            "risk_level": "high",
            "description": "IP assignment and ownership clauses"
        },
        "Confidentiality": {
            "keywords": ["confidential", "confidentiality", "nda", "non-disclosure", "proprietary"],
            "risk_level": "medium",
            "description": "Confidentiality and NDA clauses"
        },
        "Limitation of Liability": {
            "keywords": ["limitation of liability", "limit of liability", "liable", "not liable", "exclude"],
            "risk_level": "medium",
            "description": "Clauses limiting liability"
        },
        "Non-Competition": {
            "keywords": ["non-compete", "non-competition", "compete", "competitor", "restrictive covenant"],
            "risk_level": "high",
            "description": "Non-compete and restrictive covenant clauses"
        }
    }
    
    def __init__(self):
        """Initialize the risk detection engine."""
        self.detected_risks = []
    
    def detect_risks(self, text: str, clauses: List[Dict] = None) -> List[Dict]:
        """
        Detect risks in contract text and clauses.
        
        Args:
            text: Full contract text
            clauses: List of extracted clauses
            
        Returns:
            List of detected risks with details
        """
        self.detected_risks = []
        
        # Scan full text for risk keywords
        text_lower = text.lower()
        for risk_type, risk_info in self.RISK_PATTERNS.items():
            for keyword in risk_info["keywords"]:
                if keyword in text_lower:
                    # Find sentences containing the keyword
                    sentences = self._find_sentence_with_keyword(text, keyword)
                    for sentence in sentences:
                        risk = {
                            "type": risk_type,
                            "risk_level": risk_info["risk_level"],
                            "description": risk_info["description"],
                            "evidence": sentence[:200],
                            "severity_score": self._assign_severity_score(risk_info["risk_level"])
                        }
                        if risk not in self.detected_risks:
                            self.detected_risks.append(risk)
                    break  # Move to next risk type
        
        return self.detected_risks
    
    @staticmethod
    def _find_sentence_with_keyword(text: str, keyword: str, context_window: int = 150) -> List[str]:
        """Find sentences containing a keyword."""
        sentences = []
        pattern = rf'.{{0,{context_window}}}[^.!?]*?{re.escape(keyword)}[^.!?]*?[.!?]'
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            sentence = match.group(0).strip()
            if sentence:
                sentences.append(sentence[:300])
        
        return sentences[:3]  # Return max 3 sentences
    
    @staticmethod
    def _assign_severity_score(risk_level: str) -> int:
        """Assign severity score (0-100 scale)."""
        scores = {
            "low": 25,
            "medium": 55,
            "high": 85
        }
        return scores.get(risk_level, 50)
    
    def calculate_risk_score(self, detected_risks: List[Dict]) -> Tuple[int, str]:
        """
        Calculate overall contract risk score (0-100).
        
        Args:
            detected_risks: List of detected risks
            
        Returns:
            Tuple of (risk_score, risk_category)
        """
        if not detected_risks:
            return 0, "Low Risk"
        
        # Calculate weighted average
        high_count = sum(1 for r in detected_risks if r["risk_level"] == "high")
        medium_count = sum(1 for r in detected_risks if r["risk_level"] == "medium")
        low_count = sum(1 for r in detected_risks if r["risk_level"] == "low")
        
        # Weighted calculation
        score = (high_count * 30 + medium_count * 15 + low_count * 5) // max(1, len(detected_risks))
        score = min(100, score)
        
        if score >= 70:
            category = "High Risk"
        elif score >= 40:
            category = "Medium Risk"
        else:
            category = "Low Risk"
        
        return score, category
