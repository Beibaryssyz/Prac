from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid, time

app = FastAPI(title="TicketBook API", version="1.0")
USERS = {
    "user@test.com": {"password": "Test1234!", "user_id": 1, "name": "Test User", "email": "user@test.com"},
    "admin@test.com": {"password": "Admin1234!", "user_id": 2, "name": "Admin", "email": "admin@test.com"},
}

EVENTS = {
    1: {"event_id": 1, "title": "Концерт Imagine Dragons", "category": "concert", "date": "2026-07-10", "price": 5000},
    2: {"event_id": 2, "title": "Спектакль «Гамлет»",     "category": "theatre", "date": "2026-07-15", "price": 3000},
    3: {"event_id": 3, "title": "Кино: Inception",          "category": "cinema",  "date": "2026-07-20", "price": 1500},
    4: {"event_id": 4, "title": "Фестиваль джаза",          "category": "concert", "date": "2026-07-25", "price": 4000},
    5: {"event_id": 5, "title": "Театр «Ревизор»",          "category": "theatre", "date": "2026-08-01", "price": 2500},
}

SESSIONS = {}  
BOOKINGS = {}   
booking_counter = 0

def get_user_from_token(authorization: Optional[str]) -> int:
    """Извлекает user_id из заголовка Authorization: Bearer <token>"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: missing token")
    token = authorization.split(" ", 1)[1]
    if token not in SESSIONS:
        raise HTTPException(status_code=401, detail="Unauthorized: invalid or expired token")
    return SESSIONS[token]

# M1 Auth
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

@app.post("/api/auth/register", tags=["M1 Auth"])
def register(body: RegisterRequest):
    if body.email in USERS:
        raise HTTPException(status_code=409, detail="User already exists")
    USERS[body.email] = {"password": body.password, "user_id": len(USERS) + 1, "name": body.name, "email": body.email}
    return {"message": "User registered successfully", "email": body.email}

@app.post("/api/auth/login", tags=["M1 Auth"])
def login(body: LoginRequest):
    user = USERS.get(body.email)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid.uuid4())
    SESSIONS[token] = user["user_id"]
    return {"session_token": token, "user_id": user["user_id"], "name": user["name"]}

@app.post("/api/auth/logout", tags=["M1 Auth"])
def logout(authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)
    token = authorization.split(" ", 1)[1]
    del SESSIONS[token]
    return {"message": "Logged out"}

# M2 Catalog
@app.get("/api/catalog/events", tags=["M2 Catalog"])
def get_events(category: Optional[str] = None, date: Optional[str] = None):
    result = list(EVENTS.values())
    if category:
        result = [e for e in result if e["category"] == category]
    if date:
        result = [e for e in result if e["date"] == date]
    return {"events": result, "total": len(result)}

@app.get("/api/catalog/events/{event_id}", tags=["M2 Catalog"])
def get_event(event_id: int):
    event = EVENTS.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/api/catalog/events", tags=["M2 Catalog"])
def create_event(body: dict, authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)
    new_id = max(EVENTS.keys()) + 1
    EVENTS[new_id] = {"event_id": new_id, **body}
    return {"message": "Event created", "event_id": new_id}

# M3 Booking
class BookingRequest(BaseModel):
    event_id: int

@app.post("/api/booking/create", tags=["M3 Booking"])
def create_booking(body: BookingRequest, authorization: Optional[str] = Header(None)):
    global booking_counter
    user_id = get_user_from_token(authorization)

    if body.event_id not in EVENTS:
        raise HTTPException(status_code=404, detail="Event not found")

    booking_counter += 1
    booking_id = booking_counter
    BOOKINGS[booking_id] = {
        "booking_id": booking_id,
        "event_id": body.event_id,
        "user_id": user_id,
        "status": "pending",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    return {"booking_id": booking_id, "event_id": body.event_id, "status": "pending"}

@app.get("/api/booking/{booking_id}", tags=["M3 Booking"])
def get_booking(booking_id: int, authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)
    booking = BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.get("/api/booking", tags=["M3 Booking"])
def list_bookings(authorization: Optional[str] = Header(None)):
    user_id = get_user_from_token(authorization)
    result = [b for b in BOOKINGS.values() if b["user_id"] == user_id]
    return {"bookings": result, "total": len(result)}

@app.delete("/api/booking/{booking_id}", tags=["M3 Booking"])
def cancel_booking(booking_id: int, authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)
    booking = BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking["status"] == "paid":
        raise HTTPException(status_code=409, detail="Cannot cancel a paid booking")
    booking["status"] = "cancelled"
    return {"message": "Booking cancelled", "booking_id": booking_id}

# M4 Payment
class PaymentRequest(BaseModel):
    booking_id: int
    card_token: str

@app.post("/api/payment/pay", tags=["M4 Payment"])
def pay(body: PaymentRequest, authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)

    booking = BOOKINGS.get(body.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # НАМЕРЕННЫЙ БАГ для TC-INT-05:
    if booking["status"] == "paid":
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if body.card_token == "tok_test_valid":
        booking["status"] = "paid"
        return {"payment_status": "success", "booking_id": body.booking_id}

    elif body.card_token == "tok_test_decline":
        booking["status"] = "failed"
        raise HTTPException(status_code=402, detail="Payment declined")

    else:
        raise HTTPException(status_code=400, detail="Unknown card token")