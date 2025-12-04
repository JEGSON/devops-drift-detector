from colorama import Fore, Style, init
from tabulate import tabulate
from typing import Dict

init(autoreset=True)


class ConsoleReporter:

    def report(self, drift_report: Dict):

        print("\n" + "="*80)
        print(f"{Fore.CYAN}DRIFT DETECTION REPORT{Style.RESET_ALL}")
        print("="*80)


        print(f"\n📍 Environment: {Fore.YELLOW}{drift_report['environment']}{Style.RESET_ALL}")
        print(f"⏰ Timestamp: {drift_report['timestamp']}")
        print(f"📊 Severity: {self._format_severity(drift_report['severity'])}")
        

        if drift_report['drift_detected']:
            print(f"\n{Fore.RED}⚠️  DRIFT DETECTED!{Style.RESET_ALL}")
            print(f"   {drift_report['summary']}")
        else:
            print(f"\n{Fore.GREEN}✅ NO DRIFT DETECTED{Style.RESET_ALL}")
            print("   Infrastructure matches Terraform state perfectly!")

        details = drift_report['details']
        
        if details['resources_modified']:
            print(f"\n{Fore.YELLOW}📝 Modified Resources:{Style.RESET_ALL}")
            for resource in details['resources_modified']:
                print(f"   • {resource}")
        
        if details['resources_added']:
            print(f"\n{Fore.BLUE}➕ Resources to be Added:{Style.RESET_ALL}")
            for resource in details['resources_added']:
                print(f"   • {resource}")
        
        if details['resources_deleted']:
            print(f"\n{Fore.RED}❌ Resources Deleted (Manual):{Style.RESET_ALL}")
            for resource in details['resources_deleted']:
                print(f"   • {resource}")    

        print(f"\n{Fore.CYAN}💡 Recommendations:{Style.RESET_ALL}")
        for rec in drift_report['recommendations']:
            print(f"   {rec}")
        
        print("\n" + "="*80 + "\n")

    def _format_severity(self, severity: str) -> str:
        """Format severity with colors"""
        if severity == 'critical':
            return f"{Fore.RED}🚨 CRITICAL{Style.RESET_ALL}"
        elif severity == 'warning':
            return f"{Fore.YELLOW}⚠️  WARNING{Style.RESET_ALL}"
        else:
            return f"{Fore.GREEN}ℹ️  INFO{Style.RESET_ALL}"
             