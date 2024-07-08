import pdfplumber
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize

# Descargar los recursos necesarios para la tokenización de oraciones
nltk.download('punkt')

# Extraer texto del PDF usando pdfplumber
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Dividir texto en oraciones
def split_text_into_sentences(text):
    sentences = sent_tokenize(text)
    return sentences

# Análisis de sentimientos para cada oración
def analyze_sentiments(sentences):
    classifier = pipeline('sentiment-analysis', model='j-hartmann/emotion-english-distilroberta-base')
    all_results = []
    for i, sentence in enumerate(sentences):
        # print(f"Analyzing sentence {i+1}/{len(sentences)}...")
        results = classifier(sentence)
        for result in results:
            result['sentence'] = sentence  # Añadir la oración al resultado
        all_results.extend(results)
    return all_results

# Calcular porcentajes, ejemplos y contar palabras
def calculate_emotion_percentages_and_words(results):
    emotion_counts = {}
    emotion_examples = {}
    emotion_word_counts = {}

    for result in results:
        emotion = result['label']
        sentence = result['sentence']
        word_count = len(sentence.split())

        # Contar número de palabras por emoción
        if emotion in emotion_word_counts:
            emotion_word_counts[emotion] += word_count
        else:
            emotion_word_counts[emotion] = word_count

        # Contar número de ocurrencias por emoción
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1
        else:
            emotion_counts[emotion] = 1

        # Añadir ejemplos de oraciones clasificadas por emoción
        if emotion not in emotion_examples:
            emotion_examples[emotion] = []
        if len(emotion_examples[emotion]) < 10:  # Limitar a 10 ejemplos por emoción
            emotion_examples[emotion].append(sentence)

    total_words = sum(emotion_word_counts.values())
    total_emotions = sum(emotion_counts.values())
    emotion_percentages_by_words = {emotion: (word_count / total_words) * 100 for emotion, word_count in emotion_word_counts.items()}
    emotion_percentages_by_counts = {emotion: (count / total_emotions) * 100 for emotion, count in emotion_counts.items()}
    
    return emotion_percentages_by_words, emotion_percentages_by_counts, emotion_examples, emotion_word_counts

# Ruta al archivo PDF
pdf_path = r'C:\Users\Brillitt\Documents\GITHUB\audio_to_text\transcripcion\dinaboluarte\2023_transcripcion_literal_traduccion.pdf'
text = extract_text_from_pdf(pdf_path)
sentences = split_text_into_sentences(text)
results = analyze_sentiments(sentences)
emotion_percentages_by_words, emotion_percentages_by_counts, emotion_examples, emotion_word_counts = calculate_emotion_percentages_and_words(results)

# Imprimir porcentaje promedio de emociones basado en el número de palabras
print("\nAverage emotion percentages based on word count:")
for emotion, percentage in emotion_percentages_by_words.items():
    print(f"{emotion}: {percentage:.2f}%")

# Imprimir porcentaje promedio de emociones basado en el número de ocurrencias
print("\nAverage emotion percentages based on sentence count:")
for emotion, percentage in emotion_percentages_by_counts.items():
    print(f"{emotion}: {percentage:.2f}%")

# Imprimir número total de palabras por emoción
print("\nTotal word count by emotion:")
for emotion, count in emotion_word_counts.items():
    print(f"{emotion}: {count} words ({emotion_percentages_by_words[emotion]:.2f}%)")

# Imprimir ejemplos de oraciones clasificadas por cada emoción
print("\nExamples of sentences classified by emotion:")
for emotion, examples in emotion_examples.items():
    if(emotion == 'surprise'):
        print(f"\nEmotion: {emotion}")
        for example in examples:
            print(f"  - {example}")
