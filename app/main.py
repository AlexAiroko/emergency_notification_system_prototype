from fastapi import FastAPI

from app.api.notification_template import router as template_router


app = FastAPI()


app.include_router(template_router)
