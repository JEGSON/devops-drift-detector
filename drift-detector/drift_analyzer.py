from typing import Dict, List
from datetime import datetime

from policy_engine import PolicyEngine


class DriftAnalyzer:
    """Analyze Terraform drift and apply policy decisions"""

    def __init__(self, config: Dict):
        self.config = config
        self.policy_engine = PolicyEngine(config)

    def analyze_drift(self, environment: str, plan_output: str, exit_code: int) -> Dict:
        """
        Main drift analysis entry point
        """
        raw_drift = self._parse_plan_output(plan_output)

        filtered_drift = self.policy_engine.filter_drift(raw_drift)

        severity = self._calculate_severity(filtered_drift)

        return {
            'environment': environment,
            'timestamp': datetime.utcnow().isoformat(),
            'drift_detected': exit_code == 2,
            'severity': severity,
            'raw_drift': raw_drift,
            'filtered_drift': filtered_drift,
            'policy_decisions': filtered_drift.get('policy_decisions', []),
            'recommendations': self._generate_recommendations(filtered_drift, severity)
        }

    def _parse_plan_output(self, output: str) -> Dict:
        """
        Parse terraform plan output (enhanced for modern Terraform versions)
        """
        drift = {
            'resources_to_add': [],
            'resources_to_change': [],
            'resources_to_destroy': []
        }

        lines = output.splitlines()
        for i, line in enumerate(lines):
            line = line.strip()
            if not line.startswith('# '):
                continue
            
            # Remove '# ' prefix
            content = line[2:].strip()

            if 'will be created' in content:
                resource = content.split('will be')[0].strip()
                drift['resources_to_add'].append({'address': resource})

            elif 'will be destroyed' in content:
                resource = content.split('will be')[0].strip()
                drift['resources_to_destroy'].append({'address': resource})

            elif 'will be updated in-place' in content or 'must be replaced' in content:
                is_replacement = 'must be replaced' in content
                separator = 'must be' if is_replacement else 'will be'
                resource = content.split(separator)[0].strip()
                
                # Attempt to extract type
                rtype = resource.split('.')[-2] if len(resource.split('.')) >= 2 else 'unknown'
                
                # Try to get precise type from the next line
                # e.g. -/+ resource "aws_instance" "web" {
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    parts = next_line.split()
                    if len(parts) >= 3 and parts[1] == 'resource':
                         rtype = parts[2].strip('"')

                changes = []
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if next_line.startswith('# '):
                        break
                    
                    # Check for attribute changes (~, +, -) ignoring the resource def line
                    if (next_line.startswith('~') or next_line.startswith('+') or next_line.startswith('-')) and ('=' in next_line or '->' in next_line):
                         # Skip the resource declaration line itself (containing "resource")
                         if ' resource ' not in next_line:
                            clean_line = next_line.lstrip('~+- ')
                            attr = clean_line.split('=')[0].strip()
                            changes.append({
                                'attribute': attr,
                                'change': next_line
                            })
                    j += 1

                drift['resources_to_change'].append({
                    'address': resource,
                    'type': rtype,
                    'changes': changes,
                    'is_replacement': is_replacement,
                    'severity': 'critical' if is_replacement else 'warning'
                })

        return drift

    def _calculate_severity(self, filtered_drift: Dict) -> str:
        """
        Severity based on filtered (policy-aware) drift
        """
        if filtered_drift.get('resources_to_destroy'):
            return 'critical'

        for res in filtered_drift.get('resources_to_change', []):
            if res.get('severity') == 'critical':
                return 'critical'

        if filtered_drift.get('resources_to_change'):
            return 'warning'

        if filtered_drift.get('resources_to_add'):
            return 'info'

        return 'info'

    def _generate_recommendations(self, filtered_drift: Dict, severity: str) -> List[str]:
        recommendations = []

        if severity == 'info':
            recommendations.append("✅ No critical drift detected.")

        if filtered_drift.get('resources_to_change'):
            recommendations.append(
                "⚠️ Some resources drifted outside Terraform. "
                "Review and run `terraform apply` if needed."
            )

        if filtered_drift.get('resources_to_destroy'):
            recommendations.append(
                "🚨 Critical drift detected: resources were deleted manually. "
                "Immediate action required."
            )

        recommendations.append(
            "💡 Best practice: manage infrastructure changes only through Terraform."
        )

        return recommendations