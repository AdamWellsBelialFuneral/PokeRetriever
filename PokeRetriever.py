from requests.exceptions import RequestException
from requests import get
from easygui import enterbox, ynbox, msgbox
from PIL import Image
from tempfile import NamedTemporaryFile
from io import BytesIO
from pygame import mixer
from gtts import gTTS
from random import randint

mixer.init(frequency=16000, channels=1)

def readPokemonDescription(description):
    mixer.music.stop()
    tts = gTTS(description, "com.br", "pt-br")
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    mixer.music.load(audio_bytes)
    mixer.music.play()

def getImage(imageURL, size=(256, 256)):
    response = get(imageURL)
    if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)

        image.thumbnail(size)

        temp_file = NamedTemporaryFile(delete=True, suffix=".png")
        temp_file.close()
        image.save(temp_file.name)

        return temp_file.name

    return None

def getPokemonData(pokemonName):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemonName.lower()}"
    try:
        response = get(url)
        if response.status_code == 200:
            pokemon_data = response.json()
            return pokemon_data
        else:
            retry = ynbox("Pokémon data not found. Do you want to retry?", "Retry?", ("Retry", "Exit"))
            if retry:
                getPokemonData(pokemonName)
            
    except RequestException as e:
        msgbox(f"Error: {e}")
        return None

def main():
    title = "PokeRetriever"
    msg = "Encontre Pokémon por nome ou ID, ou insira nada para pesquisar aleatório"
    imageURL = "https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi_256.png"

    while True:
        readPokemonDescription(msg)
        image = getImage(imageURL)
        
        pokemonName = enterbox(msg, title, image=image)

        if pokemonName in (None, "Cancel"):
            break
        if pokemonName == "":
            pokemonName = str(randint(1, 1010))
        
        data = getPokemonData(pokemonName)
        if data:
            msg = (
                f"ID: {data['id']}.\n"
                f"Nome: {data['name']}.\n"
                f"Habilidades: {', '.join([ability['ability']['name'] for ability in data['abilities']])}.\n"
                f"Tipos: {', '.join([type_data['type']['name'] for type_data in data['types']])}.\n"
                f"Movimentos: {', '.join([move_data['move']['name'] for move_data in data['moves'][-4:]])}.\n"
            )
            
            imageURL = data["sprites"]["other"]["official-artwork"]["front_default"]

if __name__ == "__main__":
    main()
    mixer.quit()
