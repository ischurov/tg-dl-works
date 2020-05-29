# based on: https://medium.com/better-programming/how-to-get-data-from-telegram-82af55268a4b
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

from pathlib import Path
from pytz import timezone
from configfile import phone, username, api_id, api_hash

import argparse
import datetime
import tzlocal


localzone = tzlocal.get_localzone()


def localdatetime(s):
    dt = datetime.datetime.strptime(s, "%Y-%m-%d")
    return localzone.localize(dt)


parser = argparse.ArgumentParser(description="Download pics from telegram")
parser.add_argument(
    "userlist",
    type=argparse.FileType("r"),
    help="List of telegram usersnames / ids (one per line)",
)
parser.add_argument("--todir", type=str, help="Directory to store results")

parser.add_argument(
    "--datefrom",
    type=localdatetime,
    help="Download images from this date only (YYYY-MM-DD)",
    default=None,
)

args = parser.parse_args()

basedir = Path(args.todir)
users = [line.strip() for line in args.userlist if line]

client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")

if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input("Enter the code: "))
    except SessionPasswordNeededError:
        client.sign_in(password=input("Password: "))

for user in users:
    try:
        print(f"Processing user")
        peer = client.get_entity(user)
        print(peer)
        userdir = basedir / user
        userdir.mkdir(parents=True, exist_ok=True)
        history = client(
            GetHistoryRequest(
                peer=peer,
                offset_id=0,
                offset_date=None,
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )

        for i, message in enumerate(history.messages):
            media = message.media
            if media:
                if args.datefrom and message.date < args.datefrom:
                    continue
                timestamp = message.date.astimezone(localzone).strftime(
                    "%Y-%m-%d-%H-%M-%S"
                )
                path = userdir / (timestamp + f"_{i}")

                path_created = client.download_media(message, file=path)
                print(path_created)

    except Exception as e:
        with open(basedir / "errors.log", "a") as f:
            print(f"Something wrong with user {user}", file=f)
            print(e, file=f)
