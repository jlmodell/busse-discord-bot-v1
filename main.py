import random

import nextcord
from nextcord.ext import commands

from rich import print

from constants import DISCORD_BOT_TOKEN

from db import get_one_ticket

from discord_modal import Note, ManyTickets, SingleTicket


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(
    command_prefix="$", description="busse-ticket-bot (discord)", intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


# testing commands


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except ValueError:
        await ctx.send("Format has to be in NdN!")
        return

    result = ", ".join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(result)


@bot.command()
async def joined(ctx, member: nextcord.Member):
    """Says when a member joined."""
    await ctx.send(f"{member.name} joined in {member.joined_at}")


# end of testing commands


@bot.slash_command(
    name="note",
    description="Adds a note to a ticket",
)
async def note(ctx: nextcord.Interaction, id: str):
    """Adds a note to a ticket

    Args:
        ctx (_type_): discord context [type: nextcord.Interaction]
        id (str): id as string
    """
    try:
        doc = await get_one_ticket(id=id)

        if not doc:
            return

        id = doc["_id"]
        note = doc.get("notes", "")

        modal = Note(id=id, note=note)

        await ctx.response.send_modal(modal)

    except Exception as e:
        await ctx.send("error: {}".format(e))


@bot.slash_command(
    name="many",
    description="Returns many tickets limited by limit, default = 5",
)
async def many_tickets(ctx: nextcord.Interaction):
    """Returns many tickets limited by limit, default = 5

    Args:
        ctx (_type_): discord context [type: nextcord.Interaction]
    """
    modal = ManyTickets()
    await ctx.response.send_modal(modal)


@bot.slash_command(name="one", description="retrieves a ticket by id")
async def one_ticket(ctx: nextcord.Interaction, id: str):
    """queries tickets database by id and returns a ticket

    Args:
        ctx (_type_): discord context [type: nextcord.Interaction]
        id (str): id of ticket
    """
    modal = SingleTicket(id=id if id else "")
    await ctx.response.send_modal(modal)


bot.run(DISCORD_BOT_TOKEN)


# @bot.command("get_tickets", aliases=["all"])
# async def get_tickets(
#     ctx, ticket_type: Optional[Union[str, TicketType]], limit: Optional[int] = 10
# ):
#     """queries tickets database and returns <limit> tickets

#     Args:
#         ctx (_type_): discord context
#         ticket_type (str): it or maintenance
#         limit (int, optional): number of tickets to grab. Defaults to 10.
#     """
#     if ticket_type not in ["it", "maintenance", TicketType.it, TicketType.maintenance]:
#         await ctx.send(
#             "Format has to be $tickets * <type:<it|maintenance>> Optional[<limit:int>]"
#         )

#         return

#     try:
#         tickets = await get_latest_tickets(limit=limit, type=ticket_type)

#         if tickets:
#             for idx, ticket in enumerate(tickets):
#                 text, embed = format_ticket(idx, ticket)
#                 await ctx.send(text)
#                 await ctx.send(embed=embed)

#     except Exception as e:
#         await ctx.send("error: {}".format(e))


# @bot.command("get_ticket", aliases=["single"])
# async def get_ticket(ctx, id: Optional[str]):
#     """queries tickets database and returns <limit> tickets

#     Args:
#         ctx (_type_): discord context
#         id (str): id of ticket
#     """
#     if not id:
#         await ctx.send("Format has to be $get_ticket *<id:str>")

#         return

#     try:
#         ticket = await get_one_ticket(id=id)

#         if ticket:
#             text, embed = format_ticket(0, ticket)
#             await ctx.send(text)
#             await ctx.send(embed=embed)

#         else:
#             await ctx.send("404: Ticket not found")

#     except Exception as e:
#         await ctx.send("error: {}".format(e))
