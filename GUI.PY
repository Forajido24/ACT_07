from tkinter import *
from tkinter import filedialog
#Aqui te ayuda para encontrar el archivo, para que lo puedas seleccionar,
#se abre una ventana donde esta solo clasificado para archivos tipo txt

def leer():
    global filename
    filetypes = [('Archivos TXT', '*.txt')]
    filename = filedialog.askopenfilename(filetypes=filetypes)
    
    if filename:
        try:
            #ESTO ESPECIFICA QUE EL R, ES SOLO PARA LEER LOS DATOS DEL ARCHVIO SIN MODIFICARLO, Y EL UTF-8 ES PARA QUE PUEDA LEER UNA GRAN VARIEDAD DE CARACTERES
            #LO ESPECIFIQUE PORQUE NO ME DEJABA LEER EL ARCHIVO DEL PROFE
            with open(filename, 'r', encoding='utf-8') as file:
                contenido = file.read()
                conteo(contenido)
                #ESTO SE PONE POR SI HAY ALGUN ERROR EN LA CODIFICACIÓN DE LA CANTIDAD DE LETRAS REPETIDS
        except UnicodeDecodeError as e:
            print(f"Error al decodificar el archivo: {e}")

#CREO QUE UNA VARIABLE GLOBAL DONDE GUARDO EN UN DICCIOANRIO LOS DATOS DE REPETICONES DEL ARCHVIO TXT
#ESTO LO HICE PARA QUE SEA MÁS FACIL UTILIZAR ESTA VARIABLE EN FUNCIONES PARA MANIPULAR
contador_letras = {}

def conteo(letras):
    global contador_letras#AQUI MARCO LA VARIABLE COMO GLOBAL, ESTO SIGNIFICA QUE SI MODIFICAS LOS VALORES
    #EN ESTA FUNCIÓN, Y LA TIENES O LA LLAMAS EN OTRA FUNCIÓN, ESTA SERÁ EXACTAMENTE LA MISMA
    
    #AHOAR BIEN, EN LA LINEA DE ABAJO HACE ALGO CURIOSO, DETECTA LA LETRA Y EN EL ARCHIVO, SI ESTA EN EL DICIIONARIO, LE SUMA UNO
    #Si no se encuentra, este se guarda como nuevo valor
    for letra in letras:
        if letra in contador_letras:
            contador_letras[letra] += 1
        else:
            contador_letras[letra] = 1
    print(contador_letras)
    #Aquí solo va insertra en el cuadro de texto, los valores que almacenó el diccioanrio
    CuadroTexto.insert(END,"El resumen de las letras son:\n")
    for clave,valor in contador_letras.items():
        CuadroTexto.insert(END,  f"{clave}: {valor}\n")


Raiz = Tk()
Raiz.title('Actividad 07')
Raiz.config(width=700, height=600)

MFrame = Frame(Raiz)
MFrame.config(width=500, height=200, bg="#757575")
MFrame.pack()

BotonLeer=Button(MFrame, text="Examinar",command=leer,bg="#0B656C",fg="#FFFFFF")
BotonLeer.place(x=10,y=75, width=115,height=25)

BotonComprimir=Button(MFrame, text="Comprimir",bg="#0B476C",fg="#FFFFFF")
BotonComprimir.place(x=10,y=105, width=115,height=25)

BotonDescomprimir=Button(MFrame, text="Descomprimir",bg="#0B476C",fg="#FFFFFF")
BotonDescomprimir.place(x=10,y=135, width=115,height=25)

CuadroTexto=Text(MFrame)
CuadroTexto.place(x=130,y=45,width=350,height=145)


BotonComprimir = Button(MFrame, text="Comprimir", command="AQUI PON LA FUNCIÓN DE COMPRIMIR", bg="#0B476C", fg="#FFFFFF")
BotonComprimir.place(x=10, y=105, width=115, height=25)

BotonDescomprimir = Button(MFrame, text="Descomprimir", command="AQUI PON LA FUNCIÓN DE DESCOMPRIMIR", bg="#0B476C", fg="#FFFFFF")
BotonDescomprimir.place(x=10, y=135, width=115, height=25)

Raiz.mainloop()
