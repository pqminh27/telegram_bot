import requests
from config import URL
class TelegramBot:

    def __init__(self):
        self.chat_id = None
        self.text = None
        self.first_name = None
        self.last_name = None
        self.incoming_message_text = None
        self.outgoing_message_text = None


    def parse_webhook_data(self, data):
        """
        Parses Telegram JSON request from webhook and sets fields for conditional actions
        Args:
            data:str: JSON string of data
        """
        message = data['message']
        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        self.last_name = message['from']['last_name']

    def action(self):
        """
        Conditional actions based on set webhook data.
        Returns:
            bool: True if the action was completed successfully else false
        """
        success = None

        if self.incoming_message_text == '/hello':
            self.outgoing_message_text = "Hello {} {}!".format(self.first_name, self.last_name)
            success = self.send_message()
        
        if self.incoming_message_text == '/rad':
            self.outgoing_message_text = '🤙'
            success = self.send_message()
        
        return success


    def send_message(self):
        """
        Sends message to Telegram servers.
        """
        res = requests.get(URL.format(self.chat_id, self.outgoing_message_text))
        return True if res.status_code == 200 else False
    

    @staticmethod
    def init_webhook(url):
        """
        Initializes the webhook
        Args:
            url:str: Provides the telegram server with an endpoint for webhook data
        """
        requests.get(url)