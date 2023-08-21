from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    firstname : str
    lastname : str
    isMale : bool
    id : int

@app.get('/', status_code=200)
def demoFunc():
    return {"message" : "server is running"}

@app.get("/getpersonbyid/{person_id}", status_code=200)
def getPerson_id(person_id : int):
    return {"message" : f"your id is {person_id}"}

@app.post('/addperson', status_code=200)
def addperson(person: Person):
    return {
        "id" : person.id,
        "firstname" : person.firstname,
        "lastname" : person.lastname,
        "isMale" : person.isMale
    }
