import fnmatch
from typing import Dict, List, Any, Tuple

class PolicyEngine:
    def __init__(self, config: Dict[str, Any]):
        policies = config.get('drift_policies', {})
        self.allowed_drift = policies.get('allowed_drift', [])
        self.critical_resources = policies.get('critical_resources', [])
        self.ignored_resources = policies.get('ignored_resources', [])

    def is_resource_ignored(self, resource_address: str) -> bool:
        return any(
            fnmatch.fnmatch(resource_address, pattern)
            for pattern in self.ignored_resources
        )

    def is_critical_resource(self, resource_type: str) -> bool:
        return any(
            fnmatch.fnmatch(resource_type, pattern)
            for pattern in self.critical_resources
        )

    def is_drift_allowed(self, resource_type: str, attribute: str) -> Tuple[bool, str]:
        for policy in self.allowed_drift:
            if fnmatch.fnmatch(resource_type, policy['resource_type']):
                for allowed_attr in policy['attributes']:
                    if self._matches_attribute(attribute, allowed_attr):
                        return True, policy.get('reason', 'Allowed by policy')
        return False, ''

    def _matches_attribute(self, attribute: str, pattern: str) -> bool:
        # Normalize Terraform attribute paths
        normalized = attribute.replace('[', '.').replace(']', '').replace('"', '')

        if pattern.endswith('.*'):
            prefix = pattern[:-2]
            return normalized.startswith(prefix)

        return fnmatch.fnmatch(normalized, pattern)

    def filter_drift(self, drift_data: Dict[str, Any]) -> Dict[str, Any]:
        filtered = {
            'resources_to_add': drift_data.get('resources_to_add', []),
            'resources_to_destroy': drift_data.get('resources_to_destroy', []),
            'resources_to_change': [],
            'policy_decisions': []
        }

        for resource in drift_data.get('resources_to_change', []):
            address = resource.get('address', '')
            rtype = resource.get('type', '')
            changes = resource.get('changes', [])

            if self.is_resource_ignored(address):
                filtered['policy_decisions'].append({
                    'resource': address,
                    'decision': 'ignored',
                    'severity': 'info',
                    'reason': 'Resource ignored by policy'
                })
                continue

            if self.is_critical_resource(rtype):
                filtered['resources_to_change'].append({
                    **resource,
                    'severity': 'critical',
                    'policy_note': 'Critical resource drift detected'
                })
                continue

            blocked, allowed = [], []

            for change in changes:
                attr = change.get('attribute', '')
                is_allowed, reason = self.is_drift_allowed(rtype, attr)

                if is_allowed:
                    allowed.append({'attribute': attr, 'reason': reason})
                else:
                    blocked.append(change)

            if blocked:
                filtered['resources_to_change'].append({
                    **resource,
                    'changes': blocked,
                    'allowed_changes': allowed,
                    'severity': 'warning'
                })
            else:
                filtered['policy_decisions'].append({
                    'resource': address,
                    'decision': 'allowed',
                    'severity': 'info',
                    'allowed_changes': allowed
                })

        return filtered