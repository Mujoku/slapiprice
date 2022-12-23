import os
import pandas as pd
from preprocess_data import prd, prd2
from matching import match_deals
from db_connector import insert_deals, get_deals
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from prep_msg import msg_blocks

# ? Slack Bolt API

load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"])
DB = get_deals()

# ? Handle message event on main thread


@app.event("message")
def handle_message_events(ack, say, body, logger, event):
    thread_id = event["ts"]
    logger.info(f"Thread ID: {thread_id}")
    # user_id = event["user"]
    # message_text = f"Ok <@{user_id}>, done! 👍 "

    test_channel = event["channel"] == "x"
    zakamarki_channel = event["channel"] == "xx"
    prepaid_channel = event["channel"] == "xxx"
    add_test_channel = event["channel"] == "xxxx"
    slack_event_body = pd.json_normalize(body)
    offer = slack_event_body["event.text"].loc[0]
    deals = offer.splitlines()
    check = None

    try:
        check = prd(deals)
    except ValueError:
        check = prd2(deals)

    logger.info(f"Request body: {body}")
    logger.info(f"Request deals: {deals}")

    if event.get("thread_ts") is None:
        if zakamarki_channel:
            insert_deals(check)
            ack()

        elif test_channel or add_test_channel:
            print(thread_id)
            result = match_deals(DB, prd2(deals))
            result["currency"] = result["prices"].str.extract("([A-z]\w+)")
            result["prices"] = result["prices"].str.extract(
                "(\d+[.]\d+)").astype(float)
            result = result.sort_values("prices", axis=0, ascending=True)
            answer = msg_blocks(result, thread_id)
            ack()
            say(text=answer, thread_ts=thread_id)
        elif prepaid_channel:
            logger.info("TODO")
    else:
        logger.info("Komentarz lub inny kanał.")


@app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
