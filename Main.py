from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from App.SocketConnection import router as SocketConnectionRouter

from App.Endpoints.Analytics import analyticsRoutes
from App.Endpoints.Chat import chatRoutes
from App.Endpoints.Email import emailRoutes
from App.Endpoints.Leases import leasesRoutes
from App.Endpoints.Properties import propertiesRoutes
from App.Endpoints.PulseAI import pulseAIRoutes
from App.Endpoints.Tenants import tenantRoutes
from App.Endpoints.Todos import todoRoutes
from App.Endpoints.Transactions import transactionsRoutes
from App.Endpoints.Users import usersRoutes

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
