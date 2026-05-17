# utils/colors.py — C9 Faizan Colors
class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def success(msg): return f"{Colors.GREEN}[+] {msg}{Colors.END}"
    @staticmethod
    def info(msg): return f"{Colors.CYAN}[~] {msg}{Colors.END}"
    @staticmethod
    def warn(msg): return f"{Colors.YELLOW}[!] {msg}{Colors.END}"
    @staticmethod
    def error(msg): return f"{Colors.RED}[X] {msg}{Colors.END}"
      
