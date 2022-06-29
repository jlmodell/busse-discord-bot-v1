import httpx

new_tix_notifier_wh = "https://discord.com/api/webhooks/991543917910704189/7cHETlkf4_bYufx9KsUmhIiXi9k4yOCwATJpPkOVHLf6KtkVyVNbp6eelU86djx_-poO"


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
