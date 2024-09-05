from typing import Dict
from fastapi import APIRouter
from Models.TodoDetails import TodoDetails
from App.Handlers.Todos.AddTodo import addTodo
from App.Handlers.Todos.GetTodos import getTodos
from App.Handlers.Todos.DeleteTodo import deleteTodo
from App.Handlers.Todos.GetRecommendations import getRecommendations

todoRoutes = APIRouter(prefix="/todo")

@todoRoutes.post("/addTodo/", response_model=Dict)
async def add_todo(todo: TodoDetails):
    return addTodo(todo)

@todoRoutes.delete("/deleteTodo/{todo_id}", response_model=Dict)
async def delete_todo(todo_id: int):
    return deleteTodo(todo_id)

@todoRoutes.post("/getRecommendations/{todoId}/{propertyAddress}", response_model=Dict)
async def get_recommendations(todoId: int, propertyAddress: str):
    return getRecommendations(todoId, propertyAddress)

@todoRoutes.post("/getTodos/{propertyId}", response_model=Dict)
async def get_todos(propertyId: int):
    return getTodos(propertyId)
