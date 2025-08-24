from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlmodel import select

from db import create_db_and_tables, SessionType, Operation as OperationDB
from schema import OperationIn, Result, OperationOut


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append(err["msg"])
    return JSONResponse(status_code=400, content={"error": ". ".join(errors)})


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/operation", response_model=list[OperationOut])
async def index(session: SessionType):
    return session.exec(select(OperationDB)).all()


@app.post("/operation", response_model=Result)
async def calculate(operation: OperationIn, session: SessionType):
    session.add(OperationDB(**operation.model_dump()))
    session.commit()
    return Result(value=eval(operation.expression))
