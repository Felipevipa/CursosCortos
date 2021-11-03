from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np


###############REGISTRO DE INFORMACION################

def registrar_usuario():
    usuario_info = usuario.get()  #informacion almacenada en usuario
    contra_info = contra.get()    #informacion almacenada en contra

    archivo = open(usuario_info, "w")        #se abre la informacion en modo escritura
    archivo.write(usuario_info + "\n")       #escribimos la informacion
    archivo.write(contra_info)
    archivo.close()


    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    Label(pantalla1, text = "Registro convencional exitoso", fg = "green", font = ("Calibri",11)).pack()

###########################FUNCION PARA ALMACENAR EL REGISTRO FACIAL###################################

def registro_facial():
    #captura del rostro
    cap = cv2.VideoCapture(0)
    while(True):
        ret,Frame = cap.read()
        cv2.imshow('Registro facial',Frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img+".jpg",Frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    Label(pantalla1, text = "Registro facial exitoso", fg = "green", font = ("calibri",11)).pack()

    ###########################DETECCION DE ROSTRO E IMPORTACION DE PIXELES###################

    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)


############################REGISTRO#################################

def registro():
    global usuario 
    global contra 
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla)
    pantalla1.title("registro")
    pantalla1.geometry("300x250")

    ######################creacion de entradas####################

    usuario = StringVar()
    contra = StringVar()

    Label(pantalla1, text = "Registro facial: debe de asignar un usuario:").pack()
    Label(pantalla1, text = "Registro tradicional: debe de asignar un usuario y contraseña:").pack()
    Label(pantalla1, text = "").pack()
    Label(pantalla1, text = "Usuario * ").pack()
    usuario_entrada = Entry(pantalla1, textvariable = usuario)
    usuario_entrada.pack()
    Label(pantalla1, text = "Contraseña * ").pack()
    contra_entrada = Entry(pantalla1, textvariable = contra)
    contra_entrada.pack()
    Label(pantalla1, text = "").pack()
    Button(pantalla1, text = "Registro tradicional", width = 15, height = 1, command = registrar_usuario).pack()

    #########################creacion boton para registro facial##########################
    Label(pantalla1, text = "").pack()
    Button(pantalla1, text = "Registro facial", width = 15, height = 1, command = registro_facial).pack()


##############################FUNCION PARA EL LOGIN FACIAL#############################

def login_facial():
    cap = cv2.VideoCapture(0)
    while(True):
        ret,frame = cap.read()
        cv2.imshow('Login facial',frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_login = verificacion_usuario.get()
    cv2.imwrite(usuario_login+"LOG.jpg",frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

#####################FUNCION PARA GUARDAR EL ROSTRO################################

    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

##############################DETECCION DEL ROSTRO######################################

    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    ########################FUNCION PARA COMPARAR LOS ROSTROS######################
    def orb_sim (img1,img2):
        orb = cv2.ORB_create()

        kpa, descr_a = orb.detectAndCompute(img1, None)
        kpa, descr_b = orb.detectAndCompute(img2, None)

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

        matches = comp.match(descr_a, descr_b)

        regiones_similares = [i for i in matches if i.distance < 70]
        if len(matches)==0:
            return 0
        return len(regiones_similares)/len(matches)


##############################IMPORTAMOS LAS IMAGENES Y LLAMAMOS LA FUNCION COMPARACION##############
    im_archivos = os.listdir()
    if usuario_login+".jpg" in im_archivos:
        rostro_reg = cv2.imread(usuario_login+".jpg",0)
        rostro_log = cv2.imread(usuario_login+"LOG.jpg",0)
        similitud= orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.9:
            Label(pantalla2, text = "Inicio de sesion exitoso", fg = "Green", font = ("Calibri",11)).pack()
            print("Bienvenido al sistema usuario: ",usuario_login)
            print("Compatibilidad con la foto de registro: ",similitud)
        else:
            print("Rostro incorrecto, verifique su usuario")
            print("Compatibilidad con la foto de registro: ",similitud)
            Label(pantalla2, text ="Incompatibilidad de rostros", fg = "red", font = ("Calibri",11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text ="Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()



############################FUNCION ASIGNADA AL BOTON LOGIN##############################

def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2

    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("300x250")
    Label(pantalla2, text = "Login facial: debe asignar un usuario").pack()
    Label(pantalla2, text = "Login tradicional: debe asignar usuario y contraseña").pack()
    Label(pantalla2, text = "").pack()

    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()

####################################INGRESO DE DATOS####################################

    Label(pantalla2, text = "Usuario * ").pack()
    usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
    usuario_entrada2.pack()
    Label(pantalla2, text ="Contraseña * ").pack()
    contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
    contra_entrada2.pack()
    Label(pantalla2, text = "").pack()
   # Button(pantalla2, text = "Inicio de sesion tradicional", width = 20, height = 1, command = verificacion_login).pack()

####################BOTON PARA LOGIN FACIAL#########################

    Label(pantalla2, text = "Usuario * ").pack()
    Button(pantalla2, text = "Inicio de sesion facial", width = 20, height = 1, command = login_facial).pack()


###################funcion de la pantalla principal##################

def pantalla_principal():
    global pantalla
    pantalla=Tk()
    pantalla.geometry("300x250")
    pantalla.title("Aprende e ingenia")
    Label(text = "Login Inteligente", bg = "gray", width = "300",height = "2", font = ("verdana", 13)).pack()


######################Creacion de botones#############################

    Label(text = "").pack()
    Button(text = "Iniciar sesion", height = "2", width = "30", command = login).pack()
    Label(text = "").pack()
    Button(text = "Registro", height = "2", width = "30", command = registro).pack()

    pantalla.mainloop()

pantalla_principal()
