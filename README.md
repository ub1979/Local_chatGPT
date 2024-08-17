# Local_chatGPT

This project implements a ChatGPT-style chat interface using Gradio and the Ollama library. It provides a web-based interface for interacting with various large language models (LLMs) through Ollama, featuring real-time streaming responses and dynamic model selection.

## Features

- Web-based chat interface powered by Gradio
- Integration with Ollama for access to multiple LLM models
- Dynamic model selection from available Ollama models on the system
- Real-time streaming of AI responses
- Adjustable temperature parameter for response generation
- Customizable system prompt to guide the AI's behavior

## Requirements

- Python 3.7+
- gradio
- ollama

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ollama-gradio-chat.git
   cd ollama-gradio-chat
   ```

2. Install the required Python packages:
   ```
   pip install gradio ollama
   ```

3. Ensure you have Ollama installed and running on your system with at least one model available.

## Usage

1. Run the script:
   ```
   python chat_interface.py
   ```

2. Open your web browser and navigate to the URL provided in the console output (typically `http://127.0.0.1:7860`).

3. In the web interface:
   - Use the dropdown menu to select different LLM models available on your system through Ollama.
   - Type your message in the input box and press Enter to send.
   - Adjust the temperature slider to control the randomness of the AI's responses.
   - Modify the system prompt to change the AI's behavior or role.
   - Use the "Clear" button to reset the conversation.

## Customization

- The interface automatically detects and lists all available Ollama models on your system.
- Adjust the temperature range or default value by modifying the `gr.Slider()` parameters in the code.
- Customize the default system prompt by changing the `value` parameter in the `gr.Textbox()` for `system_prompt`.

## Contributing

Contributions to improve the chat interface or extend its functionality are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

