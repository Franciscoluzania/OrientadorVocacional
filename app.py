import gradio as gr

def saludar(nombre):
    return f"Hola {nombre}! (App en Azure sin Flask)"

app = gr.Interface(
    fn=saludar,
    inputs="text",
    outputs="text",
    title="App Gradio en Azure",
    description="Versión sin Flask para despliegue simple"
)

if __name__ == "__main__":
    # Este comando inicia el servidor en Azure
    app.launch(server_name="0.0.0.0", server_port=8000, share=False)

