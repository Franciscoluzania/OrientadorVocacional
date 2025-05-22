from flask import Flask, request, jsonify, redirect
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
def create_gradio_app():
    return gr.Interface(
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

# Ruta principal - ahora redirige directamente a Gradio
@app.route("/")
def home():
    return redirect("/gradio")

# Montar Gradio como una ruta de Flask
@app.route("/gradio")
def gradio_interface():
    return create_gradio_app().launch(server_name="0.0.0.0", server_port=8000)

# API REST
@app.route("/api/recomendar", methods=["POST"])
def api_recomendar():
    data = request.json
    texto = data.get("texto", "")
    return jsonify({"recomendaciones": clasificar_carrera(texto)})

# Configuración para Azure App Service
if __name__ == "__main__":
    # Para desarrollo local
    app.run()
else:
    # Para producción en Azure
    gradio_app = create_gradio_app()
    app = gr.mount_gradio_app(app, gradio_app, path="/gradio")

