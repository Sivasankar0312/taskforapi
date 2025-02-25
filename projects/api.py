from sanic import Sanic, json
from sanic.exceptions import NotFound
import uuid
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = Sanic("FSMApp")
app.config.ALLOWED_COMMANDS = {"Start", "Pause", "Resume", "Stop"}

class FSMStorage:
    def __init__(self):
        self.instances = {}
        self.global_lock = asyncio.Lock()
    
    async def create_instance(self):
        async with self.global_lock:
            instance_id = str(uuid.uuid4())
            self.instances[instance_id] = {
                "current_state": "IDLE",
                "lock": asyncio.Lock()
            }
            return instance_id
    
    async def get_instance(self, fsm_id: str):
        async with self.global_lock:
            return self.instances.get(fsm_id)

storage = FSMStorage()


TRANSITIONS = {
    ("IDLE", "Start"): "Running",
    ("Running", "Pause"): "Paused",
    ("Running", "Stop"): "IDLE",
    ("Paused", "Resume"): "Running",
    ("Paused", "Stop"): "IDLE",
}
@app.get("/")
async def hello_world(request):
    return text("Hello, world.")
    
@app.post("/fsm")
async def create_fsm(request):
    """Create a new FSM instance with IDLE state"""
    instance_id = await storage.create_instance()
    return json({"id": instance_id, "state": "IDLE"}, status=201)

@app.get("/fsm/<fsm_id:str>")
async def get_state(request, fsm_id: str):
    """Get current state of an FSM instance"""
    instance = await storage.get_instance(fsm_id)
    if not instance:
        raise NotFound("FSM instance not found")
    return json({"state": instance["current_state"]})

@app.post("/fsm/<fsm_id:str>/command")
async def process_command(request, fsm_id: str):
    """Process state transition command"""
    instance = await storage.get_instance(fsm_id)
    if not instance:
        raise NotFound("FSM instance not found")
    
    command = request.json.get("command")
    if command not in app.config.ALLOWED_COMMANDS:
        return json({"error": "Invalid command"}, status=400)
    
    async with instance["lock"]:
        current_state = instance["current_state"]
        next_state = TRANSITIONS.get((current_state, command))
        
        if not next_state:
            return json({"error": "Transition not allowed"}, status=400)
        
        instance["current_state"] = next_state
        return json({"state": next_state})

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        access_log=True,
        debug=os.getenv("DEBUG", False)
    )