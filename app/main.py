
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import Base
from app.database.connection import engine

# Import models
from app.models.user import User
from app.models.customer import Customer
from app.models.support import SupportAssignment
from app.models.payment import Payment
from app.models.analytics_note import AnalyticsNote

# Import controllers
from app.controllers.user_controller import router as user_router
from app.controllers.customer_controller import router as customer_router
from app.controllers.support_controller import router as support_router
from app.controllers.payment_controller import router as payment_router
from app.controllers.analytics_note_controller import router as analytics_note_router
from app.controllers.analytics_controller import router as analytics_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Support Management System API",
    description="Python backend for Support Management System",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://support-management-system-new-ui.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Register controllers
app.include_router(user_router)
app.include_router(customer_router)
app.include_router(support_router)
app.include_router(payment_router)
app.include_router(analytics_note_router)
app.include_router(analytics_router)


@app.get("/")
def home():
    return {
        "message": "Support Management System API is running"
    }
