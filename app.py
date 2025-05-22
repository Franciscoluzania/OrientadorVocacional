from flask import Flask, request, jsonify
import gradio as gr
from modelo import BuscadorCarreras

# Inicializar Flask
app = Flask(__name__)

# Configuración del modelo
RUTA_CSV = 'data.csv'
modelo = BuscadorCarreras(RUTA_CSV)

# Función principal de recomendación
def clasificar_carrera(texto):
    resultados = modelo.buscar_carreras(texto)
    if isinstance(resultados, str):
        return resultados
    else:
        output = ""
        for i, (carrera, puntaje) in enumerate(resultados, 1):
            output += f"{i}. {carrera} (Score: {puntaje:.2f})\n"
        return output.strip()

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

# Montar Gradio dentro de la app Flask
gradio_app = gr.mount_app(app, interfaz, path="/gradio")

# Ruta principal
@app.route("/")
def home():
    return "Bienvenido al Orientador de Carreras. Accede a <a href='/gradio'>/gradio</a> para la interfaz interactiva."

# API REST
@app.route("/api/recomendar", methods=["POST"])
def api_recomendar():
    data = request.json
    texto = data.get("texto", "")
    return jsonify({"recomendaciones": clasificar_carrera(texto)})

# Ejecutar la app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

