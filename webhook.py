import httpx
from constants import DISCORD_WEBHOOK_URL

new_tix_notifier_wh = DISCORD_WEBHOOK_URL


def send_message(message: str) -> None:
    httpx.post(new_tix_notifier_wh, json={"content": message})


if __name__ == "__main__":
    msg = """

**New Ticket**

__ID__: ```{}```
__Submitted By__: ```{}```
__Description__: ```{}```

""".format(
        "abcdefghijk123456789", "John Doe", "This is a test ticket"
    )

    send_message(msg)
