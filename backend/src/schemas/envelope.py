from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class ApiEnvelope(BaseModel, Generic[T]):
    cod_retorno: int
    mensagem: str | None
    data: T | None

    @staticmethod
    def ok(data: T) -> "ApiEnvelope[T]":
        return ApiEnvelope(cod_retorno=0, mensagem=None, data=data)

    @staticmethod
    def err(message: str) -> "ApiEnvelope[None]":
        return ApiEnvelope(cod_retorno=1, mensagem=message, data=None)
