import logging
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader
)

from llama_index.llms import OpenAI
from llama_index.memory import ChatMemoryBuffer
from .utils import get_log_handler

logger = logging.getLogger(__name__)
logger.addHandler(get_log_handler())

class UserAgent:
    def __init__(self, bot_id, user_id):
        self.bot_id = bot_id
        self.user_id = user_id
        
        self.llm = OpenAI()
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        
        self.documents = SimpleDirectoryReader('knowledge_base').load_data()
        self.index = VectorStoreIndex.from_documents(self.documents)
        self.query_engine = self.index.as_query_engine()

    def handle_message(self, message):
        try:
            self.memory.put(message, is_user=True)
            
            response = self.query_engine.query(
                message,
                chat_history=self.memory.get_all()
            )
            
            self.memory.put(str(response), is_user=False)
            
            return {
                "status": "success",
                "message": str(response)
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "status": "error", 
                "message": "Sorry, I encountered an error processing your message."
            }

    def get_user_id(self):
        return self.user_id

    def get_bot_id(self):
        return self.bot_id

def main():
    # Initialize the agent
    bot_id = "test_bot"
    user_id = "test_user"
    agent = UserAgent(bot_id, user_id)
    
    # Test messages
    test_messages = [
        "Hello, who are you?",
        "What products do you have?",
        "Can you tell me about your pricing?"
    ]
    
    # Process each test message
    for message in test_messages:
        print(f"\nUser: {message}")
        response = agent.handle_message(message)
        print(f"Bot: {response['message']}")
        print(f"Status: {response['status']}")

if __name__ == "__main__":
    main()
