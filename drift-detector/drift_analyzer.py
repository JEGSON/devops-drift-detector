
from typing import Dict, List
from datetime import datetime


class DriftAnalyzer:
    """Analyze drift detection results"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.ignore_attributes = config.get('detection', {}).get('ignore_attributes', [])
    
    def analyze_drift(self, environment: str, plan_result: Dict) -> Dict:
        """
        Analyze drift detection results and categorize by severity
        
        Returns a structured report
        """
        # Make sure drift_detected exists
        drift_detected = plan_result.get('drift_detected', False)
        
        drift_report = {
            'environment': environment,
            'timestamp': datetime.now().isoformat(),
            'drift_detected': drift_detected,  # FIXED: Ensure this is always present
            'summary': plan_result.get('summary', 'No changes detected'),
            'details': {
                'resources_added': plan_result.get('resources_to_add', []),
                'resources_modified': plan_result.get('resources_to_change', []),
                'resources_deleted': plan_result.get('resources_to_destroy', [])
            },
            'severity': self._calculate_severity(plan_result),
            'recommendations': self._generate_recommendations(plan_result, drift_detected)
        }
        
        return drift_report
    
    def _calculate_severity(self, plan_result: Dict) -> str:
        """
        Calculate severity based on type of drift
        
        Returns: 'critical', 'warning', or 'info'
        """
        num_deleted = len(plan_result.get('resources_to_destroy', []))
        num_modified = len(plan_result.get('resources_to_change', []))
        num_added = len(plan_result.get('resources_to_add', []))
        
        # Deletions are critical
        if num_deleted > 0:
            return 'critical'
        
        # Many modifications are warnings
        if num_modified > 3:
            return 'warning'
        
        # Small changes or additions are info
        if num_modified > 0 or num_added > 0:
            return 'warning'
        
        return 'info'
    
    def _generate_recommendations(self, plan_result: Dict, drift_detected: bool) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if not drift_detected:
            recommendations.append("✅ No drift detected. Infrastructure matches Terraform state.")
            return recommendations
        
        num_modified = len(plan_result.get('resources_to_change', []))
        num_added = len(plan_result.get('resources_to_add', []))
        num_deleted = len(plan_result.get('resources_to_destroy', []))
        
        if num_modified > 0:
            recommendations.append(
                f"⚠️  {num_modified} resource(s) modified outside Terraform. "
                "Run 'terraform apply' to restore desired state."
            )
        
        if num_added > 0:
            recommendations.append(
                f"ℹ️  {num_added} resource(s) will be created. "
                "Review if these are intentional additions."
            )
        
        if num_deleted > 0:
            recommendations.append(
                f"🚨 {num_deleted} resource(s) were deleted manually! "
                "This is CRITICAL. Run 'terraform apply' immediately to recreate."
            )
        
        recommendations.append(
            "\n💡 Best practice: Always make infrastructure changes through Terraform, never manually."
        )
        
        return recommendations