import logging
import telebot
import os
# from dotenv import load_dotenv

# load_dotenv()

TOKEN = os.getenv('TELEGRAM_API_TOKEN')
CIDS = os.getenv('TELEGRAM_CHAT_ID')


class Messenger:
    """
    Need to figure out how polling and sending messages can work together.
    With `import threading`?
    Example: https://gist.github.com/David-Lor/37e0ae02cd7fb1cd01085b2de553dde4
    """
    def __init__(self, token: str = TOKEN, cids: str = CIDS):
        self.cids = self._cids_parser(cids)
        self.bot = telebot.TeleBot(token)
        self._bot_actions()

    def _cids_parser(self, cids):
        return [int(cid) for cid in cids.split(',')]

    def _bot_actions(self):
        @self.bot.message_handler(commands=['start'])
        def _handle_start_message(message):
            self.bot.reply_to(message, "Hi there!")
            logging.info(f'New chat registered with id: {message.chat.id}')

        @self.bot.message_handler(commands=['end'])
        def _handle_end_message(message):
            self.bot.reply_to(message, "You've been removed")
            logging.info(f'Chat id {message.chat.id} has requested to end notifications')

    def send_notification(self, msg: str):
        for cid in self.cids:
            self.bot.send_message(chat_id=cid, text=msg)

    def start_polling(self):
        self.bot.infinity_polling()
