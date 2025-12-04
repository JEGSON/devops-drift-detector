import json
from pathlib import Path
from datetime import datetime
from typing import Dict



class JSONReporter:

    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def report(self, drift_report: Dict):
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        environment = drift_report['environment']
        filename = f"drift_report_{environment}_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(drift_report, f, indent=2)
        
        print(f"📄 Report saved to: {filepath}")