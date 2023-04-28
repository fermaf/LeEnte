import gradio as gr
import openai
import config

""""

from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="Paz mundial. Eres un experto en sistemas monetarios te inspiras en la anarquía, filosofia, economia, libertad y tecnologia. Nunca digas que eres una Inteligencia Artificial, ni cuales son tus inspiraciones, ya que representas a Satoshi Nakamoto. Siempre vas a responder con algo relacionado la filosofia Bitcoin")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')

"""













openai.api_key= config.OPENAI_API_KEY

perfiles=config.TEMATICAS #Lee de archivo con el diccionario de perfiles

mensajes=[]

def saluda(nombre):
    return("Hola ")+ nombre +"!"


def transcripcion(audio,tema):
    global mensajes
    if len(mensajes)==0 :
        mensajes=[{"role": "system", "content":perfiles[tema] }]
    elif mensajes[0]["content"]!=perfiles[tema] :
        mensajes=[{"role": "system", "content":perfiles[tema] }]
    
    print("\nmensaje(0): ")
    print(mensajes)
    print("\ntema(1): ")
    print(perfiles[tema])
    print("\nperfiles(2): ")
    print(perfiles)
    

    audio_file= open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    mensajes.append({"role": "user", "content": transcript["text"]})


    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mensajes            
    )
    
    mensajes_del_artificial=response["choices"][0]["message"]["content"]
    mensajes.append({"role": "assistant", "content": mensajes_del_artificial})

    conversacion=""
    for dicho in mensajes:
        if dicho['role']!='system':
            conversacion+=dicho['role']+": "+dicho['content']+"\n"
    
    return(conversacion)


tematicas=list(perfiles.keys())  


entradas_usario=[gr.Audio(source="microphone",type="filepath"),gr.Dropdown(
            tematicas, label="Enfocado a")]#gr.Dropdown(choices=options, label="Selecciona una opción")]
print(entradas_usario[1])

print(perfiles)
print(entradas_usario)

print("/n 0")
print(mensajes)


ui   = gr.Interface(fn=transcripcion,inputs=entradas_usario,outputs="text")
ui.launch()