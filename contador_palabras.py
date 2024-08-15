import PyPDF2
from collections import Counter
import pdfplumber

def leer_pdf(file_path):
    texto = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()
        # print (texto[:1000])
    return texto

# Example usage
# pdf_path = r'C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\PPK - 2017.pdf'
# pdf_path = r'C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\Ollanta Humala -2012.pdf'
pdf_path = r'C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\Dina Boluarte - 2023 (formateado).pdf'
# pdf_path = r'C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\PPK - 2017 (formateado).pdf'
# pdf_path = r'C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\Pedro Castillo - 2022 (formateado).pdf'
# pdf_path = r'C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\Martín Vizcarra - 2019 (formateado).pdf'
# pdf_path = r'C:\Users\Brillitt\Downloads\Discurso Dina Boluarte\Ollanta Humala -2012 (formateado).pdf'



word_count = leer_pdf(pdf_path)

# Print the most common words
print("Total de palabras: ",(len(word_count.split())))