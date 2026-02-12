import os

from dotenv import load_dotenv
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

load_dotenv()

TOKEN = os.getenv('VK_BOT_TOKEN') or os.getenv('TOKEN')
GROUP_ID = int(os.getenv('VK_GROUP_ID', '0'))


def build_answer(text: str) -> str:
    normalized = text.strip().lower()

    if normalized == 'привет':
        return 'Привет! Я бот сообщества VK.'
    if normalized == 'помощь':
        return 'Команды: привет, помощь'
    return f'Вы написали: {text}'


vk_session = VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
print(f'bot started, group_id={GROUP_ID}')

for event in longpoll.listen():
    if event.type != VkBotEventType.MESSAGE_NEW:
        continue

    message = event.object['message']
    peer_id = message['peer_id']
    from_id = message['from_id']
    text = message.get('text', '')
    print(f'event: peer_id={peer_id}, from_id={from_id}, text={text!r}')

    # чтобы бот не отвечал в беседы, только в личку
    if peer_id != from_id:
        continue

    answer = build_answer(text)
    vk.messages.send(peer_id=peer_id, random_id=0, message=answer)


