from django.shortcuts import render
from ninja import NinjaAPI
from .models import Todo
from pydantic import BaseModel
from typing import List
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
# Create your views here.

api = NinjaAPI()

def api_redirect(request):
    return redirect("/api/docs")

class TodoSchema(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class TodoOutSchema(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    class Config:
        orm_mode = True
        from_attributes = True

@api.get("/todos", response=List[TodoOutSchema])
def list_todos(request):
    todos = Todo.objects.all()
    return [TodoOutSchema.from_orm(todo) for todo in todos]

@api.get("/todos/{todo_id}", response=TodoOutSchema)
def get_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, id=todo_id)
    return todo

@api.post("/todos", response=TodoOutSchema)
def create_todo(request, data: TodoSchema):
    todo = Todo.objects.create(**data.dict())
    return todo

@api.put("/todos/{todo_id}", response=TodoOutSchema)
def update_todo(request, todo_id: int, data: TodoSchema):
    todo = get_object_or_404(Todo, id=todo_id)
    for attr, value in data.dict().items():
        setattr(todo, attr, value)
    todo.save()
    return todo

@api.delete("/todos/{todo_id}")
def delete_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return {"success": True}

@api.get("/checkPer")
def per_todo(request):
    total = Todo.objects.count()
    ch_count = Todo.objects.filter(completed=True).count()
    if ch_count == 0:
        per_check = 0
    else:
        per_check = (ch_count / total) * 100  # 완료된 할 일의 비율 계산
    
    per_noncheck = 100 - per_check 
    return {
        "total" : total,
        "check_count" : ch_count,
        "per_check" : per_check,
        "per_noncheck" : per_noncheck
            }
