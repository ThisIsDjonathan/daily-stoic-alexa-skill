
<h1 align="center">Welcome to daily-stoic-alexa-skill 👋🏛️📜 </h1>

This project aims to provide daily Stoic quotes for Alexa users and show how I built my first Alexa Skill 😄💻

You can download this skill on the Skill Store in your Alexa app.
- Download the **English** version for free [here]([url](https://www.amazon.com.br/Djonathan-Krause-Di%C3%A1rio-Estoico/dp/B0CRZ9Y9K7/ref=sr_1_1?brr=1&qid=1708199685&rd=1&s=alexa-skills&sr=1-1))!
- Baixe grátis a versão em **Português** [aqui]([url](https://www.amazon.com.br/Djonathan-Krause-Di%C3%A1rio-Estoico/dp/B0CRZ9Y9K7/ref=sr_1_1?brr=1&qid=1708199685&rd=1&s=alexa-skills&sr=1-1))!

# How I built this
The premise for this Alexa Skill was to have a single Stoic Quote for each day of the year.<br>
So the first thing I did was create a `.json` file with 366 entries.

📦 daily-stoic-alexa-skill<br>
┣ 📂 assets<br>
┃ ┗ 📜 `quotes-in-portuguese.json`<br>
┃ ┗ 📜 `quotes-in-english.json`<br>


## The Speech to Text 🗣️👂
On the first try, I used a text feed but the current text-to-speech used by Alexa is very bad, so I used the [ElevenLabs](https://github.com/elevenlabs/elevenlabs-python/tree/main) library + API to convert the text-to-speech.
<br><br>This is done by the code in the `text-to-speech.py` file. More details on how to run this are in the [Contributing 🤝](#Contributing) section.

<br>The result was 366 `.mp3` files.
📦 daily-stoic-alexa-skill<br>
┣ 📂 assets<br>
┃ ┗ 📂 audios<br>
┃   ┗ 📂 portuguese <br>
┃&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┗ 🎧 `1.mp3`<br>
┃&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┗ 🎧 `2.mp3`<br>
┃   ┗ 📂 english <br>
┃&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┗ 🎧 `366.mp3`<br>

## The Alexa Skill 🤖
The Alexa Skill is a Flash Briefing skill created in the [Alexa Developer Console](https://developer.amazon.com/alexa/console) that will consume our JSON feed API hosted on AWS.
<br>These are the docs I used for reference:<br>
- [Understand the Flash Briefing Skill](https://developer.amazon.com/en-US/docs/alexa/flashbriefing/understand-the-flash-briefing-skill-api.html)
- [Flash Briefing Skill API Feed Reference](https://developer.amazon.com/en-US/docs/alexa/flashbriefing/flash-briefing-skill-api-feed-reference.html)


## Amazon Lambda and S3 🪣λ
To feed the Alexa Skill I created a Lambda function hosted on AWS. This is a simple python script that will fetch the `mp3` file for the current date.
The `mp3` files are hosted in an S3 bucket and the Lambda Function has an API Gateway so the Alexa Skill can consume it.

The script details can be found in the `TheDailyStoic-LambdaFunction.py` file 🐍

## Contributing 🤝
### You can contribute by adding support for more languages! 🌎<br>

#### Translating the quotes
To do so, first, you have to translate the `quotes-in-english.json` to your language and then create a new `quotes-in-YOUR_LANGUAGE.json` file and put it in the `assets/` directory.

<br>📦 daily-stoic-alexa-skill<br>
┣ 📂 assets<br>
┃ ┗ 📜 `quotes-in-YOUR_LANGUAGE.json`<br>

#### Getting an ElevenLabs API Key
You can do the text-to-speech using another tool, but if you want to use the same I used just go to the [ElevenLabs website](https://elevenlabs.io/) and create a free account.
You will get an `API Key` by clicking on your name in the bottom right corner, then click on `Profile` and copy your API Key.

#### Running the code
Then let's run the code in your environment!
First, install the Python dependencies `python-dotenv` and `elevenlabs`:
```sh
pip install -r requirements.txt
```

Then update the `.env` file by adding your API Key.
📦 daily-stoic-alexa-skill
┣ 📜 `.env`
```
API_KEY='your API key goes here'
```

Update the `main()` function in the `text-to-speech.py` file adding your language:
```
def main():
    create_folders_if_not_exists()

    quotes = get_quotes_from_file('./quotes-in-english.json')
    process_data(quotes, 'english')

    # add your code here!
    quotes = get_quotes_from_file('./quotes-in-YOUR_LANGUAGE.json')
    process_data(quotes, 'YOUR_LANGUAGE')
```

#### Push a PR
Finally, push a PR to this repo. I will merge it, add the new audio files to the S3 bucket, and make the Alexa Skill available in your country.
Please specify the language you are adding, the country where you are from, and your name to the PR description!

## Author
👤 **Djonathan Krause**
- Website: [djonathan.com](https://www.djonathan.com)
- Github: [@ThisIsDjonathan](https://github.com/ThisIsDjonathan)

## Show your support
Please ⭐️ this repository if this project helped you!
<br><br><a href="https://www.buymeacoffee.com/djonathan" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

