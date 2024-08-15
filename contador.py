import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string
import unicodedata
import re

# Descargar las stop words en español
nltk.download('stopwords')

# Función para leer el PDF y extraer el texto
def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def count_words(text):
    # Convertir a minúsculas
    text = text.lower()
    
    # Eliminar puntuación y caracteres especiales, excepto letras y números
    text = re.sub(r'[^\w\s]', '', text)
    
    # Dividir el texto en palabras
    words = text.split()
    
    # Eliminar stop words
    stop_words = set(stopwords.words('spanish'))
    words = [word for word in words if word not in stop_words]
    
    # Contar la frecuencia de las palabras
    word_counts = Counter(words)
    
    return word_counts


# Ruta al archivo PDF
pdf_path = r'C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\Ollanta Humala -2012.pdf'

# Leer el PDF
pdf_text = read_pdf(pdf_path)
# print(pdf_text[:1000])
# Contar las palabras
word_counts = count_words(pdf_text)

# Mostrar las palabras más comunes
most_common_words = word_counts.most_common(10)  # Cambiar el número para ver más o menos palabras
words = ''
for word, count in most_common_words:
    words = words + word + ' (' + str(count) + '), '
    # print(f'{word} ({count})')

print(words)