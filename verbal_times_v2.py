import pdfplumber
import spacy

# Cargar el modelo de español
nlp = spacy.load('es_core_news_sm')

# Función para leer texto de un archivo PDF usando pdfplumber
def leer_pdf(file_path):
    texto = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()
        # print (texto[:1000])
    return texto

# Ruta al archivo PDF
pdf_path = r"C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\Ollanta Humala -2012.pdf"

# Leer el texto del PDF
texto = leer_pdf(pdf_path)

# Procesar el texto
doc = nlp(texto)

# Listas para almacenar los verbos según el tiempo
pasado = []
presente = []
futuro = []

# Recorrer los tokens y clasificar los verbos
for token in doc:
    if token.pos_ == 'VERB':
        #print(token.text, token.tag_,token.morph)
        if  'Tense=Past' in token.morph:
            pasado.append(token.text)
        elif 'Tense=Pres' in token.morph:
            presente.append(token.text)
        elif 'Tense=Fut' in token.morph:
            futuro.append(token.text)

total = len(pasado) + len(presente) + len(futuro)
print(f"Total de verbos: {total}")
print("Porcentaje de verbos en pasado: {:.2f}%".format(len(pasado) / total * 100))
print("Porcentaje de verbos en presente: {:.2f}%".format(len(presente) / total * 100))
print("Porcentaje de verbos en futuro: {:.2f}%".format(len(futuro) / total * 100))

# Formatear e imprimir el resultado
def formatear_lista(titulo, lista):
    lista_unica = list(set(lista))
    return f"{titulo} ({len(lista_unica)} palabras): {', '.join(lista_unica)}"

print(formatear_lista("PASADO", pasado))
print(formatear_lista("PRESENTE", presente))
print(formatear_lista("FUTURO", futuro))

