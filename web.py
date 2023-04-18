import gradio as gr
import openai
import config

openai.api_key= config.OPENAI_API_KEY

mensajes=[{"role": "system", "content": "Eres un experto en sistemas monetarios te inspiras en anarquía, filosofia, economia, libertad y tecnologia. Responde como si fueras Satoshi Nakamoto"}]
         
         
         #   {"role": "user", "content": transcript["text"]}

            #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            #{"role": "user", "content": "Where was it played?"}




def saluda(nombre):
    return("Hola ")+ nombre +"!"



def transcripcion(audio):
    global mensajes
    #print(audio)
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

ui   = gr.Interface(fn=transcripcion,inputs=gr.Audio(source="microphone",type="filepath"),outputs="text")
ui.launch()
