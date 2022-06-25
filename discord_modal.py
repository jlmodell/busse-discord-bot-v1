import nextcord

from datetime import datetime

from bson.objectid import ObjectId

from db import TICKETS, get_latest_tickets, get_one_ticket, format_ticket


class ManyTickets(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Get Tickets")

        self.limit = nextcord.ui.TextInput(
            "Limit",
            placeholder="Limit number of records you want to retrieve. (default is 5)",
            default_value="5",
            required=True,
            row=1,
        )
        self.add_item(self.limit)

        self.type = nextcord.ui.Select(row=2)
        self.add_item(self.type)
        self.type.add_option(label="IT", value="it", default=True)
        self.type.add_option(label="Maintenance", value="maintenance", default=False)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            limit = int(self.limit.value)
        except:
            limit = 5

        if len(self.type.values) > 0:
            try:
                docs = await get_latest_tickets(limit=limit, type=self.type.values[0])
                if not docs:
                    await interaction.response.send_message(
                        "No pending tickets found for type: {}".format(
                            self.type.values[0]
                        )
                    )

                    return

                await interaction.response.send_message(
                    "{0} queried database for {1} ticket(s)\n".format(
                        interaction.user.mention, len(docs)
                    )
                )

                for idx, doc in enumerate(docs):
                    text, embed = format_ticket(idx, doc)
                    await interaction.followup.send(text)
                    await interaction.followup.send(embed=embed)

                return

            except Exception as e:
                await interaction.response.send_message("error: {}\n".format(e))


class SingleTicket(nextcord.ui.Modal):
    def __init__(self, id: str):
        super().__init__("Get Ticket by ID")

        self.id = nextcord.ui.TextInput(
            "Ticket ID",
            placeholder="ID for ticket you want to retrieve",
            default_value=id,
            required=True,
            row=1,
        )
        self.add_item(self.id)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            doc = await get_one_ticket(id=self.id.value)
            if not doc:
                await interaction.response.send_message(
                    "No pending tickets found for id: {}".format(self.id.value)
                )

                return

            await interaction.response.send_message(
                "{0} queried database for {1}\n".format(
                    interaction.user.mention, self.id.value
                )
            )

            text, embed = format_ticket(0, doc)
            await interaction.followup.send(text)
            await interaction.followup.send(embed=embed)

            return

        except Exception as e:
            await interaction.response.send_message("error: {}\n".format(e))


class Note(nextcord.ui.Modal):
    def __init__(self, id: ObjectId, note: str):
        super().__init__("Add/Update Notes to Ticket")

        self.id = nextcord.ui.TextInput(
            "Ticket ID",
            default_value=str(id),
            required=True,
            row=1,
        )
        self.add_item(self.id)

        self.note = nextcord.ui.TextInput(
            "Notes",
            style=nextcord.TextInputStyle.paragraph,
            default_value=note,
            placeholder="Add note to ticket...",
            required=False,
            max_length=2000,
            row=2,
        )
        self.add_item(self.note)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        if self.note.value and self.id.value:

            filter = {"_id": ObjectId(self.id.value)}
            doc = await TICKETS.find_one(filter)

            if not doc:
                await interaction.response.send_message(
                    "ticket with id {0} was not updated".format(self.id.value)
                )

                return

            update = {"$set": {"notes": self.note.value}}
            update["$set"]["updatedAt"] = datetime.now()

            await TICKETS.update_one(filter, update, upsert=False)

            html_hyperlink = nextcord.Embed(
                title=self.id.value,
                url="https://it.busseweb.com/tickets/editor/{}".format(self.id.value),
                description=doc["description"],
                colour=3447003,
            )

            await interaction.response.send_message(
                "{0} updated ticket with id {1}".format(
                    interaction.user.mention, self.id.value
                )
            )
            await interaction.followup.send(embed=html_hyperlink)

            return

        await interaction.response.send_message(
            "ticket with id {0} was not updated".format(self.id.value)
        )
