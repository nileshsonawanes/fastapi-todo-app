from fastapi import FastAPI
from app.database.connection import engine, Base
from app.api import auth_routes, todo_routes

app = FastAPI(
    title="Todo Management API",
    description="A RESTful API for managing todos with JWT authentication",
    version="1.0.0"
)

# Include API routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(todo_routes.router, prefix="/todos", tags=["todos"])

@app.get("/")
def root():
    return {"message": "Welcome to the Todo Management API"}

# Create database tables on startup
@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

@app.on_event("shutdown")
def shutdown():
    print("🛑 Application shutting down")