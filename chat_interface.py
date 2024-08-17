# ==============================================================
# Importing the libraries
# ==============================================================
import gradio as gr  # Import Gradio for creating the web interface
from ollama import Client  # Import Ollama Client for interacting with the LLM model
import httpx  # Import httpx for handling HTTP-related exceptions

# ==============================================================
# Initialize Ollama client and fetch available models
# ==============================================================
client = Client()  # Create an instance of the Ollama client

def get_available_models():
    """Fetch and return a list of available models from Ollama."""
    try:
        models = client.list()
        return [model['name'] for model in models['models']]
    except httpx.ConnectTimeout:
        print("Warning: Unable to connect to Ollama server. Please ensure it's running.")
        return ["Ollama server not available"]
    except Exception as e:
        print(f"An error occurred while fetching models: {str(e)}")
        return ["Error fetching models"]

available_models = get_available_models()

# ==============================================================
# Define the chat function with streaming, model selection, and error handling
# ==============================================================
def chat(message, history, system_prompt, temperature, selected_model):
    """
    Process the user's message and generate a streaming response using the selected LLM model.

    :param message: User's input message
    :param history: Chat history
    :param system_prompt: System prompt to guide the model's behavior
    :param temperature: Temperature parameter for response generation
    :param selected_model: The name of the selected Ollama model
    :yield: Updated history with the new message and streaming response
    """
    # Check if Ollama server is available
    if selected_model == "Ollama server not available" or selected_model == "Error fetching models":
        error_message = "Unable to connect to Ollama server. Please ensure it's running and try again."
        history.append((message, error_message))
        yield history
        return

    # Prepare the full prompt including system prompt and chat history
    full_prompt = f"{system_prompt}\n\n"  # Start with the system prompt
    for human, assistant in history:  # Add the chat history
        full_prompt += f"Human: {human}\nAssistant: {assistant}\n"
    full_prompt += f"Human: {message}\nAssistant:"  # Add the current message

    # Add the user's message to the history
    history.append((message, ""))
    streaming_history = history.copy()

    try:
        # Generate a streaming response using Ollama with the selected model
        stream = client.chat(model=selected_model,  # Use the selected model
                             messages=[{'role': 'user', 'content': full_prompt}],  # Provide the full prompt
                             options={'temperature': temperature},  # Set the temperature
                             stream=True)  # Enable streaming

        # Stream the response
        assistant_response = ""
        for chunk in stream:
            assistant_response += chunk['message']['content']
            streaming_history[-1] = (message, assistant_response)
            yield streaming_history

        # Update the final history with the complete response
        history[-1] = (message, assistant_response)

    except httpx.ConnectTimeout:
        error_message = "Connection to Ollama server timed out. Please check your connection and try again."
        history[-1] = (message, error_message)
        yield history
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        history[-1] = (message, error_message)
        yield history

# ==============================================================
# Set up the Gradio interface
# ==============================================================
with gr.Blocks() as demo:
    # Create a Markdown component for the title
    gr.Markdown("# Ollama-powered Chat Interface with Model Selection")

    # Create a Chatbot component for the main chat interface
    chatbot = gr.Chatbot()

    # Create a Textbox component for user input
    msg = gr.Textbox(label="Type your message here")

    # Create a Dropdown component for model selection
    model_dropdown = gr.Dropdown(choices=available_models, value=available_models[0] if available_models else None, label="Select Model")

    # Create a Slider component for temperature adjustment
    temperature = gr.Slider(minimum=0.1, maximum=2.0, value=0.7, label="Temperature")

    # Create a Textbox component for the system prompt
    system_prompt = gr.Textbox(
        label="System Prompt",
        value="You are a helpful AI assistant. Respond concisely and accurately.")

    # Create a Button component for clearing the chat
    clear = gr.Button("Clear")

    # Set up the chat function with the necessary inputs
    msg.submit(chat,
               inputs=[msg, chatbot, system_prompt, temperature, model_dropdown],
               outputs=[chatbot],
               postprocess=False)

    # Set up the clear button functionality
    clear.click(lambda: None, None, chatbot, queue=False)

# ==============================================================
# Launch the Gradio interface
# ==============================================================
if __name__ == "__main__":
    demo.launch()  # Launch the Gradio interface