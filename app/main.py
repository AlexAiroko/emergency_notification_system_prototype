from fastapi import FastAPI

from app.api.notification_template import router as template_router
from app.api.contact import router as contact_router
from app.api.contact_method import router as contact_method_router
from app.api.group import router as group_router
from app.api.delivery import router as delivery_router
from app.api.notification import router as notification_router

app = FastAPI()


app.include_router(template_router)
app.include_router(contact_router)
app.include_router(contact_method_router)
app.include_router(group_router)
app.include_router(delivery_router)
app.include_router(notification_router)
