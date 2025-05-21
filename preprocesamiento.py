import re
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import nltk
from unidecode import unidecode

nltk.download('stopwords')

def limpiar_palabras_clave(texto, idioma='spanish'):
    if not isinstance(texto, str):
        return []
    
    # Normalizar texto (quitar acentos, convertir a minúsculas)
    texto = unidecode(texto.lower())
    
    # Eliminar caracteres especiales y números
    texto = re.sub(r'[^a-zA-Záéíóúñ\s]', '', texto)
    

    palabras = re.findall(r'\b\w+\b', texto)
    
   
    stop_words = set(stopwords.words(idioma))
    stemmer = SnowballStemmer(idioma)
    
    palabras_limpias = []
    for palabra in palabras:
        if palabra not in stop_words and len(palabra) > 2:
            try:
                palabra_stem = stemmer.stem(palabra)
                palabras_limpias.append(palabra_stem)
            except:
                continue
    
    return palabras_limpias