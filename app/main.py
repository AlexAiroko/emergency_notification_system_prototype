from fastapi import FastAPI

from app.api.notification_template import router as template_router
from app.api.contact import router as contact_router

app = FastAPI()


app.include_router(template_router)
app.include_router(contact_router)

