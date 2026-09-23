from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from connection import send_to_event_hub
from data import generate_ride_confirmation


app = FastAPI(title="RideFlow")

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/")
def booking_home(request: Request):

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request
        }
    )


@app.post("/book")
def book_ride(
    request: Request,
    pickup: str = Form(...),
    destination: str = Form(...),
    ride_type: str = Form(...),
    passengers: int = Form(...),
    payment: str = Form(...)
):

    ride = generate_ride_confirmation(
        pickup=pickup,
        destination=destination,
        ride_type=ride_type,
        passengers=passengers,
        payment=payment
    )

    event_data = {
        "ride_id": ride["ride_id"],
        "passenger_id": ride["passenger_id"],
        "driver_id": ride["driver_id"],
        "vehicle_id": ride["vehicle_id"],

        "pickup_city_id": ride["pickup_city_id"],
        "dropoff_city_id": ride["dropoff_city_id"],

        "vehicle_type_id": ride["vehicle_type_id"],
        "vehicle_make_id": ride["vehicle_make_id"],
        "payment_method_id": ride["payment_method_id"],
        "ride_status_id": ride["ride_status_id"],

        "distance_miles": ride["distance_miles"],
        "duration_minutes": ride["duration_minutes"],

        "booking_timestamp": ride["booking_timestamp"],
        "pickup_timestamp": ride["pickup_timestamp"],
        "dropoff_timestamp": ride["dropoff_timestamp"],

        "base_fare": ride["base_fare"],
        "distance_fare": ride["distance_fare"],
        "time_fare": ride["time_fare"],
        "surge_multiplier": ride["surge_multiplier"],
        "subtotal": ride["subtotal"],
        "tip_amount": ride["tip_amount"],
        "total_fare": ride["total_fare"]
    }

    result = send_to_event_hub(event_data)

    return templates.TemplateResponse(
        "confirmation.html",
        {
            "request": request,
            "ride": ride,
            "sent": result
        }
    )


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )