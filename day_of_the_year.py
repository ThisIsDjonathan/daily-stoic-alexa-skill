from datetime import datetime
from rich.console import Console

console = Console()

def date_to_day_of_the_year(date_str: str) -> int:
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        day_of_year = date_obj.timetuple().tm_yday
    except Exception:
        raise Exception("Invalid date format. Please use YYYY-MM-DD.")
    return day_of_year

def main() -> None:
    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        date_str = console.input(f"[blue]Enter date (YYYY-MM-DD or ENTER for Today {today})[/blue]: ").strip()

        if not date_str:
            date_str = today

        try:
            day_of_year = date_to_day_of_the_year(date_str)
            break
        except Exception as e:
            console.print(f'[bright_red]{e}[/bright_red]')

    console.print(f'[green]Day of the year [bold]{day_of_year}[/bold][dim] - {date_str}[/dim][/green]')

if __name__ == "__main__":
    main()
