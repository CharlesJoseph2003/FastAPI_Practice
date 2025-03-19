from fastapi import FastAPI
from models import Todo

#use this command to restart server: uvicorn main:app --reload
#use this command to run sever: fastapi dev main.py
#fastapi supports authentication methods, are built in 
#can input .docs after local host url to get swagger ui in browser
# -ex http://127.0.0.1:8000.docs

app = FastAPI()

#sytnax is in plain python
@app.get("/") #path decorator, whateve method is below is in charge of handling any requests going
# to slash
async def root(): #root returns json of hello world
    #async is build in with asgi 
    return {"message": "Hello World"}

todos = [] #global todo list 

#create a todo 
#If want to put an item in a database or a list, have to specify a pydantic schema
@app.post("/todos") 
async def create_todos(todo: Todo): #passing todo item of type Todo, this is enforcing type validation because of pydantic 
    todos.append(todo) #appending the todo to the todos list
    return {"message": "todo has been added"} #returning message that todo has been added

#get all todos
@app.get("/todos") 
async def get_todos():  # Ensure no parameters here
    return {"todos": todos}  # Return the global todos list

#get a single todo
@app.get("/todos/{todo_id}") 
async def get_single_todo(todo_id:int): 
    for todo in todos:
        if todo.id == todo_id: #checks if each specific todo in the list of todos has this specific id 
            return {"todo": todo} #returning the todo if it is found
    return {"message": "no todos found"} #if not todo is found then output this message 


#update a todo
@app.put("/todos/{todo_id}")
async def update_todo(todo_id:int, new_value:Todo):
    for todo in todos:
        if todo.id == todo_id:
            todo.item = new_value.item
            return{"message": "todo has been updated"}
    return {"message":"no todos found "}


#delete a todo
@app.get("/todos/{todo_id}") 
async def get_single_todo(todo_id:int): 
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": "todo has been deleted"} #returning the todo if it is found
    return {"message": "no todos found"} #if not todo is found then output this message 
