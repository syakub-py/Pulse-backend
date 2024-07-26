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
from Properties.DeleteProperty import router as DeletePropertyRouter

load_dotenv()
app = FastAPI()
app.include_router(CreateChatRouter)
app.include_router(AddPropertyRouter)
app.include_router(GetPropertiesRouter)
app.include_router(DeletePropertyRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getMessages/{chat_id}")
def get_chat_messages(chat_id: int):
    try:
        messages = getChatMessages(chat_id).to_dict(orient='records')
        if not messages:
            logger.warning("Chat %s has no messages" % str(chat_id))
            return []
        return messages
    except Exception as e:
        logger.error("Failed to retrieve chat messages for chat %s: %s" % (str(chat_id), str(e)))
        return []


@app.get("/generateResponse/{chat_id}/{prompt}", response_model=dict[str, str])
def return_and_save_response(prompt: str, chat_id: int):
    try:
        messages = getChatMessages(chat_id)
        if messages.to_dict(orient='records'):
            try:
                messages = messages.drop(columns=['_id', 'createdAt'])
                messages = messages.rename(columns={'user': 'role', 'text': 'content'})
            except KeyError as e:
                logger.error("Missing key in chat messages: %s" % str(e))
            except Exception as e:
                logger.error("Failed to process chat messages: %s" % str(e))
        try:
            saveMessagesToDB(chat_id, prompt, "user")
        except Exception as e:
            logger.error("Failed to save user message to DB: %s" % str(e))
        try:
            aiResponse = generateResponse(prompt, messages.to_dict(orient='records'))
        except Exception as e:
            logger.error("Failed to generate AI response: %s" % str(e))
            return {"error": "Failed to generate AI response"}
        try:
            saveMessagesToDB(chat_id, aiResponse['text'], "assistant")
        except Exception as e:
            logger.error("Failed to save AI response to DB: %s" % str(e))
        return aiResponse
    except Exception as e:
        logger.error("Failed to process chat: %s" % str(e))
        return {"error": "Failed to process chat"}


