from fastapi import FastAPI
from pydantic import BaseModel
import requests
from requests.exceptions import HTTPError
app = FastAPI()

class Server(BaseModel):
    url: str
    
tested_servers = []
up_servers = []
down_servers = []

@app.get("/all")
async def all_servers():
    for server in tested_servers:
        try:
            response = requests.get(server,timeout=4)
            response.raise_for_status()
            if response.status_code == 200:
                status = "Fine " + str(response.status_code)
                up_servers.append(server)
        except HTTPError as error:
            down_servers.append(server)
        except Exception as error:
            down_servers.append(server) 
    return {"Up Servers":up_servers,"DownServers":down_servers}

@app.get('/monitor/')
async def monitor(server: str):
    if server in tested_servers:
        try:
            response = requests.get(server,timeout=4)
            response.raise_for_status()
            if response.status_code == 200:
                status = "Fine " + str(response.status_code)
                return {"Status":"Up"}
        except HTTPError as error:
            return {"Status":"Down"}
        except Exception as error:
            return {"Status":"Down"} 
    else:
        return {"Status":"Please use Post to add this server"}

@app.post('/server/add/')
async def add_Server(items: Server):
    tested_servers.append(items.url)
    try:
        response = requests.get(items.url,timeout=4)
        response.raise_for_status()
        if response.status_code == 200:
            status = "Fine " + str(response.status_code)
            return {"Status":"Up"}
    except HTTPError as error:
        return {"Status":"Down"}
    except Exception as error:
        return {"Status":"Down"}



@app.put('/server/update')
async def update_server(server: str,newserver: str):
    if server in tested_servers:
        idx = tested_servers.index(server)
        tested_servers[idx] = newserver
        return {"Status":"Updated"}
    else:
        return {"Status":"Not Found"}

@app.delete('/server/delete/')
async def delete_Server(server: str):
    if server in tested_servers:
        tested_servers.remove(server)
        return {"Status":"Deleted"}
    else:
        {"Status":"Not Found"}






