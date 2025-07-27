import logging
from time import sleep
from celery import shared_task

from .cache import get_conversation_id
from .models import Document, ChatConversation, convert_conversation_to_openai_messages, load_conversation
from .brain import openai_chat_complete, get_embedding, gen_doc_prompt
from .configs import DEFAULT_COLLECTION_NAME
from .utils import get_log_handler
from .vectorize import search_vector

logger = logging.getLogger(__name__)
logger.addHandler(get_log_handler())


def create_or_update_chat_conversation(bot_id, user_id, message):
    # Step 1: Create a new ChatConversation instance
    conversation_id = get_conversation_id(bot_id, user_id)

    new_conversation = ChatConversation(
        conversation_id=conversation_id,
        bot_id=bot_id,
        user_id=user_id,
        message=message,
        is_request=True,
        completed=False,
    )
    # Step 4: Save the ChatConversation instance
    new_conversation.save()

    logger.info(f"Create message for conversation {conversation_id}")

    return conversation_id


def generate_conversation_text(conversations):
    conversation_text = ""
    for conversation in conversations:
        role = "assistant" if not conversation.is_request else "user"
        content = str(conversation.message)
        conversation_text += f"{role}: {content}\n"
    return conversation_text


def detect_user_intent(conversation_id, message):
    # Load history conversation
    conversations = load_conversation(conversation_id)
    # Convert history to list messages
    history_messages = generate_conversation_text(list(conversations)[:-1])
    logger.info(f"History messages: {history_messages}")
    # Update documents to prompt
    user_prompt = f"""
    Given following conversation and follow up question, rephrase the follow up question to a standalone question in Vietnamese.

    Chat History:
    {history_messages}

    Original Question: {message}

    Answer:
    """
    openai_messages = [
        {"role": "system", "content": "You are an amazing virtual assistant"},
        {"role": "user", "content": user_prompt}
    ]
    logger.info(f"Rephrase input messages: {openai_messages}")
    # call openai
    rephrase_response = openai_chat_complete(openai_messages)
    # return intent user
    return rephrase_response["content"]


@shared_task()
def answer_user_request(bot_id, user_id, message):
    # Update chat conversation
    conversation_id = create_or_update_chat_conversation(bot_id, user_id, message)

    # Sub task
    user_intent = detect_user_intent(conversation_id, message)
    logger.info(f"User intent: {user_intent}")

    # Embedding text
    vector = get_embedding(user_intent)
    logger.info(f"Get vector: {user_intent}")

    # Search document
    top_docs = search_vector(DEFAULT_COLLECTION_NAME, vector, 5)
    logger.info(f"Top docs: {top_docs}")

    # Convert history to list messages
    conversations = load_conversation(conversation_id)
    openai_messages = convert_conversation_to_openai_messages(conversations)

    # Update documents to prompt
    openai_messages.insert(
        len(openai_messages) - 1,
        {"role": "user", "content": gen_doc_prompt(top_docs)}
    )

    logger.info(f"Openai messages: {openai_messages}")

    # LLM generate answer
    assistant_answer = openai_chat_complete(openai_messages)
    logger.info(f"Openai reply: {assistant_answer}")
    update_answer = ChatConversation(
        conversation_id=conversation_id,
        bot_id=bot_id,
        user_id=user_id,
        message=assistant_answer,
        is_request=False,
        completed=True,
    )
    update_answer.save()
    logger.info(f"Save bot answer to database successfully")

    return assistant_answer
