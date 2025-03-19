from fastapi import FastAPI
from app.models import Todo
from db.supabase_client import create_supabase_client

#use this command to restart server: uvicorn main:app --reload
#use this command to run sever: fastapi dev main.py
#fastapi supports authentication methods, are built in 
#can input .docs after local host url to get swagger ui in browser
# -ex http://127.0.0.1:8000.docs
#supabase db password: 0zDHtimOVq8dZfRu

app = FastAPI()
supabase = create_supabase_client()

#sytnax is in plain python
@app.get("/") #path decorator, whateve method is below is in charge of handling any requests going
# to slash
async def root(): #root returns json of hello world
    #async is build in with asgi 
    return {"message": "Hello World"}

#create a todo 
#If want to put an item in a database or a list, have to specify a pydantic schema
@app.post("/todos") 
async def create_todos(todo: Todo): #passing todo item of type Todo, this is enforcing type validation because of pydantic 
    response = supabase.from_("todo")\
            .insert({"item": todo.item})\
            .execute()
    if "error" in response or response.data is None:
        return {"error": "Failed to add todo to database"}
    # todos.append(todo) #appending the todo to the todos list
    return {"message": "todo has been added"} #returning message that todo has been added

#get all todos
@app.get("/todos")
async def get_todos():
    response = supabase.from_("todo")\
        .select("*")\
        .execute()

    if not response.data:
        return {"message": "No todos found"}

    return {"todos": response.data}  # ✅ Return all todos


#get a single todo
@app.get("/todos/{todo_id}") 
async def get_single_todo(todo_id:int): 
        response = supabase.from_("todo")\
            .select("id", "item")\
            .eq("id", todo_id)\
            .execute()
        if not response.data:
            return {"message": "todo not found"}
        return {"message": response.data[0]} #if not todo is found then output this message 


#update a todo
@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, new_value: Todo):
    # Check if the todo exists in the database
    response = supabase.from_("todo")\
        .select("id")\
        .eq("id", todo_id)\
        .execute()

    # If not found, return an error message
    if not response.data:
        return {"message": "todo not found"}

    # Update the todo item
    update_response = supabase.from_("todo")\
        .update({"item": new_value.item})\
        .eq("id", todo_id)\
        .execute()

    return {"message": "successfully updated", "updated_data": update_response.data}



#delete a todo
@app.delete("/todos/{todo_id}") 
async def delete_todo(todo_id:int): 
     response = supabase.from_("todo")\
            .select("id")\
            .eq("id", todo_id)\
            .execute()\
        #if not found return that it is not found 
     if not response.data:
        return {"message": "todo not found"}
     delete_response = supabase.from_("todo")\
        .delete().eq("id", todo_id)\
        .execute()
     return {"message": "successfully deleted", "deleted_data": delete_response}

