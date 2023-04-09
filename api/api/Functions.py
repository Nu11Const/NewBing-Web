import asyncio
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from EdgeGPT import Chatbot, ConversationStyle
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time
import json
app = FastAPI()
bot_list = []
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# 创建Jinja2模板实例
templates = Jinja2Templates(directory="templates")
@app.get("/")
def index(request: Request):
    # 渲染index.html模板，传入request参数
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data_raw = await websocket.receive_text()
        data = json.loads(data_raw)
        print(data)
        id = data["id"]
        if (bot_list[id]["style"] == "balanced"):
            style = ConversationStyle.balanced
        elif(bot_list[id]["style"] == "creative"):
            style = ConversationStyle.creative
        elif(bot_list[id]["style"] == "precise"):
            style = ConversationStyle.precise
        time.sleep(1)
        await websocket.send_text("Websocket OK")
        async for final,response in bot_list[id]["bot"].ask_stream(prompt=data["message"],conversation_style=style):
            if not final:
                await websocket.send_text(response)
            
        
        
        
@app.post("/api/newchat")
async def newchat(jsonData: dict):
    id = len(bot_list)
    print(jsonData)
    bot_list.append({
        "id": id,
        "style": jsonData["style"],
        "bot": None,
        "cookie": jsonData["cookie"]
    })
    if not(jsonData["cookie"] == str):
        temp = jsonData["cookie"]
        jsonData["cookie"] = json.loads(temp)
    bot_list[id]["bot"] = Chatbot(cookies=jsonData["cookie"])
    print(jsonData["cookie"])
    return bot_list[id]

@app.get("/api/get")
async def get(jsonData: dict):
    id = jsonData["id"]
    return bot_list[id]

@app.post("/api/change_style")
async def change_style(jsonData:dict):
    response = {"message": "successful","code":"200"}
    try:
        bot_list[jsonData["id"]]["style"] = jsonData["style"]
    except Exception as err:
        response["message"] = err
        response["code"] = "500"
    return response