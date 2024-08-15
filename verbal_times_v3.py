import pdfplumber
import spacy
import random

# Cargar el modelo de español
nlp = spacy.load('es_core_news_sm')

# Función para leer texto de un archivo PDF usando pdfplumber
def leer_pdf(file_path):
    texto = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()
    return texto

# Ruta al archivo PDF
# pdf_path = r"C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\Pedro Castillo - 2022.pdf"
pdf_path = r"C:\Users\Brillitt\Documents\GITHUB\audio_to_text\transcripcion\dinaboluarte\transcripcion_literal.pdf"

# Leer el texto del PDF
texto = leer_pdf(pdf_path)

# Procesar el texto
doc = nlp(texto)

# Listas para almacenar los verbos según el tiempo
pasado = []
presente = []
futuro = []

# Diccionarios para almacenar las oraciones según el tiempo
oraciones_pasado = []
oraciones_presente = []
oraciones_futuro = []

# Recorrer las oraciones y clasificar los verbos
for sent in doc.sents:
    for token in sent:
        if token.pos_ == 'VERB':
            if 'Tense=Past' in token.morph:
                pasado.append(token.text)
                oraciones_pasado.append(sent.text)
            elif 'Tense=Pres' in token.morph:
                presente.append(token.text)
                oraciones_presente.append(sent.text)
            elif 'Tense=Fut' in token.morph:
                futuro.append(token.text)
                oraciones_futuro.append(sent.text)

# Seleccionar 10 oraciones aleatorias de cada lista
oraciones_pasado = random.sample(oraciones_pasado, min(10, len(oraciones_pasado)))
oraciones_presente = random.sample(oraciones_presente, min(10, len(oraciones_presente)))
oraciones_futuro = random.sample(oraciones_futuro, min(10, len(oraciones_futuro)))

# total = len(pasado) + len(presente) + len(futuro)
# print(f"Total de verbos: {total}")
# print("Porcentaje de verbos en pasado: {:.2f}%".format(len(pasado) / total * 100))
# print("Porcentaje de verbos en presente: {:.2f}%".format(len(presente) / total * 100))
# print("Porcentaje de verbos en futuro: {:.2f}%".format(len(futuro) / total * 100))

print("\nOraciones con verbos en pasado:")
for oracion in oraciones_pasado:
    print(oracion)

print("\nOraciones con verbos en presente:")
for oracion in oraciones_presente:
    print(oracion)

print("\nOraciones con verbos en futuro:")
for oracion in oraciones_futuro:
    print(oracion)
