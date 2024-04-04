from pydub import AudioSegment
import os
import sys

INCREASE_VOLUME_IN_DB = 13

def louder(language_to_increase_volume, filename):
    file_path = f'assets/audios/{language_to_increase_volume}/{filename}'
    song = AudioSegment.from_mp3(file_path)
    louder_song = song + INCREASE_VOLUME_IN_DB
    louder_song.export(file_path, format='mp3')

def main(language_to_increase_volume):
    if len(sys.argv) > 1:
        full_filename = sys.argv[1]
        full_filename_parts = full_filename.split('/')
        language = full_filename_parts[2]
        dotmp3_filename = full_filename_parts[-1]
        print(f'Making the {full_filename} louder')
        louder(language, dotmp3_filename)
        print(f'{dotmp3_filename} done.')
        return

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
