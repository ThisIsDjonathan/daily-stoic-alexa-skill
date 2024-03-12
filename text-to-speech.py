from elevenlabs import generate
from dotenv import load_dotenv
import json
import os
import glob

def list_quote_files():
    return [os.path.splitext(os.path.basename(file))[0] for file in glob.glob("./assets/quotes/*.json")]

def get_quotes_from_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f'Error reading file {path}\n\n: {e}')
        raise e

def process_data(quotes, language):
    my_api_key = get_api_key()
    for i, quote in enumerate(quotes):
        if audio_already_exists_for_quote(i, language):
            print(f'Audio {i+1}.mp3 already exists, skipping.')
            continue
        try:
            print(f'Processing quote {i+1}/{len(quotes)}')
            audio = text_to_speech(quote, my_api_key, language)
            save_audio_to_file(audio, f'./assets/audios/{language}/{i+1}.mp3')
        except Exception as e:
            print(f'Error processing quote {i+1}/{len(quotes)}\n\nERROR: {e}')
            if 'You have reached the limit of unauthenticated requests' in str(e) or 'Free Tier usage disabled' in str(e) or 'This request exceeds your quota.' in str(e):
                print('Stopping due to API limit reached.')
                break
            continue
    show_report(language)

def get_api_key():
    try:
        my_api_key = os.environ['API_KEY']
        if my_api_key == '' or my_api_key == 'your API key goes here':
            raise KeyError
    except KeyError:
        print('API_KEY not found in .env file. Requesting without authentication.')
        my_api_key = None
    return my_api_key

def audio_already_exists_for_quote(quote_number, language):
    return os.path.exists(f'./assets/audios/{language}/{quote_number+1}.mp3')

def text_to_speech(text, my_api_key, language):
    if text == '':
        print('Empty text, skipping.')
        return

    if language == 'english':
        voice_to_use = "Michael"
        model_to_use = "eleven_multilingual_v1"
    else: # this model has more languages available
        voice_to_use = "Rachel"
        model_to_use = "eleven_multilingual_v2"

    if my_api_key is None:
        return generate(text=text, voice=voice_to_use, model=model_to_use)
    else:
        return generate(text=text, api_key=my_api_key, voice=voice_to_use, model=model_to_use)

def save_audio_to_file(audio, filename):
    with open(filename, 'wb') as f:
        f.write(audio)

def create_folders_if_not_exists(language):
    if not os.path.exists('./assets/audios'):
        os.makedirs('./assets/audios')
    if not os.path.exists('./assets/audios/' + language):
        os.makedirs('./assets/audios/' + language)

def show_report(language):
    total_audios_already_created = len(os.listdir(f'./assets/audios/{language}'))
    missing_audios = 366 - total_audios_already_created
    print(f'\n\nREPORT: {total_audios_already_created} of 366 audios in {language} are already created.\nMissing {missing_audios} audios to complete.\n')

def main():
    available_languages = list_quote_files()
    for language in available_languages:
        print(f'Processing language: {language}')
        create_folders_if_not_exists(language)

        quotes = get_quotes_from_file('./assets/quotes/' + language + '.json')
        process_data(quotes, language)

if __name__ == '__main__':
    load_dotenv()
    main()
