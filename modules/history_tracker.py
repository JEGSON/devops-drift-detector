import boto3
import json
from datetime import datetime
from decimal import Decimal
from typing import Dict, List

class HistoryTracker:
    def __init__(self, table_name: str = 'terraform-drift-history'):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def save_scan_result(self, scan_data: Dict):
        timestamp = int(datetime.now().timestamp())
        scan_id = f"scan_{timestamp}"
        
        item = {
            'scan_id': scan_id,
            'timestamp': timestamp,
            'environment': scan_data.get('environment', 'unknown'),
            'total_resources': scan_data.get('total_resources', 0),
            'drifted_resources': scan_data.get('drifted_resources', 0),
            'drift_percentage': Decimal(str(scan_data.get('drift_percentage', 0))),
            'critical_count': scan_data.get('critical_count', 0),
            'high_count': scan_data.get('high_count', 0),
            'drift_details': json.dumps(scan_data.get('drift_details', []))
        }
        
        self.table.put_item(Item=item)
        return scan_id
    
    def get_drift_history(self, days: int = 30) -> List[Dict]:
        from datetime import timedelta
        
        cutoff = int((datetime.now() - timedelta(days=days)).timestamp())
        
        response = self.table.scan(
            FilterExpression='#ts >= :cutoff',
            ExpressionAttributeNames={'#ts': 'timestamp'},
            ExpressionAttributeValues={':cutoff': cutoff}
        )
        
        return response.get('Items', [])
    
    def get_frequent_drifters(self, days: int = 30) -> List[Dict]:
        history = self.get_drift_history(days)
        resource_drift_count = {}
        
        for scan in history:
            details = json.loads(scan.get('drift_details', '[]'))
            for drift in details:
                resource = drift.get('resource_address', 'unknown')
                resource_drift_count[resource] = resource_drift_count.get(resource, 0) + 1
        
        return sorted(
            [{'resource': k, 'drift_count': v} for k, v in resource_drift_count.items()],
            key=lambda x: x['drift_count'],
            reverse=True
        )[:10]