# 导入所需的库
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from EdgeGPT import Chatbot, ConversationStyle

# 创建一个fastapi应用
app = FastAPI()

# 创建一个edgegpt聊天机器人对象
bot = Chatbot(cookiePath="cookie.json")

# 定义一个websocket路由
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 接受websocket连接请求
    await websocket.accept()
    # 循环接收和发送消息
    while True:
        # 接收用户发送的消息
        data = await websocket.receive_text()
        # 调用edgegpt的API并获取回复消息
        response = await bot.ask(prompt=data, conversation_style=ConversationStyle.balanced)
        # 发送回复消息给用户
        await websocket.send_text(response["item"][
                    "messages"
                ][1]["adaptiveCards"][0]["body"][0]["text"])

# 定义一个HTML模板来显示聊天界面，这里只是简单地使用了一些基本的HTML和JavaScript代码，你可以根据你的喜好进行美化和改进。
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat with EdgeGPT</title>
</head>
<body>
    <h1>Chat with EdgeGPT</h1>
    <div id="chatbox" style="width: 600px; height: 400px; border: 1px solid black; overflow-y: scroll;"></div>
    <form id="form" action="#" onsubmit="sendMessage(event)">
        <input id="input" type="text" autocomplete="off"/>
        <button type="submit">Send</button>
    </form>
    <script>
        // 创建一个websocket对象，连接到后端的websocket路由
        var ws = new WebSocket("ws://localhost:8000/ws");
        
        // 定义一个函数，用于在聊天框中显示消息，并滚动到最底部
        function showMessage(message) {
            var chatbox = document.getElementById("chatbox");
            chatbox.innerHTML += message + "<br>";
            chatbox.scrollTop = chatbox.scrollHeight;
        }
        
        // 当websocket连接成功时，显示一条欢迎消息，并清空输入框中的内容（如果有）
        ws.onopen = function(event) {
            showMessage("Welcome to chat with EdgeGPT!");
            document.getElementById("input").value = "";
        };
        
        // 当websocket接收到后端发送的消息时，显示一条带有EdgeGPT标签的消息，并清空输入框中的内容（如果有）
        ws.onmessage = function(event) {
            showMessage("<b>EdgeGPT:</b> " + event.data);
            document.getElementById("input").value = "";
        };
        
        // 当表单提交时，阻止默认行为（刷新页面），获取输入框中的内容（如果不为空），并通过websocket发送给后端，并显示一条带有User标签的消息。
        function sendMessage(event) {
            event.preventDefault();
            var input = document.getElementById("input");
            var message = input.value;
            if (message) {
                ws.send(message);
                showMessage("<b>User:</b> " + message);
            }
            
        }
    </script>
</body>
</html>
"""
