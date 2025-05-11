from fastapi import FastAPI
app=FastAPI() # fast api initilization
#Route 
@app.get("/") #route 
def index(): # route handler function
    return {"data":{"name":"ganesh"}}
@app.get("/about") # about route
def about(): #route handler
    return {"about":"this is about route"}
#path parameter:
@app.get("/user/testuser")
def getuser():
    return {"user":"testuser path"}
@app.get("/user/{id}") # dynamic path parameter  (name of the parameter need to be same)
def getUser(id:int): #passed that in function (here id is type int)
    return {"userid":id} #getting the id in function
