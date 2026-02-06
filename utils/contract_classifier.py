"""
Contract type classification using rule-based patterns.
"""
import re
from typing import Dict, Tuple


class ContractClassifier:
    """Classifies contract types."""
    
    CLASSIFICATION_PATTERNS = {
        "Employment": {
            "keywords": ["employment", "employee", "employer", "salary", "compensation", "work", "position", "job"],
            "min_matches": 3
        },
        "Lease": {
            "keywords": ["lease", "landlord", "tenant", "rent", "property", "premises", "leaseholder"],
            "min_matches": 2
        },
        "Service Agreement": {
            "keywords": ["service", "services", "service provider", "contractor", "engagement", "work"],
            "min_matches": 3
        },
        "Vendor": {
            "keywords": ["vendor", "supplier", "supply", "purchasing", "goods", "material"],
            "min_matches": 2
        },
        "Partnership": {
            "keywords": ["partnership", "partner", "joint venture", "co-founder", "equity", "profit", "loss"],
            "min_matches": 2
        },
        "NDA": {
            "keywords": ["non-disclosure", "nda", "confidential", "confidentiality agreement", "proprietary"],
            "min_matches": 2
        },
        "License Agreement": {
            "keywords": ["license", "licensed", "licensor", "licensee", "intellectual property", "ip"],
            "min_matches": 2
        },
        "Loan Agreement": {
            "keywords": ["loan", "lender", "borrower", "principal", "interest", "repayment", "debt"],
            "min_matches": 3
        }
    }
    
    def classify_contract(self, text: str) -> Dict[str, any]:
        """
        Classify the contract type.
        
        Args:
            text: Contract text
            
        Returns:
            Dictionary with classification results
        """
        text_lower = text.lower()
        
        # Calculate match scores for each type
        scores = {}
        for contract_type, pattern_info in self.CLASSIFICATION_PATTERNS.items():
            matches = 0
            for keyword in pattern_info["keywords"]:
                if keyword in text_lower:
                    matches += 1
            
            if matches >= pattern_info["min_matches"]:
                scores[contract_type] = matches
        
        # Sort by match count
        if scores:
            primary_type = max(scores, key=scores.get)
            confidence = min(100, (scores[primary_type] / 10) * 100)
        else:
            primary_type = "General Contract"
            confidence = 0
        
        return {
            "primary_type": primary_type,
            "confidence": confidence,
            "all_matches": scores,
            "description": self._get_type_description(primary_type)
        }
    
    @staticmethod
    def _get_type_description(contract_type: str) -> str:
        """Get description for contract type."""
        descriptions = {
            "Employment": "Agreement between employer and employee defining terms of work",
            "Lease": "Agreement for renting property or equipment",
            "Service Agreement": "Contract for provision of services",
            "Vendor": "Agreement for supply of goods or services from a vendor",
            "Partnership": "Agreement establishing partnership between parties",
            "NDA": "Non-disclosure agreement protecting confidential information",
            "License Agreement": "Agreement granting rights to use intellectual property",
            "Loan Agreement": "Agreement for borrowing and repayment of funds",
            "General Contract": "Contract of unknown type"
        }
        return descriptions.get(contract_type, "Contract of unknown type")
