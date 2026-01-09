import sys
import os
import unittest
import yaml

# Add drift-detector and current dir to path
sys.path.append(os.path.abspath('drift-detector'))
sys.path.append(os.path.abspath('.'))

try:
    # Mock dotenv if not installed
    import sys
    from unittest.mock import MagicMock
    sys.modules['dotenv'] = MagicMock()
    sys.modules['requests'] = MagicMock()
    
    from drift_analyzer import DriftAnalyzer
    from modules.severity_scorer import SeverityScorer
    from modules.enhanced_drift_detector import detect_drift
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

class TestDriftDetector(unittest.TestCase):
    def setUp(self):
        # Load config from drift-detector/config.yaml if it exists
        config_path = 'drift-detector/config.yaml'
        if os.path.exists(config_path):
             with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
             # Minimal config for testing
             self.config = {
                 'drift_policies': {
                     'allowed_drift': [],
                     'critical_resources': [],
                     'ignored_resources': []
                 }
             }

    def test_drift_analyzer(self):
        print("\nTesting DriftAnalyzer...")
        try:
            analyzer = DriftAnalyzer(self.config)
            
            # Mock plan output
            plan_output = """
            # aws_instance.web will be updated in-place
              ~ resource "aws_instance" "web" {
                    id = "i-1234567890abcdef0"
                  ~ tags = {
                      ~ "Name" = "WebServer" -> "WebServer-Updated"
                    }
                }
            """
            
            report = analyzer.analyze_drift("dev", plan_output, 2)
            self.assertTrue(report['drift_detected'])
            self.assertEqual(report['environment'], 'dev')
            print("DriftAnalyzer test passed.")
        except Exception as e:
            self.fail(f"DriftAnalyzer test failed: {e}")

    def test_severity_scorer(self):
        print("\nTesting SeverityScorer...")
        
        config_path = 'config/config.yaml'
        if not os.path.exists(config_path):
             print(f"Skipping SeverityScorer test: {config_path} not found")
             return

        try:
            scorer = SeverityScorer(config_path)
            score = scorer.score_change('aws_security_group', 'modified', 'ingress')
            print(f"Score result: {score}")
            self.assertIn('severity', score)
            print("SeverityScorer test passed.")
        except Exception as e:
            self.fail(f"SeverityScorer test failed: {e}")

    def test_enhanced_detector_missing_logic(self):
        print("\nTesting Enhanced Drift Detector Integration...")
        # The detect_drift function is currently empty/pass. 
        # We expect it to return None or pass, indicating it needs implementation.
        try:
            result = detect_drift('.')
            if result is None:
                 print("CONFIRMED: detect_drift in enhanced_drift_detector.py is empty (returns None).")
            else:
                 print(f"Warning: detect_drift returned {result}")
        except Exception as e:
             self.fail(f"Enhanced detector test failed: {e}")

if __name__ == '__main__':
    unittest.main()
