# Gemini AI Chat

A desktop AI chat application built with Python, CustomTkinter, Tkinter, and the Google Gemini API.

## Features

- Gemini-powered conversational chat
- Clean desktop GUI built with CustomTkinter
- Light and dark themes
- New Chat functionality
- Markdown-style rendering for headings, lists, bold, italic, inline code, and code blocks
- Thinking/loading animation while Gemini responds
- Background thread for API responses so the UI remains responsive
- Conversation history during the current session

## Requirements

- Python 3.9+
- A Google Gemini API key

## Installation

Install the required Python packages:

```bash
pip install customtkinter google-genai
```

## API Key

The source code intentionally does **not** contain a real API key. The project uses the placeholder:

```python
GEMINI_API_KEY = "enter_your_api"
```

For security, never commit a real API key to a public GitHub repository. Before running the application, replace the placeholder locally with your own Gemini API key.

## Run

```bash
python gemini_ai_chat.py
```

## Project Structure

```text
gemini-ai-chat/
├── gemini_ai_chat.py
└── README.md
```

## Security

No real API credentials are included in this repository. Keep your API key private and do not publish it in source code, commits, screenshots, or logs.

## License

No license has been specified for this project yet.
