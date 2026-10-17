"""
Decoupled Declarative Business Rule Engine for Enterprise Travel Advisory.
Evaluates domain constraints (visa lead time, passport validity, pax limits, discount ceilings).
Groundwork for RQ3 (2x2 Ablation: Rules vs. Drift) and RQ4 (Turn Economy).
"""

import os
import yaml
from typing import Dict, Any, List, Tuple


class RuleViolation:
    def __init__(self, rule_id: str, severity: str, message: str, action: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.action = action

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
            "action": self.action
        }


class DeclarativeRuleEngine:
    def __init__(self, rules_yaml_path: str = "rules/rules_enterprise.yaml"):
        self.rules_path = rules_yaml_path
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.rules_path):
            raise FileNotFoundError(f"Rules YAML not found: {self.rules_path}")
        with open(self.rules_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get('rules', [])

    def evaluate_booking_state(self, state: Dict[str, Any]) -> Tuple[bool, List[RuleViolation]]:
        """
        Evaluates current dialogue state against declarative business rules.
        Returns: (is_compliant, list_of_violations)
        """
        violations = []
        is_international = state.get('is_international', True)
        departure_lead_days = state.get('departure_lead_days', 30)
        passport_expiry_months = state.get('passport_expiry_months', 12)
        traveler_count_adults = state.get('traveler_count_adults', 2)
        package_type = state.get('package_type', 'FIT')
        discount_applied = state.get('discount_applied_percentage', 0.0)
        budget = state.get('budget_amount')

        for r in self.rules:
            rid = r.get('id')
            if rid == "RULE_VISA_WINDOW":
                if is_international and departure_lead_days is not None and departure_lead_days < 15:
                    violations.append(RuleViolation(
                        rule_id=rid,
                        severity=r.get('severity', 'FATAL'),
                        message=r.get('error_message', 'Visa lead time violation'),
                        action=r.get('action', 'BLOCK_AND_FLAG')
                    ))

            elif rid == "RULE_PASSPORT_VALIDITY":
                if is_international and passport_expiry_months is not None and passport_expiry_months < 6:
                    violations.append(RuleViolation(
                        rule_id=rid,
                        severity=r.get('severity', 'FATAL'),
                        message=r.get('error_message', 'Passport validity below 6 months'),
                        action=r.get('action', 'BLOCK_AND_FLAG')
                    ))

            elif rid == "RULE_PAX_CAPACITY":
                if package_type == 'FIT' and traveler_count_adults is not None and traveler_count_adults > 8:
                    violations.append(RuleViolation(
                        rule_id=rid,
                        severity=r.get('severity', 'WARNING'),
                        message=r.get('error_message', 'Exceeds FIT capacity'),
                        action=r.get('action', 'CONVERT_TO_GROUP')
                    ))

            elif rid == "RULE_DISCOUNT_THRESHOLD":
                if discount_applied is not None and discount_applied > 15.0:
                    violations.append(RuleViolation(
                        rule_id=rid,
                        severity=r.get('severity', 'FATAL'),
                        message=r.get('error_message', 'Discount exceeds 15% threshold'),
                        action=r.get('action', 'CLAMP_DISCOUNT')
                    ))

            elif rid == "RULE_BUDGET_MINIMUM":
                if is_international and budget is not None and budget < 500:
                    violations.append(RuleViolation(
                        rule_id=rid,
                        severity=r.get('severity', 'WARNING'),
                        message=r.get('error_message', 'Stated budget below operational threshold'),
                        action=r.get('action', 'PROMPT_REALISTIC_BUDGET')
                    ))

        is_compliant = len([v for v in violations if v.severity == 'FATAL']) == 0
        return is_compliant, violations


if __name__ == "__main__":
    engine = DeclarativeRuleEngine()
    test_state = {
        "is_international": True,
        "departure_lead_days": 8,
        "passport_expiry_months": 3,
        "traveler_count_adults": 10,
        "package_type": "FIT",
        "discount_applied_percentage": 20.0,
        "budget_amount": 350
    }
    compliant, viols = engine.evaluate_booking_state(test_state)
    print(f"Rule compliance: {compliant}, Total violations: {len(viols)}")
    for v in viols:
        print(f"  [{v.severity}] {v.rule_id}: {v.message}")
