import PyPDF2
import pandas as pd

# Función para extraer texto de un PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Lista de regiones fuera de Lima
regiones = ["Amazonas", "Áncash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", "Cusco", 
            "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", "Loreto", "Madre de Dios", 
            "Moquegua", "Pasco", "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali"]

# Función para contar menciones de regiones en un texto
def count_region_mentions(text, regiones):
    counts = {region: text.count(region) for region in regiones}
    return counts

# Leer y analizar cada discurso
files = {
    "Dina Boluarte": r"C:\Users\Brillitt\Downloads\Discursos presidenciales (Transcripcion Literal)\Dina Bolaurte.pdf",
    "Pedro Castillo": r"C:\Users\Brillitt\Downloads\Discursos presidenciales (Transcripcion Literal)\Pedro Castillo.pdf",
    "Martín Vizcarra": r"C:\Users\Brillitt\Downloads\Discursos presidenciales (Transcripcion Literal)\Martín Vizcarra.pdf",
    "PPK": r"C:\Users\Brillitt\Downloads\Discursos presidenciales (Transcripcion Literal)\PPK.pdf",
    "Ollanta Humala": r"C:\Users\Brillitt\Downloads\Discursos presidenciales (Transcripcion Literal)\Ollanta Humala.pdf"
}

# Almacenar resultados en un dataframe
results = []

for president, file_path in files.items():
    text = extract_text_from_pdf(file_path)
    counts = count_region_mentions(text, regiones)
    counts["Presidente"] = president
    results.append(counts)

df = pd.DataFrame(results)

print(df)

