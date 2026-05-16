import vk_api
import random
import json

from vk_api.longpoll import VkLongPoll, VkEventType

from config import TOKEN, ADMIN_ID
from quiz import start_quiz, check_answer
from admin import handle_admin

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def send(user_id, text, keyboard=None, attachment=None):
    vk.messages.send(
        user_id=user_id,
        message=text,
        keyboard=keyboard,
        attachment=attachment,
        random_id=random.randint(1, 99999999)
    )


print("BOT STARTED")

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        user_id = event.user_id
        text = event.text.lower() if event.text else ""

        payload = None
        if hasattr(event, 'message') and event.message and "payload" in event.message:
            try:
                payload = json.loads(event.message["payload"])
            except:
                pass

        if handle_admin(send, user_id, text):
            continue

        if payload and payload.get("cmd") == "start":
            start_quiz(send, user_id)
            continue

        if text in ["начать игру", "начать", "start", "/start"]:
            start_quiz(send, user_id)
            continue

        if text:
            check_answer(send, user_id, text)