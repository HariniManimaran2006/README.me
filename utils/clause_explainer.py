"""
LLM-based clause explanation and suggestions.
Provides plain-language explanations and alternative clauses.
"""
from typing import Dict, List


class ClauseExplainer:
    """Generates explanations and suggestions for contract clauses."""
    
    # Pre-defined explanations for common clauses
    CLAUSE_EXPLANATIONS = {
        "Termination": {
            "explanation": "This clause specifies the conditions and procedures for ending the contract.",
            "key_points": [
                "Define notice periods required",
                "Specify termination for-cause vs. without-cause",
                "Detail post-termination obligations",
                "State severance/exit fees if any"
            ],
            "tips": "Ensure notice periods are reasonable and align with business needs."
        },
        "Confidentiality": {
            "explanation": "This clause protects sensitive business information from unauthorized disclosure.",
            "key_points": [
                "Define what qualifies as Confidential Information",
                "Specify duration of confidentiality obligation",
                "List exceptions (public knowledge, independently developed)",
                "Detail remedies for breach"
            ],
            "tips": "Clarify what information is covered and how long protection lasts."
        },
        "Indemnity": {
            "explanation": "One party agrees to cover losses of the other party if certain events occur.",
            "key_points": [
                "Define indemnifiable events clearly",
                "Specify indemnifying party's obligations",
                "Cap indemnification limits if possible",
                "Require prompt notice of claims"
            ],
            "tips": "Negotiate caps on indemnification liability to limit exposure."
        },
        "Non-Competition": {
            "explanation": "Restricts one party from engaging in competing business during and after the contract.",
            "key_points": [
                "Geographic scope of restriction",
                "Time period of non-compete",
                "Specific activities restricted",
                "Exceptions or carve-outs"
            ],
            "tips": "Ensure non-compete is narrowly tailored to protect legitimate interests."
        },
        "Compensation": {
            "explanation": "Details how payment will be made for services or goods provided.",
            "key_points": [
                "Payment amount clearly stated",
                "Payment schedule and frequency",
                "What triggers payment obligations",
                "Adjustment mechanisms if any"
            ],
            "tips": "Specify exact amounts and payment dates to avoid disputes."
        },
        "Intellectual Property": {
            "explanation": "Determines ownership of creations and inventions made during the contract term.",
            "key_points": [
                "Ownership of work product",
                "Pre-existing IP rights preserved",
                "Scope of IP assignment if any",
                "License grants"
            ],
            "tips": "Protect your pre-existing IP and clarify ownership of work created."
        },
        "Limitation of Liability": {
            "explanation": "Caps the amount one party can claim from another in case of breach or damage.",
            "key_points": [
                "Excluded damages (e.g., consequential)",
                "Liability caps or limits",
                "Damages calculation method",
                "Exceptions to limitations"
            ],
            "tips": "Understand which damages are excluded and negotiate reasonable caps."
        },
        "Governing Law": {
            "explanation": "Specifies which jurisdiction's laws will interpret and enforce the contract.",
            "key_points": [
                "Choice of law (which state/country)",
                "Jurisdiction for disputes",
                "Dispute resolution method (litigation vs. arbitration)",
            ],
            "tips": "Choose a neutral jurisdiction if possible."
        }
    }
    
    ALTERNATIVE_CLAUSES = {
        "Termination": [
            "Multi-tier notice: 30 days for without-cause, 10 days for cause with cure period",
            "Immediate termination for material breach with 30-day cure opportunity",
            "Termination for convenience with 60-day notice and proportional fee refund"
        ],
        "Confidentiality": [
            "Information ceases to be confidential if it enters public domain without breach",
            "Carve-outs: Information already known, independently developed, received from third parties",
            "Obligation survives termination for 2-3 years"
        ],
        "Indemnity": [
            "Indemnification capped at annual contract value",
            "Indemnifying party not liable for indirect or consequential damages",
            "Indemnified party must mitigate damages and provide prompt notice"
        ],
        "Intellectual Property": [
            "Pre-existing IP retained by creator; only custom work assigned",
            "License back of IP to creator for personal, non-commercial use",
            "Joint ownership of derivative works"
        ],
        "Compensation": [
            "Fixed fee + hourly rate for out-of-scope work",
            "Payment in installments tied to milestones",
            "Annual adjustment tied to inflation (CPI)"
        ]
    }
    
    def explain_clause(self, clause_type: str) -> Dict[str, any]:
        """
        Get explanation for a specific clause type.
        
        Args:
            clause_type: Type of clause (e.g., "Termination")
            
        Returns:
            Dictionary with explanation details
        """
        if clause_type in self.CLAUSE_EXPLANATIONS:
            return self.CLAUSE_EXPLANATIONS[clause_type]
        else:
            return {
                "explanation": f"No specific guidance available for {clause_type}",
                "key_points": ["Review the clause carefully in context"],
                "tips": "Consider consulting legal counsel for specialized clauses"
            }
    
    def suggest_alternatives(self, clause_type: str) -> List[str]:
        """
        Get alternative language suggestions for a clause.
        
        Args:
            clause_type: Type of clause
            
        Returns:
            List of alternative clause suggestions
        """
        return self.ALTERNATIVE_CLAUSES.get(clause_type, [
            "Consult with legal counsel for alternative language"
        ])
    
    def generate_summary(self, clause_text: str) -> str:
        """
        Generate a plain-language summary of a clause.
        
        Args:
            clause_text: Full clause text
            
        Returns:
            Simplified summary
        """
        # Simple heuristic summary based on length and keywords
        if len(clause_text) < 100:
            return "Short clause with limited scope."
        
        keywords = {
            "must": "party is obligated to",
            "shall": "party must",
            "may": "party has the option to",
            "not": "party is prohibited from",
            "terminate": "contract can be ended",
            "pay": "payment is required",
            "confidential": "information must be kept private"
        }
        
        summary_points = []
        text_lower = clause_text.lower()
        
        for keyword, meaning in keywords.items():
            if keyword in text_lower:
                summary_points.append(f"- {meaning}")
        
        if summary_points:
            return "Key obligations:\n" + "\n".join(summary_points)
        else:
            return "Review clause carefully for exact obligations and restrictions."
