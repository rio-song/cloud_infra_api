from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import main

app = FastAPI()


class Start_req(BaseModel):
    cpu_size: str
    memory_size: str
    name: str

class Login_req(BaseModel):
    command: str

# class Start_res(BaseModel):
#     userId: int
#     instanceId: int

# class Login_res(BaseModel):
#     result: str

#起動API
# @app.post("/instance/start", response_model=Start_res)
@app.post("/instance/start")
async def start(start: Start_req):
    result = main.start_instance(start.name, start.cpu_size, start.memory_size)
    if result == 'not_empty_error': 
        raise HTTPException(status_code=404, detail="not_empty_memory")
    if result == 'not_found_unused_ipaddress': 
        raise HTTPException(status_code=404, detail="not_found_unused_ipaddress")
    return JSONResponse(content={"userId": result[0], "instanceId": result[1]})

#停止API
@app.post("/instance/stop/{instanceId}/{userId}")
async def stop(instanceId:int,userId: int):
    main.stop_instance(instanceId, userId)
    return {"res": "ok"}

#ログインAPI
# @app.post("/instance/login/{instanceId}/{userId}",response_model= Login_res)
@app.post("/instance/login/{instanceId}/{userId}")
async def login(instanceId:int, userId : int, login_req:Login_req):
    result = main.login_instance(instanceId, userId, login_req.command)
    return {"res": result}
