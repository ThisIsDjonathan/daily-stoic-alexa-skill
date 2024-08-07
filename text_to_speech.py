from elevenlabs import generate
from dotenv import load_dotenv
import json
import os
import glob
from rich.console import Console
from rich.progress import track
from typing import List, Optional

console = Console()

QUOTES_DIR = os.path.join("assets", "quotes")
AUDIOS_DIR = os.path.join("assets", "audios")

def list_quote_files() -> List[str]:
    return [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(os.path.join(QUOTES_DIR, "*.json"))]

def get_quotes_from_file(path: str) -> List[str]:
    """Read quotes from a JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        console.print(f'[bold red]Error reading file {path}[/bold red]\n\n: {e}')
        raise e

def process_data(quotes: List[str], language: str, quote_number: Optional[int] = None, force: bool = False) -> None:
    """Process quotes and generate audio files."""
    my_api_key = get_api_key()
    quotes_to_process = quotes if quote_number is None else [quotes[quote_number - 1]]
    for i, quote in enumerate(track(quotes_to_process, description=f"Processing quotes in {language}...")):
        actual_index = i if quote_number is None else quote_number - 1
        if not force and audio_already_exists_for_quote(actual_index, language):
            console.print(f' [yellow]Audio {actual_index+1}.mp3 already exists, skipping.[/yellow]')
            continue
        try:
            console.print(f' [green]Processing quote {actual_index+1}/{len(quotes)}[/green]')
            audio = text_to_speech(quote, my_api_key, language)
            save_audio_to_file(audio, os.path.join(AUDIOS_DIR, language, f'{actual_index+1}.mp3'))
        except Exception as e:
            console.print(f' [bold red]Error processing quote {actual_index+1}/{len(quotes)}[/bold red]\n\nERROR: {e}')
            if any(limit in str(e) for limit in ['You have reached the limit of unauthenticated requests', 'Free Tier usage disabled', 'This request exceeds your quota.']):
                console.print('[bold red]Stopping due to API limit reached.[/bold red]')
                break
            continue
    show_report(language)

def get_api_key() -> Optional[str]:
    """Retrieve the API key from environment variables."""
    try:
        my_api_key = os.environ['API_KEY']
        if not my_api_key or my_api_key == 'your API key goes here':
            raise KeyError
    except KeyError:
        console.print('[bold yellow]API_KEY value not found in .env file. Requesting without authentication.[/bold yellow]')
        my_api_key = None
    return my_api_key

def audio_already_exists_for_quote(quote_number: int, language: str) -> bool:
    return os.path.exists(os.path.join(AUDIOS_DIR, language, f'{quote_number+1}.mp3'))

def text_to_speech(text: str, my_api_key: Optional[str], language: str) -> bytes:
    """Convert text to speech using the ElevenLabs API."""
    if not text:
        console.print('[yellow]Empty text, skipping.[/yellow]')
        return b''

    voice_to_use = "Bill"
    model_to_use = "eleven_multilingual_v1" if language == 'english' else "eleven_multilingual_v2"

    return generate(text=text, api_key=my_api_key, voice=voice_to_use, model=model_to_use)

def save_audio_to_file(audio: bytes, filename: str) -> None:
    """Save audio data to a file."""
    with open(filename, 'wb') as f:
        f.write(audio)

def create_folders_if_not_exists(language: str) -> None:
    os.makedirs(os.path.join(AUDIOS_DIR, language), exist_ok=True)

def show_report(language: str) -> None:
    """Show a report of the audio files created."""
    audio_files = [file for file in os.listdir(os.path.join(AUDIOS_DIR, language)) if file.endswith('.mp3')]
    total_audios_already_created = len(audio_files)
    missing_audios = 366 - total_audios_already_created
    console.print(f'\n\n[bold blue]REPORT:[/bold blue] {total_audios_already_created} of 366 audios in {language} are already created.\nMissing {missing_audios} audios to complete.\n')

def main() -> None:
    """Main function to process all available languages."""
    available_languages = list_quote_files()

    while True:
        language = console.input(f"Enter language {available_languages}: ").strip()
        if language not in available_languages:
            console.print(f'[bold red]Language [code]{language}[/code] not found. [italic]Available languages: {available_languages}[/italic][/bold red]')
        else:
            break

    while True:
        quote_number = console.input("Enter quote number (optional): ").strip()
        quote_number = int(quote_number) if quote_number.isdigit() else None
        if quote_number is not None and (quote_number < 1 or quote_number > 366):
            console.print(f'[bold red]Invalid quote number [code]{quote_number}[/code]. [italic]Must be between 1 and 366.[/italic][/bold red]')
        else:
            break

    while True:
        force = console.input("Force processing (y/n): ").strip()
        if force.lower() not in ['y', 'n']:
            console.print(f'[bold red]Invalid option [code]{force}[/code]. [italic]Must be y or n.[/italic][/bold red]')
        force = force.lower() == 'y'
        if force:
            console.print('[bold yellow]Force processing enabled. Existing audio files will be overwritten.[/bold yellow]')
        break

    create_folders_if_not_exists(language)
    quotes = get_quotes_from_file(os.path.join(QUOTES_DIR, f'{language}.json'))
    process_data(quotes, language, quote_number, force)

if __name__ == '__main__':
    load_dotenv()
    main()
