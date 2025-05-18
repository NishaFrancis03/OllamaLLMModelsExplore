from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ollama import chat, ChatResponse

# Initialize the FastAPI app
app = FastAPI()


# Serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def get_chatbot_html():
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


# Define a request model to handle user input
class Message(BaseModel):
    user_input: str


# Route to get a response from the model
@app.post("/chat/")
async def chat_route(message: Message):
    user_input = message.user_input

    # Call the Ollama model for a response
    response: ChatResponse = chat(model='llama3.2', messages=[{
        'role': 'user',
        'content': user_input,
    }])

    # Extracting the response message content
    bot_message = response.message.content

    return {"response": bot_message}
