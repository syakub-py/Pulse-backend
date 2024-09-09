from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from App.SocketConnection import router as SocketConnectionRouter

from App.Api.Analytics import analyticsRoutes
from App.Api.Chat import chatRoutes
from App.Api.Email import emailRoutes
from App.Api.Leases import leasesRoutes
from App.Api.Properties import propertiesRoutes
from App.Api.PulseAI import pulseAIRoutes
from App.Api.Tenants import tenantRoutes
from App.Api.Todos import todoRoutes
from App.Api.Transactions import transactionsRoutes
from App.Api.Users import usersRoutes

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(SocketConnectionRouter)

app.include_router(analyticsRoutes)
app.include_router(chatRoutes)
app.include_router(emailRoutes)
app.include_router(leasesRoutes)
app.include_router(propertiesRoutes)
app.include_router(pulseAIRoutes)
app.include_router(tenantRoutes)
app.include_router(todoRoutes)
app.include_router(transactionsRoutes)
app.include_router(usersRoutes)
