from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from fastapi.staticfiles import StaticFiles
from pathlib import Path
from control.control import Controle

import asyncio

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
PHOTOS_DIR = FRONTEND_DIR / "photos"

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)

controle = Controle()

@app.get("/")
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")

capture_running = False # app state

connected_clients: list[WebSocket] = []

# ======== Websocket helpers ========
async def broadcast_message(message:dict):
    disconnected = []

    for client in connected_clients:
        try:
            await client.send_json(message)
        except:
            disconnected.append(client)
    for client in disconnected:
        connected_clients.remove(client)


# ======== REST API ========
@app.post("/api/capture/start")
async def start_capture():
    global capture_running

    if capture_running:
        raise HTTPException(
            status_code=400,
            detail='Capture is already running'
        )
    
    try:
        capture_running = True

        await broadcast_message({
            "type": "status",
            "value": "running"
        })

        asyncio.create_task(capture_task())

        return JSONResponse({
            "message": "Capture started"
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start capture: {str(e)}"
        )
    
@app.post("/api/capture/cancel")
async def cancel_capture():
    global capture_running

    if not capture_running:
        raise HTTPException(
            status_code=400,
            detail='No capture is running'
        )
    
    try:
        capture_running = False

        controle.parar()

        await broadcast_message({
            "type": "status",
            "value": "idle"
        })

        return JSONResponse({
            "message": "Capture canceled"
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cancel capture: {str(e)}"
        )
    
@app.get("/api/photos")
async def get_photos():
    try:
        photos = sorted([
            file.name
            for file in PHOTOS_DIR.iterdir()
            if file.is_file()
        ])

        return JSONResponse({
            "photos": photos
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load photos: {str(e)}"
        )
    
# ======== Tasks ========
async def capture_task():
    global capture_running

    try:
        controle.iniciar()

        print("Captura concluída")

    finally:
        capture_running = False

        await broadcast_message({
            "type": "status",
            "value": "idle"
        })

# ======== Websocket ========
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    print("client connected")

    # Envia o status inicial
    await websocket.send_json({
        "type": "status",
        "value": "running" if capture_running else "idle"
    })

    try:
        while True:
            message = await websocket.receive_json()

            if message["type"] == "get_status":
                await websocket.send_json({
                    "type": "status",
                    "value": "running" if capture_running else "idle"
                })

    except WebSocketDisconnect:
        print("client disconnected")
        if websocket in connected_clients:
            connected_clients.remove(websocket)