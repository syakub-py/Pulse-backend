from typing import Dict, Any
from fastapi import APIRouter
from App.EndpointParams.TodoDetails import TodoDetails
from App.Handlers.Todos.AddTodo import addTodo
from App.Handlers.Todos.GetTodos import getTodos
from App.Handlers.Todos.DeleteTodo import deleteTodo
from App.Handlers.Todos.GetRecommendations import getRecommendations

todoRoutes = APIRouter(prefix="/todo")

@todoRoutes.post("/addTodo/", response_model=Dict)
def add_todo(todo: TodoDetails) -> (int | Dict[str, Any]):
    return addTodo(todo)

@todoRoutes.delete("/deleteTodo/{todoId}", response_model=Dict)
def delete_todo(todoId: int) -> (None | Dict[str, Any]):
    return deleteTodo(todoId)

@todoRoutes.get("/getRecommendations/{todoId}/{propertyAddress}", response_model=Dict)
def get_recommendations(todoId: int, propertyAddress: str) -> (str | Dict[str, Any]):
    return getRecommendations(todoId, propertyAddress)

@todoRoutes.get("/getTodos/{propertyId}", response_model=Dict)
def get_todos(propertyId: int) -> (str | Dict[str, Any]):
    return getTodos(propertyId)
