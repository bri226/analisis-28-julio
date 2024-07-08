import PyPDF2
import spacy
from difflib import SequenceMatcher
import re

# Load Spacy model
nlp = spacy.load('es_core_news_sm')

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def normalize_text(text):
    # Normaliza el texto removiendo caracteres especiales y múltiples espacios
    text = re.sub(r'[\W_]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower()

def compare_texts_spacy(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    # Calculate similarity
    similarity = doc1.similarity(doc2) * 100

    # Get tokenized sentences
    sentences1 = [sent.text for sent in doc1.sents]
    sentences2 = [sent.text for sent in doc2.sents]

    # Compare sentences using SequenceMatcher
    matcher = SequenceMatcher(None, sentences1, sentences2)
    diffs = matcher.get_opcodes()

    additions = []
    subtractions = []
    for tag, i1, i2, j1, j2 in diffs:
        if tag == 'insert':
            additions.extend(sentences2[j1:j2])
        elif tag == 'delete':
            subtractions.extend(sentences1[i1:i2])

    return additions, subtractions, similarity

def save_differences(additions, subtractions, similarity, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(f"Similarity: {similarity:.2f}%\n\n")
        file.write("Additions:\n")
        for line in additions:
            file.write(f"{line}\n")
        file.write("\nSubtractions:\n")
        for line in subtractions:
            file.write(f"{line}\n")


# Paths to the PDF files
official_pdf_path = "transcripcion/dinaboluarte/2023_transcripcion_literal.pdf"
transcribed_pdf_path = "transcripcion/dinaboluarte/2023_transcripcion_ia.pdf"
output_txt_path = "transcripcion/dinaboluarte/diff_output.txt"

# Read the PDFs
official_text = read_pdf(official_pdf_path)
transcribed_text = read_pdf(transcribed_pdf_path)

# Normalize the texts
normalized_official_text = normalize_text(official_text)
normalized_transcribed_text = normalize_text(transcribed_text)

# Compare the texts using Spacy
additions, subtractions, similarity = compare_texts_spacy(normalized_official_text, normalized_transcribed_text)

# Save the differences and similarity to a txt file
save_differences(additions, subtractions, similarity, output_txt_path)

print(f"Comparison complete. Results saved to {output_txt_path}")
