import os, config, requests
import gradio as gr
import openai
import config
import pandas as pd
import numpy as np

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

    print("\nperfiles(2): ")
    print(perfiles)

    print("\ntema(1): ")
    print(perfiles[tema])


    print("\nmensaje(0): ")
    print(mensajes)
    
    

    audio_file= open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    mensajes.append({"role": "user", "content": transcript["text"]})


    response=openai.ChatCompletion.create(
        #model="gpt-4",
        model="gpt-3.5-turbo",
        messages=mensajes            
    )
    
    mensajes_del_artificial = response["choices"][0]["message"]["content"] #relacinado con btn.click
                        
    #mensajes_del_artificial=response["choices"][0]["message"]["content"]
    mensajes.append({"role": "assistant", "content": mensajes_del_artificial})

    #audio text to speech solicitud a eleven labs
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config.ADVISOR_VOICE_ID}/stream"
    data = {
        "text": mensajes_del_artificial.replace('"', ''),
        "model_id":"eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.85,
            "similarity_boost": 0.9
        }
    }

    r = requests.post(url, headers={'xi-api-key': config.ELEVEN_LABS_API_KEY}, json=data)
    archivo_salida_audio = "respuestaAI.mp3"
    with open(archivo_salida_audio, "wb") as output:
        output.write(r.content)

  

    #FIN AUDIO




    conversacion=""
    for dicho in mensajes:
        if dicho['role']!='system':
            conversacion+=dicho['role']+": "+dicho['content']+"\n"
    
    return conversacion,archivo_salida_audio


tematicas=list(perfiles.keys())  

with gr.Blocks() as ui:
    entradas_usario=[gr.Audio(source="microphone",type="filepath"),gr.Dropdown(
                tematicas, label="Enfocado a",value="Asistente")]#gr.Dropdown(choices=options, label="Selecciona una opción")]
    #entradas_usario=[gr.Audio(source="microphone",type="filepath"),"Asistente"]
    
    print(entradas_usario[1])

    print(perfiles)
    print(entradas_usario)

    print("/n 0")
    print(mensajes)

    text_output = gr.Textbox(label="Transcripció de la Conversación")
    audio_output = gr.Audio()

    btn = gr.Button("Ejecutar")
    btn.click(fn=transcripcion, inputs=entradas_usario, outputs=[text_output , audio_output])
  

    #ui   = gr.Interface(fn=transcripcion,inputs=entradas_usario,outputs="text")
ui.launch()