import yaml
from typing import Dict, List

class SeverityScorer:
    def __init__(self, config_path: str = 'config/config.yaml', rules_path: str = 'config/severity_rules.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        try:
            with open(rules_path, 'r') as f:
                rules = yaml.safe_load(f)
                self.severity_map = rules.get('severity', {})
        except FileNotFoundError:
            # Fallback to config.yaml if separate file missing
            self.severity_map = self.config.get('severity', {})
    
    def score_resource(self, resource_type: str) -> str:
        for severity, resources in self.severity_map.items():
            if resource_type in resources:
                return severity
        return 'low'
    
    def score_change(self, resource_type: str, change_type: str, attribute: str) -> Dict:
        base_severity = self.score_resource(resource_type)
        
        # Escalate security-related changes
        security_attributes = ['security_group_ids', 'iam_policy', 'public', 'ingress', 'egress']
        if any(attr in attribute.lower() for attr in security_attributes):
            base_severity = self._escalate_severity(base_severity)
        
        severity_scores = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        
        return {
            'severity': base_severity,
            'score': severity_scores.get(base_severity, 1),
            'resource_type': resource_type,
            'change_type': change_type,
            'attribute': attribute
        }
    
    def _escalate_severity(self, current: str) -> str:
        escalation = {'low': 'medium', 'medium': 'high', 'high': 'critical'}
        return escalation.get(current, 'critical')