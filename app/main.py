from fastapi import Depends,FastAPI,Request
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import motor.motor_asyncio
from pydantic import BaseModel


class Item(BaseModel):
    item: str
    item_status: bool


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://my-database-container:27017') #update => ('localhost',27017) for testing it locally 
db = client['Notes']
collection = db.todo
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")



@app.get("/")
async def root(request: Request):
    notes_open =[]
    notes_completed =[]
    async for doc in collection.find({'item_status': False}):
        notes_open.append(doc)
    async for doc in collection.find({'item_status': True}):
            notes_completed.append(doc)
    return templates.TemplateResponse("index.html",{"request": request , "notes_open":notes_open,"notes_completed":notes_completed})


@app.post("/notes")
async def create_item(item: Item):
    temp = 0;
    latest_id = collection.find({},{"id":1,"_id":0}).sort("id",-1).limit(1)
    for ids in await latest_id.to_list(length=1):
        temp = ids['id']
    collection.insert_one({'id':int(temp)+1,'item':item.item,'item_status':item.item_status})
    return {
            "code":"ok",
            "message":"success"
        }

@app.get("/notes/{id}")
async def read_item(request: Request,id: int):
    value = await collection.find_one({'id':id})
    if value is None:
        return{
            "code":"ok",
            "message":"no notes found"
        }
    return {
        "code":"ok",
        "message":"success",
        "id":value['id'],
        "item":value['item'],
        "item_status":value['item_status']
    }


@app.put("/notes/{id}")
async def update_item(item: Item,id: int):
    collection.update_one({'id':id},{'$set' : {'item':item.item,'item_status':item.item_status}})
    return {
        "code":"ok",
        "message":"success",
        "id":id,
        "item":item.item,
        "item_status":item.item_status
    }


@app.delete("/notes/{id}")
async def delete_item(id: int):
    collection.delete_many({'id':id})
    return {
        "code":"ok",
        "Message":"Deleted Note "+ str(id)
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000,reload=True)