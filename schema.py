from pydantic import BaseModel, model_validator

from constants import Operator


class Operation(BaseModel):
    a: int | float
    b: int | float
    operator: Operator

    @property
    def expression(self):
        return f"{self.a} {self.operator.value} {self.b}"

    @model_validator(mode="after")
    def model_validate(self):
        if self.b == 0 and self.operator == Operator.DIVISION:
            raise ValueError("Division by zero is not allowed")
        return self


class Result(BaseModel):
    value: int | float
