"""
Prompt Assembler for Dynamic In-Context Few-Shot Conditioning.
Implements Slot Masking and Dynamic Cluster-Adaptive Prompt Construction.
"""

import re
from typing import List, Dict, Any


def mask_dialogue_slots(utterance: str) -> str:
    """
    Applies slot masking to prevent LLM factual leakage.
    Replaces concrete entity values with abstract tokens.
    """
    text = utterance
    # Mask currency amounts
    text = re.sub(r'(\$|INR|Rs\.?|CAD|EUR)\s?\d+(?:,\d{3})*(?:\.\d+)?', '[BUDGET]', text, flags=re.I)
    text = re.sub(r'\b\d{3,5}\s?(?:dollars|rupees|bucks|euros)\b', '[BUDGET]', text, flags=re.I)
    # Mask dates
    text = re.sub(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{0,4}\b', '[DATE]', text, flags=re.I)
    text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '[DATE]', text)
    # Mask passenger numbers
    text = re.sub(r'\b\d+\s+(?:adults?|children|kids?|pax|people|passengers?)\b', '[PAX_COUNT]', text, flags=re.I)
    return text


class PromptAssembler:
    def __init__(self):
        self.system_instruction = (
            "You are an enterprise AI travel counseling assistant. "
            "Help the client plan their vacation itinerary while maintaining policy guidelines, "
            "verifying visa and passport validity, and eliciting necessary booking constraints."
        )

    def assemble_zero_shot_prompt(self, current_conversation_history: List[str]) -> str:
        """
        Mode 1: Zero-Shot baseline with instruction only.
        """
        history_text = "\n".join(current_conversation_history)
        return (
            f"SYSTEM: {self.system_instruction}\n\n"
            f"CURRENT CONVERSATION:\n{history_text}\n\n"
            f"AGENT RESPONSE:"
        )

    def assemble_static_few_shot_prompt(
        self,
        current_conversation_history: List[str],
        static_exemplar: str
    ) -> str:
        """
        Mode 2: Static Few-Shot baseline with fixed generic exemplar.
        """
        history_text = "\n".join(current_conversation_history)
        masked_exemplar = mask_dialogue_slots(static_exemplar)
        return (
            f"SYSTEM: {self.system_instruction}\n\n"
            f"REFERENCE CONVERSATION EXEMPLAR:\n{masked_exemplar}\n\n"
            f"CURRENT CONVERSATION:\n{history_text}\n\n"
            f"AGENT RESPONSE:"
        )

    def assemble_cluster_adaptive_prompt(
        self,
        current_conversation_history: List[str],
        retrieved_exemplars: List[str],
        archetype_name: str
    ) -> str:
        """
        Mode 3: Dynamic Cluster-Adaptive Few-Shot with archetype-conditioned exemplars.
        """
        history_text = "\n".join(current_conversation_history)
        exemplars_text = "\n---\n".join([mask_dialogue_slots(ex) for ex in retrieved_exemplars])

        # Stylistic pacing directive conditioned on archetype
        pacing_directives = {
            "Hesitant Explorer / Consultative": "Maintain an empathetic, patient consultative tone. Provide guided suggestions and explore options without rushing the booking.",
            "Budget Negotiator / Value-Conscious": "Acknowledge cost constraints proactively. Emphasize value trade-offs, flexible alternative dates, and package inclusions.",
            "Rapid Transactional / Corporate": "Be concise, rapid, and transaction-oriented. Confirm dates, traveler counts, and booking actions immediately without unnecessary pleasantries."
        }
        directive = pacing_directives.get(archetype_name, "Engage professionally and address the client's requirements.")

        return (
            f"SYSTEM: {self.system_instruction}\n"
            f"CONVERSATIONAL STYLE DIRECTIVE ({archetype_name}): {directive}\n\n"
            f"ARCHETYPE-ALIGNED IN-CONTEXT EXEMPLARS:\n{exemplars_text}\n\n"
            f"CURRENT CONVERSATION:\n{history_text}\n\n"
            f"AGENT RESPONSE:"
        )
