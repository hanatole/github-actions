import uuid

from pydantic import BaseModel, model_validator, ConfigDict

from constants import Operator


class OperationBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    a: float
    b: float
    operator: Operator


class OperationIn(OperationBase):
    @property
    def expression(self):
        return f"{self.a} {self.operator} {self.b}"

    @model_validator(mode="after")
    def model_validate(self):
        if self.b == 0 and self.operator == Operator.DIVISION.value:
            raise ValueError("Division by zero is not allowed")
        return self


class OperationOut(OperationBase):
    id: uuid.UUID


class Result(BaseModel):
    value: float
