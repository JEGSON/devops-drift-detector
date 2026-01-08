from colorama import Fore, Style, init
from typing import Dict

init(autoreset=True)


class ConsoleReporter:
    """Console-based drift report renderer"""

    def report(self, drift_report: Dict):
        print("\n" + "=" * 80)
        print(f"{Fore.CYAN}DRIFT DETECTION REPORT{Style.RESET_ALL}")
        print("=" * 80)

        print(f"\n📍 Environment: {Fore.YELLOW}{drift_report['environment']}{Style.RESET_ALL}")
        print(f"⏰ Timestamp: {drift_report['timestamp']}")
        print(f"📊 Severity: {self._format_severity(drift_report['severity'])}")

        if drift_report['drift_detected']:
            print(f"\n{Fore.RED}⚠️  DRIFT DETECTED{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✅ NO DRIFT DETECTED{Style.RESET_ALL}")
            print("   Infrastructure matches Terraform state.")

        filtered = drift_report.get('filtered_drift', {})

        # ─── Changed Resources ────────────────────────────────────────────────
        if filtered.get('resources_to_change'):
            print(f"\n{Fore.YELLOW}📝 Resources with Drift:{Style.RESET_ALL}")
            for res in filtered['resources_to_change']:
                icon = "🚨" if res.get('severity') == 'critical' else "⚠️"
                print(f"  {icon} {res['address']} ({res['type']})")

                for change in res.get('changes', []):
                    print(f"     - {change['attribute']}")

                if res.get('allowed_changes'):
                    print(f"     {Fore.GREEN}Allowed changes:{Style.RESET_ALL}")
                    for allowed in res['allowed_changes']:
                        print(f"       ✓ {allowed['attribute']}")

        # ─── Added Resources ─────────────────────────────────────────────────
        if filtered.get('resources_to_add'):
            print(f"\n{Fore.BLUE}➕ Resources to be Created:{Style.RESET_ALL}")
            for res in filtered['resources_to_add']:
                print(f"  • {res['address']}")

        # ─── Destroyed Resources ─────────────────────────────────────────────
        if filtered.get('resources_to_destroy'):
            print(f"\n{Fore.RED}❌ Resources Destroyed:{Style.RESET_ALL}")
            for res in filtered['resources_to_destroy']:
                print(f"  • {res['address']}")

        # ─── Policy Decisions ────────────────────────────────────────────────
        if drift_report.get('policy_decisions'):
            print(f"\n{Fore.CYAN}📋 Policy Decisions:{Style.RESET_ALL}")
            for decision in drift_report['policy_decisions']:
                if decision['decision'] == 'allowed':
                    print(f"  ✅ {decision['resource']}")
                elif decision['decision'] == 'ignored':
                    print(f"  ⏭️  {decision['resource']} (ignored)")

        # ─── Recommendations ────────────────────────────────────────────────
        print(f"\n{Fore.CYAN}💡 Recommendations:{Style.RESET_ALL}")
        for rec in drift_report.get('recommendations', []):
            print(f"  {rec}")

        print("\n" + "=" * 80 + "\n")

    def _format_severity(self, severity: str) -> str:
        if severity == 'critical':
            return f"{Fore.RED}🚨 CRITICAL{Style.RESET_ALL}"
        elif severity == 'warning':
            return f"{Fore.YELLOW}⚠️  WARNING{Style.RESET_ALL}"
        return f"{Fore.GREEN}ℹ️  INFO{Style.RESET_ALL}"