import gradio as gr
from modelo import BuscadorCarreras
import os

# Configuración
RUTA_CSV = 'data.csv'
modelo = BuscadorCarreras(RUTA_CSV)

def clasificar_carrera(texto):
    resultados = modelo.buscar_carreras(texto)
   
    if isinstance(resultados, str):
        return resultados  # Mensaje de no coincidencias
    else:
        output = ""
        for i, (carrera, puntaje) in enumerate(resultados, 1):
            output += f"{i}. {carrera} (Score: {puntaje:.2f})\n"
        return output.strip()

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

# Configuración para Azure App Service
app = interfaz.app

if __name__ == "__main__":
    # Obtener el puerto de las variables de entorno o usar 8000 por defecto
port = int(os.environ.get("PORT", 8000))
interfaz.launch(server_name="0.0.0.0", server_port=port)
