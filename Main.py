from fastapi import FastAPI
from dotenv import load_dotenv
from PulseAI.GenerateResponse import generateResponse
from PulseAI.GetChatMessages import getChatMessages
from PulseAI.SaveMessagesToDB import saveMessagesToDB
from starlette.middleware.cors import CORSMiddleware
from LoggerConfig import logger
from Properties.AddProperty import router as AddPropertyRouter
from PulseAI.CreateChat import router as CreateChatRouter
from Properties.GetProperties import router as GetPropertiesRouter


load_dotenv()
app = FastAPI()
app.include_router(CreateChatRouter)
app.include_router(AddPropertyRouter)
app.include_router(GetPropertiesRouter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getMessages/{chat_id}")
def get_chat_messages(chat_id: int):
    messages = getChatMessages(chat_id).to_dict(orient='records')
    logger.info("Messages for Chat %s: %s" % (str(chat_id), messages))
    if not messages:
        logger.warning("Chat %s has no messages" % str(chat_id))
        return []
    return messages


@app.get("/generateResponse/{chat_id}/{prompt}", response_model=dict[str, str])
def generate_response(prompt: str, chat_id: int):
    messages = getChatMessages(chat_id)
    if messages.to_dict(orient='records'):
        messages = messages.drop(columns=['_id', 'createdAt'])
        messages = messages.rename(columns={'user': 'role', 'text': 'content'})
    saveMessagesToDB(chat_id, prompt, "user")
    aiResponse = generateResponse(prompt, messages.to_dict(orient='records'))
    logger.info("Responses for Chat %s: %s" % (str(chat_id), aiResponse))
    saveMessagesToDB(chat_id, aiResponse['text'], "assistant")
    return aiResponse


