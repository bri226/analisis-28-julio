import fitz  # PyMuPDF
import difflib

# Función para extraer texto de un PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
    return text

# Rutas a los archivos PDF
pdf_path_1 = "docs/dinaboluarte/2023_transcripcion_literal.pdf"
pdf_path_2 = "docs/dinaboluarte/2023_transcripcion_ia.pdf"

# Extraer el texto de los PDFs
text1 = extract_text_from_pdf(pdf_path_1)
text2 = extract_text_from_pdf(pdf_path_2)

# Comparar los textos
diff = difflib.unified_diff(text1.splitlines(), text2.splitlines(), lineterm='')

# Mostrar las diferencias
for line in diff:
    print(line)

# Guardar las diferencias en un archivo
with open("diff_output.txt", "w") as f:
    for line in diff:
        f.write(line + '\n')

print("Las diferencias se han guardado en diff_output.txt")
