from fastapi import FastAPI
from dotenv import load_dotenv

from PulseAI.GetChatMessages import router as GetChatMessagesRouter
from PulseAI.CreateChat import router as CreateChatRouter
from PulseAI.GenerateResponse import router as GenerateResponseRouter

from Properties.AddProperty import router as AddPropertyRouter
from Properties.GetProperties import router as GetPropertiesRouter
from Properties.DeleteProperty import router as DeletePropertyRouter

from Leases.AddLease import router as AddLeaseRouter
from Leases.GetLeases import router as GetLeasesRouter

from starlette.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(CreateChatRouter)
app.include_router(AddPropertyRouter)
app.include_router(GetPropertiesRouter)
app.include_router(DeletePropertyRouter)
app.include_router(GetChatMessagesRouter)
app.include_router(GenerateResponseRouter)
app.include_router(AddLeaseRouter)
app.include_router(GetLeasesRouter)
