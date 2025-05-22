from flask import Flask, request, jsonify, redirect
import gradio as gr
from modelo import BuscadorCarreras

app = Flask(__name__)

# Configuración
RUTA_CSV = 'data.csv'
modelo = BuscadorCarreras(RUTA_CSV)

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

# Lanzar interfaz Gradio en un hilo separado
@app.before_first_request
def launch_gradio():
    import threading
    def run_gradio():
        interfaz.launch(server_name="0.0.0.0", server_port=7860, show_api=False)
    thread = threading.Thread(target=run_gradio)
    thread.daemon = True
    thread.start()

# Redirigir a la interfaz de Gradio
@app.route("/gradio")
def redireccionar_gradio():
    return redirect("http://localhost:7860")

# API endpoint alternativo
@app.route("/api/recomendar", methods=["POST"])
def api_recomendar():
    data = request.json
    texto = data.get("texto", "")
    return jsonify({"recomendaciones": clasificar_carrera(texto)})

@app.route("/")
def home():
    return "Bienvenido al Orientador de Carreras. Accede a /gradio para la interfaz interactiva."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

