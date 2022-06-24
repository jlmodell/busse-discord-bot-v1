from pymongo import MongoClient

from .constants import MONGODB_URI

CLIENT = MongoClient(MONGODB_URI)
DB = CLIENT.tickets_prod

TICKETS = DB.tickets

def get_latest_tickets(limit: int = 10):
    return list(TICKETS.find({ "completed": False }).sort("created_at", -1).limit(limit))