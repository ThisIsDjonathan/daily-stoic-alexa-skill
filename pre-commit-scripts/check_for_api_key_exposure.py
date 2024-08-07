import sys
from rich.console import Console

def check_api_key():
    with open('.env', 'r') as file:
        dotenv_content = file.read()
        if "API_KEY='your API key goes here'" not in dotenv_content:
            console.print("[bright_red]Error: You can't change the API_KEY value on [code] .env [/code]![/bright_red]")
            return False
    return True

if __name__ == "__main__":
    console = Console(style="magenta",highlight=False)
    if not check_api_key():
        sys.exit(1)