from pydub import AudioSegment
import os

def louder(filename):
    file_path = f'assets/audios/portuguese/{filename}'
    song = AudioSegment.from_mp3(file_path)
    louder_song = song + 15
    louder_song.export(file_path, format='mp3')

def main(language_to_increase_volume):
    for filename in os.listdir(f'assets/audios/{language_to_increase_volume}'):
        try:
            louder(filename)
            print(f'{filename} done.')
        except Exception as e:
            print(f'Error on file {filename}: {e}')
            continue

if __name__ == '__main__':
    language_to_increase_volume = 'portuguese'
    main(language_to_increase_volume)
