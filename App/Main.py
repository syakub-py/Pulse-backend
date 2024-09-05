from fastapi import FastAPI
from dotenv import load_dotenv

from App.Handlers.Chat.GetChatMessages import router as GetChatMessagesRouter
from App.Handlers.Chat.GetChats import router as GetChatsRouter
from App.Handlers.PulseAI.GenerateResponse import router as GenerateResponseRouter

from App.Handlers.Properties.AddProperty import router as AddPropertyRouter
from App.Handlers.Properties.GetProperties import router as GetPropertiesRouter
from App.Handlers.Properties.DeleteProperty import router as DeletePropertyRouter

from App.Handlers.Leases.AddLease import router as AddLeaseRouter
from App.Handlers.Leases.GetLeases import router as GetLeasesRouter
from App.Handlers.Leases.DeleteLease import router as DeleteLeaseRouter

from App.Handlers.Tenants.GetTenants import router as GetTenantsRouter
from App.Handlers.Tenants.CheckTenantCode import router as CheckTenantCodeRouter

from App.Handlers.Todos.AddTodo import router as AddTodoRouter
from App.Handlers.Todos.GetTodos import router as GetTodosRouter
from App.Handlers.Todos.DeleteTodo import router as DeleteTodoRouter
from App.Handlers.Todos.GetRecommendations import router as GetRecommendationsRouter

from App.Handlers.Users.AddAUser import router as AddUserRouter
from App.Handlers.Users.DeleteAUser import router as DeleteUserRouter
from App.Handlers.Users.GetUid import router as GetUidRouter

from App.Handlers.Emails.SendEmail import router as SendEmailRouter

from App.Handlers.Analytics.GenerateExpenseAnalytics import router as GenerateExpenseAnalyticsRouter
from App.Handlers.Analytics.GenerateIncomeAnalytics import router as GenerateIncomeAnalyticsRouter

from App.Handlers.Transactions.AddTransaction import router as AddTransactionRouter
from App.Handlers.Transactions.GetTransactions import router as GetTransactionsRouter

from App.SocketConnection import router as SocketConnectionRouter

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

app.include_router(AddPropertyRouter)
app.include_router(GetPropertiesRouter)
app.include_router(DeletePropertyRouter)

app.include_router(GetChatMessagesRouter)
app.include_router(GenerateResponseRouter)
app.include_router(GetChatsRouter)

app.include_router(CheckTenantCodeRouter)
app.include_router(AddLeaseRouter)
app.include_router(GetLeasesRouter)
app.include_router(DeleteLeaseRouter)
app.include_router(SendEmailRouter)

app.include_router(AddUserRouter)
app.include_router(DeleteUserRouter)
app.include_router(GetUidRouter)

app.include_router(GetTenantsRouter)

app.include_router(AddTodoRouter)
app.include_router(GetTodosRouter)
app.include_router(DeleteTodoRouter)

app.include_router(GetRecommendationsRouter)

app.include_router(GenerateExpenseAnalyticsRouter)
app.include_router(GenerateIncomeAnalyticsRouter)

app.include_router(AddTransactionRouter)
app.include_router(GetTransactionsRouter)

app.include_router(SocketConnectionRouter)
