import gradio as gr

def saludar(nombre):
    return f"¡Hola, {nombre}! Bienvenido a tu app en Azure App Service"

with gr.Blocks() as app:
    gr.Markdown("# 🚀 Mi App con Gradio en Azure")
    gr.Markdown("Esta es una aplicación sencilla desplegada en Azure App Service usando Gradio")
    
    with gr.Row():
        nombre = gr.Textbox(label="¿Cómo te llamas?")
        saludo = gr.Textbox(label="Saludo")
    
    btn = gr.Button("Saludar")
    btn.click(fn=saludar, inputs=nombre, outputs=saludo)
    
    gr.Examples(
        ["Juan", "María", "Carlos"],
        inputs=nombre
    )

# Para Azure, necesitamos exponer la app como un objeto callable
demo = app

# Azure espera una variable llamada 'application' para el despliegue
application = demo.launch(server_name="0.0.0.0", server_port=8000)
