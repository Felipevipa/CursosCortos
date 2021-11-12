##Este aplicativo funciona pero el contexto es muy grande y se demora en responder##



#import wikipedia




##########################################################

##############Seleccion de modelo ###########################################
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import os
import time
############################################################################
import pyttsx3
from pyttsx3 import engine

pv = 0
model = ""
tokenizer = ""
contexto = ""
nlp = ""

def sonido(son):
    engine = pyttsx3.init()
    voice_id = 'spanish-latin-am'
    engine.setProperty('voice',voice_id)
    rate = engine.getProperty('rate')
    engine.say(str(son))
    engine.runAndWait()
    engine.stop()

def cargar():
      global pv, model, tokenizer, contexto, nlp
      if pv == 0:
        inicio = time.time()
        pregunta=""
        the_model = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
        tokenizer = AutoTokenizer.from_pretrained(the_model, do_lower_case=False)
        model = AutoModelForQuestionAnswering.from_pretrained(the_model)

        final = time.time()
        print("Tiempo para importar el modelo: " + str(final - inicio) + " segundos\n")


        inicio = time.time()
        
        # contexto='Conjunto de elementos físicos o materiales que constituyen una computadora o un sistema informático.'
        final = time.time()
        print("Tiempo para leer el archivo: " + str(final - inicio) + " segundos")
        encode = tokenizer.encode_plus(pregunta, contexto, return_tensors='pt')
        input_ids = encode['input_ids'].tolist()
        tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
        for id, token in zip(input_ids[0], tokens):
        #print('{:<12} {:>6}'.format(token, id))
            pass
            # print('')
        pv = 1

        

def pregunta_respuesta_escrito(pregunta):
    with open(os.getcwd() + "\\nombre\\nuevo.txt", "r") as archivo:
            contexto = str(archivo.read().splitlines())
            archivo.close()
    # Ejemplo de inferencia (pregunta-respuesta)
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

    inicio = time.time()

    salida = nlp({'question':pregunta, 'context':contexto})
    final = time.time()
    print("Tiempo para responder la pregunta: " + str(final - inicio) + " segundos\n")
    #sonido(salida['answer'])
    #return salida['answer']

    continuar = pregunta!=''

    if continuar:
        salida = nlp({'question':pregunta, 'context':contexto})
        print('\nRespuesta:')
        print('-----------------')
        print(salida['answer'])
        sonido(salida['answer'])
    return salida['answer']

