# FastAPI
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

# Third Party
from starlette.middleware.base import BaseHTTPMiddleware


class ErrorHandler(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as error:
            return JSONResponse(
                content={'error': str(error)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
