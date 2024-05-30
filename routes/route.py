from fastapi import APIRouter
from models.evaluations import Evaluation
from database.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

### Evaluations collection

# GET Request
@router.get("/")
async def get_evaluations():
    evaluations = list_serial(collection_name.find())
    return evaluations

# POST
@router.post("/")
async def post_evaluation(evaluation: Evaluation):
    collection_name.insert_one(dict(evaluation))
