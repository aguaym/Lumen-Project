from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

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
        photos = [
            "photo_001.jpg",
            "photo_002.jpg",
            "photo_003.jpg",
        ]

        return JSONResponse({
            "photos": photos
        })
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load photos: {str(e)}"
        )
    
# ======== Websocket ========
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    connected_clients.append(websocket)

    print("client connected")

    await websocket.send_json({
        "type":"status",
        "value":"running" if capture_running else "idle"
    })

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("client disconnected")
        if(websocket in connected_clients):
            connected_clients.remove(websocket)