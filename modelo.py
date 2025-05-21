import pickle
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocesamiento import limpiar_palabras_clave

class BuscadorCarreras:
    def __init__(self, ruta_csv=None):
        if ruta_csv:
            self.entrenar_modelo(ruta_csv)
    
    def entrenar_modelo(self, ruta_csv):
        """Entrena el modelo desde un CSV y guarda los componentes."""
        self.df = pd.read_csv(ruta_csv, usecols=['carrera', 'Palabras_clave'])
        self.df['texto_limpio'] = self.df['Palabras_clave'].apply(
            lambda x: ' '.join(limpiar_palabras_clave(str(x)))
        )
        
        # Codificar carreras
        self.le = LabelEncoder()
        self.df['carrera_encoded'] = self.le.fit_transform(self.df['carrera'])
        
        # Vectorización TF-IDF
        self.vectorizer = TfidfVectorizer(max_features=1000)
        X = self.vectorizer.fit_transform(self.df['texto_limpio'])
        y = self.df['carrera_encoded']
        
        # Modelo KNN
        self.model = KNeighborsClassifier(
            n_neighbors=5,
            weights='distance',
            metric='cosine'
        )
        self.model.fit(X, y)
    
    def guardar_modelo(self, ruta_archivo):
        """Guarda el modelo en un archivo .pkl usando pickle."""
        with open(ruta_archivo, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'model': self.model,
                'le': self.le
            }, f)
    
    @staticmethod
    def cargar_modelo(ruta_archivo):
        """Carga el modelo desde un archivo .pkl."""
        with open(ruta_archivo, 'rb') as f:
            componentes = pickle.load(f)
        
        # Crea una instancia sin entrenar
        buscador = BuscadorCarreras()
        buscador.vectorizer = componentes['vectorizer']
        buscador.model = componentes['model']
        buscador.le = componentes['le']
        return buscador
    
    def buscar_carreras(self, texto_usuario):
        """Predice carreras basadas en texto de entrada."""
        texto_limpio = ' '.join(limpiar_palabras_clave(str(texto_usuario)))
        texto_vectorizado = self.vectorizer.transform([texto_limpio])
        
        probas = self.model.predict_proba(texto_vectorizado)[0]
        carreras_probas = list(zip(self.le.classes_, probas))
        carreras_probas.sort(key=lambda x: x[1], reverse=True)
        
        resultados = []
        for carrera, prob in carreras_probas[:2]:  # Top 2
            if prob > 0.05:  # Umbral mínimo
                resultados.append((carrera, round(prob, 2)))
        
        return resultados if resultados else "No hay coincidencias."