import motor.motor_tornado
from pymongo import ReturnDocument

from rich import print

from datetime import datetime

from nextcord import Embed

from bson.objectid import ObjectId
from typing import List, Tuple

from constants import MONGODB_URI


CLIENT = motor.motor_tornado.MotorClient(MONGODB_URI)
DB = CLIENT.tickets_prod

TICKETS = DB.tickets


async def get_latest_tickets(limit: int = 10, type: str = "it") -> List:
    """
    Args:
        limit (int, optional): set limit to number of tickets to grab. Defaults to 10.
        type (str, optional): it|maintenance are the available types. Defaults to "it".

    Returns:
        List: returns list of tickets as dict
    """

    return (
        await TICKETS.find({"type": type, "completed": False})
        .sort("createdAt", -1)
        .limit(limit)
        .to_list(limit)
    )


async def get_one_ticket(id: str) -> dict:
    """
    Args:
        id (str): id as string

    Returns:
        dict: returns ticket as dict
    """
    filter = {"_id": ObjectId(id)}
    doc = await TICKETS.find_one(filter)

    return doc


def format_ticket(idx: int, ticket: dict) -> Tuple[str, Embed]:
    if not ticket:
        return "...\n"

    ca = ticket["createdAt"]
    up = ticket["updatedAt"]

    html_hyperlink = Embed(
        title=str(ticket["_id"]),
        url="https://it.busseweb.com/tickets/editor/{}".format(str(ticket["_id"])),
        description=ticket["description"],
        colour=3447003,
    )

    obj = {
        "id": str(ticket["_id"]),
        "created_at": f"{ca:%m/%d/%y %H:%M:%S}",
        "updated_at": f"{up:%m/%d/%y %H:%M:%S}",
        "submitted_by": ticket["submittedBy"],
        "files": "\n".join(ticket.get("files", []))
        if len(ticket.get("files", [])) > 0
        else "No files",
        "description": ticket["description"],
        "notes": ticket["notes"],
    }

    r = "**{0}. -> Start**\n".format(idx + 1)

    for k, v in obj.items():
        if k in ["description", "notes"]:
            _v = v.split("\n")
            r += "{0: <25}\n".format("__" + k + "__:")
            for val in _v:
                r += "{0: <30}{1}\n".format("", val)

        elif k == "id":
            r += "{0: <25}{1}\n".format("__" + k + "__:", "||" + v + "||")

        else:
            r += "{0: <25}{1}\n".format("__" + k + "__:", v)

    r += "**{0}. -> End**\n\n".format(idx + 1)

    return r, html_hyperlink


if __name__ == "__main__":
    print(get_latest_tickets())
