import gradio as gr
from modelo import BuscadorCarreras

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

# Configuración de la interfaz
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

# Configuración especial para Azure
app = interfaz.app

# Esto es necesario para que Azure lo reconozca como una aplicación WSGI
def get_app():
    return app

