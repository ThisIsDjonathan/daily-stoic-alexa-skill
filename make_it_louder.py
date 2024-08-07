import os
from pydub import AudioSegment
from rich.console import Console
from text_to_speech import list_quote_files

console = Console()

INCREASE_VOLUME_IN_DB = 13

def louder(file_path):
    """Increase the volume of the audio file by a specified amount."""
    song = AudioSegment.from_mp3(file_path)
    louder_song = song + INCREASE_VOLUME_IN_DB
    louder_song.export(file_path, format='mp3')

def get_language(available_languages):
    """Prompt the user to enter a valid language."""
    while True:
        language = console.input(f"[blue]Enter language {available_languages}: [/blue]").strip()
        if language not in available_languages:
            console.print(f'[bold red]Language [code]{language}[/code] not found. [italic]Available languages: {available_languages}[/italic][/bold red]')
        else:
            return language

def get_file_path(language):
    """Prompt the user to enter a valid file path or choose to process all files."""
    while True:
        user_input = console.input(
            f"[blue]Enter day of the year - [italic]e.g., input [code]1[/code] to make [code]assets/audios/{language}/1.mp3[/code] louder[/italic]\n"
            f"or [bold]ENTER[/bold] to process all files for language [code]{language}[/code]: [/blue]"
        ).strip()
        if user_input:
            file_path = f'assets/audios/{language}/{user_input}.mp3'
            if not os.path.exists(file_path):
                console.print(f'[bold red]File not found: {file_path}[/bold red]')
            else:
                return file_path
        else:
            return None

def process_files(language, file_path=None):
    """Process the specified file or all files in the language directory."""
    if file_path:
        console.print(f'[bold blue]Making the {file_path} louder[/bold blue]')
        louder(file_path)
        console.print(f'[bold green]{file_path} done.[/bold green]')
    else:
        console.print(f'[bold blue]Making all {language} audios louder[/bold blue]')
        for filename in os.listdir(f'assets/audios/{language}'):
            try:
                file_path = f'assets/audios/{language}/{filename}'
                louder(file_path)
                console.print(f'[bold green]{filename} done.[/bold green]')
            except Exception as e:
                console.print(f'[bold red]Error on file {filename}: {e}[/bold red]')

def main():
    available_languages = list_quote_files()
    language = get_language(available_languages)
    file_path = get_file_path(language)
    process_files(language, file_path)

if __name__ == '__main__':
    main()