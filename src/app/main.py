from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.database import engine
from .api.database import Base
from .api.routers import authenticate_router, user_router, user_info_router, confirm_router

Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    """`` FastAPI initialization ``  """
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(user_router.router, prefix="/sign-up", tags=["sign-up"])
    application.include_router(confirm_router.router, prefix="/verify", tags=["verify"])
    application.include_router(authenticate_router.router, prefix="/sign-in", tags=["sign-in"])
    application.include_router(user_info_router.router, prefix="/user-info", tags=["user-info"])

    return application


app = get_application()
