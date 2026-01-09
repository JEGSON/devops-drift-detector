import os
import subprocess
import json 
from typing import Dict, List, Optional, Tuple
from pathlib import Path



class TerraformClient:

    def __init__(self, working_dir: str):

        if not os.path.isabs(working_dir):
            self.working_dir = Path(working_dir).resolve()
        else:
            self.working_dir = Path(working_dir).resolve()
        
        if not self.working_dir.exists():
            raise ValueError(f"Terraform directory does not exist: {self.working_dir}")
    
        
    def init(self) -> Tuple[bool, str]:

        try:
            result = subprocess.run(
                ["terraform", "init", "-input=false"],    
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=300
            )    
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
        
    def plan(self, detailed_exitcode: bool = True) -> Tuple[int, str, str]:
        """
        Run terraform plan
        
        Returns:
            (exit_code, stdout, stderr)
            Exit codes:
            0 = No changes
            1 = Error
            2 = Changes detected (drift!)
        """

        try:
            cmd = ["terraform", "plan", "-input=false", "-no-color"]
            if detailed_exitcode:
                cmd.append("-detailed-exitcode")

            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=300
            )

            return result.returncode, result.stdout, result.stderr
        
        except subprocess.TimeoutExpired:
            return 1, "", "Terraform plan timed out."
        except Exception as e:
            return 1, "", str(e)
        
    def show_json(self) -> Optional[Dict]:
        """
        Get current state in JSON format
        """
        try:
            result = subprocess.run(
                ["terraform", "show", "-json"],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            return None
            
        except Exception as e:
            print(f"Error getting Terraform state: {e}")
            return None
        
    def get_outputs(self) -> Dict:
        """Get Terraform outputs"""
        try:
            result = subprocess.run(
                ["terraform", "output", "-json"],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {}
            
        except Exception as e:
            print(f"Error getting outputs: {e}")
            return {}    

    def parse_plan_output(self, plan_output: str) -> Dict:
        """
        Parse terraform plan output to extract drift information
        
        Returns a dict with:
        - resources_to_add: []
        - resources_to_change: []
        - resources_to_destroy: []
        - drift_detected: bool
        """
        lines = plan_output.split('\n')

        result = {
            'resources_to_add': [],
            'resources_to_change': [],
            'resources_to_destroy': [],
            'drift_detected': False,
            'summary': ''
        }

        for line in lines:
            if 'Plan:' in line:
                result['summary'] = line.strip()
                result['drift_detected'] = True

            if line.strip().startswith('#'):
                resource_line = line.strip()

                if 'will be created' in resource_line:
                    resource_name = resource_line.split()[1]
                    result['resources_to_add'].append(resource_name)

                elif 'will be updated in-place' in resource_line or 'will be modified' in resource_line:
                    resource_name = resource_line.split()[1]
                    result['resources_to_change'].append(resource_name)
                    
                elif 'will be destroyed' in resource_line:
                    resource_name = resource_line.split()[1]
                    result['resources_to_destroy'].append(resource_name)    

        return result                
                    
