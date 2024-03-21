from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import Beer
from database import SessionLocal, engine
from sqlalchemy import or_, and_, func


app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/")
async def fulfillment(request: Request):
    # Get the JSON payload from the request
    db = SessionLocal()
    payload = await request.json()
    # Extract the intent name
    print(payload)
    intent_name = payload["queryResult"]["intent"]["displayName"]
    print(intent_name)
    beer_names = []

    fulfillment_message = payload["queryResult"]["fulfillmentText"]

    if intent_name == "AlcoholContent_Intent":
        alcohol_level = payload["queryResult"]["parameters"]["alcohol_level_indicators"]
        if "high alcohol" in alcohol_level:
            qs = db.query(Beer).filter(Beer.alcohol_content >= 6.0).all()
            beer_names.extend([beer.name for beer in qs])
        elif "medium alcohol" in alcohol_level:
            qs = (
                db.query(Beer)
                .filter(and_(Beer.alcohol_content < 6.0, Beer.alcohol_content >= 4.0))
                .all()
            )
            beer_names.extend([beer.name for beer in qs])
        else:
            qs = db.query(Beer).filter(Beer.alcohol_content < 4.0).all()
            beer_names.extend([beer.name for beer in qs])

    elif intent_name == "Flavor_intent":
        flavor = payload["queryResult"]["parameters"]["flavor_indicator"]
        qs = db.query(Beer).filter(func.lower(Beer.flavor) == flavor.lower())
        beer_names.extend([beer.name for beer in qs])

    elif intent_name == "Packing_intent":
        packing = payload["queryResult"]["parameters"]["Packing_indicators"][0]
        qs = db.query(Beer).filter(func.lower(Beer.packing) == packing.lower())
        beer_names.extend([beer.name for beer in qs])

    elif intent_name == "Rating_intent":
        rating_indicator = payload["queryResult"]["parameters"]["user_rating_indicator"]
        if rating_indicator.lower().strip() == "excellent":
            qs = db.query(Beer).filter(Beer.user_rating >= 9.0).all()
            beer_names.extend([beer.name for beer in qs])
        elif rating_indicator.lower().strip() == "good":
            qs = (
                db.query(Beer)
                .filter(and_(Beer.user_rating < 9.0, Beer.user_rating >= 7.0))
                .all()
            )
            beer_names.extend([beer.name for beer in qs])
        elif rating_indicator.lower().strip() == "average":
            qs = (
                db.query(Beer)
                .filter(and_(Beer.user_rating < 7.0, Beer.user_rating >= 5.0))
                .all()
            )
            beer_names.extend([beer.name for beer in qs])
        else:
            qs = db.query(Beer).filter(Beer.user_rating < 5.0).all()
            beer_names.extend([beer.name for beer in qs])

    elif intent_name == "Region_Intent":
        region = payload["queryResult"]["parameters"]["Region_Indicators"]
        qs = db.query(Beer).filter(func.lower(Beer.region) == region.lower())
        beer_names.extend([beer.name for beer in qs])

    elif intent_name == "SeasonWeather_Intent":
        season = payload["queryResult"]["parameters"]["Season_Indicators"]
        qs = db.query(Beer).filter(func.lower(Beer.season) == season.lower())
        beer_names.extend([beer.name for beer in qs])

    beers = ", ".join(beer_names)
    return JSONResponse(
        content={
            "fulfillmentMessages": [{"text": {"text": [fulfillment_message, beers]}}]
        },
        headers={"Content-Type": "application/json"},
    )
