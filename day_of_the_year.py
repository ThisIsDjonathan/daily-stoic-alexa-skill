from datetime import datetime
from rich.console import Console

console = Console()

def main() -> None:
    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        date_str = console.input(f"[blue]Enter date (YYYY-MM-DD or ENTER for Today {today})[/blue]: ").strip()

        if not date_str:
            date_str = today

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            console.print("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]")

    day_of_year = date_obj.timetuple().tm_yday
    console.print(f'[bold green]Day of the year {day_of_year}[dim] - {date_str}[/dim][/bold green]')

if __name__ == "__main__":
    main()
