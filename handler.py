from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append(err["msg"])
    return JSONResponse(status_code=400, content={"error": ". ".join(errors)})
