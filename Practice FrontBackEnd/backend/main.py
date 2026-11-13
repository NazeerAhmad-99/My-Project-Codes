from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

class SalaryRequest(BaseModel):
    salary: int = Field(gt=0 , description = " Dont fuck around fool, you wanna work for free?? retard!")
    


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Salary checker API is running!"}


@app.post("/check-salary")
def check_salary(salary_data: SalaryRequest):
    if salary_data.salary > 39000:
        return {"message": "The salary is above the maximum we can offer."}
    else:
        return {"message": "The salary is within the acceptable range."}
