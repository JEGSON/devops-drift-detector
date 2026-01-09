import subprocess
from typing import Optional
import os

class DependencyMapper:
    def __init__(self, terraform_dir: str):
        self.terraform_dir = terraform_dir
    
    def generate_graph(self, output_dir: str = 'reports') -> Optional[str]:
        """
        Generates a Terraform dependency graph in DOT format.
        """
        try:
            # Check if directory exists
            if not os.path.exists(self.terraform_dir):
                return None

            print("🕸️  Generating dependency graph...")
            result = subprocess.run(
                ["terraform", "graph"],
                cwd=self.terraform_dir,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"Warning: Failed to generate graph: {result.stderr}")
                return None

            timestamp = os.path.basename(output_dir).split('_')[-1] if '_' in output_dir else 'latest'
            filename = f"{output_dir}/dependencies.dot"
            
            with open(filename, 'w') as f:
                f.write(result.stdout)
            
            return filename

        except Exception as e:
            print(f"Error mapping dependencies: {e}")
            return None
