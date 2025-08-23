from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from handler import validation_exception_handler
from schema import Operation, Result

app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/operation")
async def index():
    return {"message": "Hello World! Welcome on Operation API!"}


@app.post("/operation", response_model=Result)
async def calculate(operation: Operation):
    return Result(value=eval(operation.expression))
