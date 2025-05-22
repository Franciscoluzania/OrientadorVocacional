from fastapi import FastAPI
import gradio as gr
from modelo import BuscadorCarreras
import os

# Cargar el modelo
RUTA_CSV = os.path.join(os.path.dirname(__file__), 'data.csv')
modelo = BuscadorCarreras(RUTA_CSV)

# Función de predicción
def clasificar_carrera(texto):
    try:
        resultados = modelo.buscar_carreras(texto)
        if isinstance(resultados, str):
            return resultados
        return "\n".join([
            f"{i+1}. {carrera} (Score: {puntaje:.2f})"
            for i, (carrera, puntaje) in enumerate(resultados)
        ])
    except Exception as e:
        return f"Error al procesar la solicitud: {str(e)}"

# Crear interfaz Gradio
interfaz = gr.Interface(
    fn=clasificar_carrera,
    inputs=gr.Textbox(
        label="Describe tus intereses, habilidades o lo que te gustaría estudiar:",
        placeholder="Ej: Me gusta resolver problemas matemáticos y trabajar con tecnología..."
    ),
    outputs=gr.Textbox(label="Carreras recomendadas"),
    examples=[
        ["Disfruto programar y crear soluciones tecnológicas innovadoras"],
        ["Me apasiona cuidar animales y entender los ecosistemas naturales"],
        ["Soy bueno con los números y me gusta analizar datos"]
    ],
    title="Orientador de Carreras",
    description="💡 Describe tus intereses, habilidades o aspiraciones profesionales para recibir recomendaciones personalizadas"
)

# Crear app FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "La aplicación está funcionando. Visita /gradio para la interfaz"}

# Montar Gradio en FastAPI
app = gr.mount_gradio_app(app, interfaz, path="/gradio")

# Para Azure Web App
application = app
