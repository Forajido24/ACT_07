from tkinter import *
from tkinter import filedialog
import os
import heapq

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def leer():
    global filename
    filetypes = [('Archivos TXT', '*.txt')]
    filename = filedialog.askopenfilename(filetypes=filetypes)
    
    if filename:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                contenido = file.read()
                conteo(contenido)
        except UnicodeDecodeError as e:
            print(f"Error al decodificar el archivo: {e}")

contador_letras = {}

def conteo(letras):
    global contador_letras
    for letra in letras:
        if letra in contador_letras:
            contador_letras[letra] += 1
        else:
            contador_letras[letra] = 1
    print(contador_letras)
    CuadroTexto.insert(END,"El resumen de las letras son:\n")
    for clave,valor in contador_letras.items():
        CuadroTexto.insert(END,  f"{clave}: {valor}\n")

def construir_arbol_huffman(contador_letras):
    heap = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in contador_letras.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        izquierda = heapq.heappop(heap)
        derecha = heapq.heappop(heap)
        padre = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        padre.izquierda = izquierda
        padre.derecha = derecha
        heapq.heappush(heap, padre)
    return heap[0]

def asignar_codigos_huffman(arbol, prefijo='', codigos={}):
    if arbol.caracter is not None:
        codigos[arbol.caracter] = prefijo
    else:
        asignar_codigos_huffman(arbol.izquierda, prefijo + '0', codigos)
        asignar_codigos_huffman(arbol.derecha, prefijo + '1', codigos)
    return codigos

def comprimir_archivo(original_filename, codigos):
    comprimido_filename = os.path.splitext(original_filename)[0] + '_comprimido.bin'
    with open(original_filename, 'r', encoding='utf-8') as original, open(comprimido_filename, 'wb') as comprimido:
        contenido = original.read()
        bits = ''.join(codigos[caracter] for caracter in contenido)
        padding = 8 - len(bits) % 8
        bits += padding * '0'  # Añadir bits de relleno
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            comprimido.write(bytes([int(byte, 2)]))
        comprimido.write(bytes([padding]))  # Guardar el número de bits de relleno al final
    return comprimido_filename

def descomprimir_archivo(comprimido_filename, arbol_huffman):
    descomprimido_filename = os.path.splitext(comprimido_filename)[0] + '_descomprimido.txt'
    with open(comprimido_filename, 'rb') as comprimido, open(descomprimido_filename, 'w', encoding='utf-8') as descomprimido:
        bits = ''
        while True:
            byte = comprimido.read(1)
            if not byte:
                break
            bits += f'{ord(byte):08b}'
        padding = bits[-8:]
        bits = bits[:-int(padding, 2)]  # Eliminar bits de relleno
        nodo_actual = arbol_huffman
        for bit in bits:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha
            if nodo_actual.caracter is not None:
                descomprimido.write(nodo_actual.caracter)
                nodo_actual = arbol_huffman  # Reiniciar para buscar el siguiente caracter
    return descomprimido_filename

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

def comprimir():
    global contador_letras, filename
    arbol_huffman = construir_arbol_huffman(contador_letras)
    codigos_huffman = asignar_codigos_huffman(arbol_huffman)
    comprimido_filename = comprimir_archivo(filename, codigos_huffman)
    print(f"Archivo comprimido: {comprimido_filename}")

def descomprimir():
    filetypes = [('Archivos Binarios', '*.bin')]
    comprimido_filename = filedialog.askopenfilename(filetypes=filetypes)
    if comprimido_filename:
        arbol_huffman = construir_arbol_huffman(contador_letras)
        descomprimido_filename = descomprimir_archivo(comprimido_filename, arbol_huffman)
        print(f"Archivo descomprimido: {descomprimido_filename}")

BotonComprimir = Button(MFrame, text="Comprimir", command=comprimir, bg="#0B476C", fg="#FFFFFF")
BotonComprimir.place(x=10, y=105, width=115, height=25)

BotonDescomprimir = Button(MFrame, text="Descomprimir", command=descomprimir, bg="#0B476C", fg="#FFFFFF")
BotonDescomprimir.place(x=10, y=135, width=115, height=25)

Raiz.mainloop()
