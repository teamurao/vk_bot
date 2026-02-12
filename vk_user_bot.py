import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os

load_dotenv()

vk_session = vk_api.VkApi(token=os.getenv("TOKEN"))
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)
print("bot started")

def send_some_msg(id, some_text):
    vk_session.method(
        "messages.send",
        {"user_id": id, "message": some_text, "random_id": 0},
    )

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            print(f"event: user_id={id}, text={event.text!r}")
            if msg == "привет":
                send_some_msg(id, "привет-привет!")
