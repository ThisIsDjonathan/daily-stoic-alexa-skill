from pydub import AudioSegment
import os

INCREASE_VOLUME_IN_DB = 13

def louder(language_to_increase_volume, filename):
    file_path = f'assets/audios/{language_to_increase_volume}/{filename}'
    song = AudioSegment.from_mp3(file_path)
    louder_song = song + INCREASE_VOLUME_IN_DB
    louder_song.export(file_path, format='mp3')

def main(language_to_increase_volume):
    for filename in os.listdir(f'assets/audios/{language_to_increase_volume}'):
        try:
            louder(language_to_increase_volume, filename)
            print(f'{filename} done.')
        except Exception as e:
            print(f'Error on file {filename}: {e}')
            continue

if __name__ == '__main__':
    language_to_increase_volume = 'portuguese'
    main(language_to_increase_volume)
