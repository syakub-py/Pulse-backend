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
from Leases.DeleteLease import router as DeleteLeaseRouter

from Tenants.GetTenants import router as GetTenantsRouter
from Tenants.CheckTenantCode import router as CheckTenantCodeRouter

from Todos.AddTodo import router as AddTodoRouter
from Todos.GetTodos import router as GetTodosRouter
from Todos.DeleteTodo import router as DeleteTodoRouter
from Todos.GetRecommendations import router as GetRecommendationsRouter

from Users.AddAUser import router as AddUserRouter

from Utils.SendEmail import router as SendEmailRouter

from Analytics.GenerateAnalytics import router as GenerateAnalyticsRouter

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
app.include_router(DeleteLeaseRouter)
app.include_router(AddUserRouter)
app.include_router(GetTenantsRouter)
app.include_router(CheckTenantCodeRouter)
app.include_router(AddTodoRouter)
app.include_router(GetTodosRouter)
app.include_router(DeleteTodoRouter)
app.include_router(GetRecommendationsRouter)
app.include_router(SendEmailRouter)
app.include_router(GenerateAnalyticsRouter)
