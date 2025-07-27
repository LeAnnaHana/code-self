import logging
import os
from openai import OpenAI

from .utils import get_log_handler

logger = logging.getLogger(__name__)
logger.addHandler(get_log_handler())

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default=None)

def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY)

client = get_openai_client()

def openai_chat_complete(messages=(), model="gpt-4o-mini", raw=False):
    logger.info("Chat complete for {}".format(messages))
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    if raw:
        return response.choices[0].message
    output = response.choices[0].message
    logger.info("Chat complete output: ".format(output))
    return {
        "role": "assistant",
        "content": str(output.content)
    }

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def gen_doc_prompt(docs):
    """
    Document:
    Title: Uong atiso ...
    Content: ....
    """
    doc_prompt = ""
    for doc in docs:
        title = doc.get("title", doc.get("document_title", ""))
        doc_prompt += f"Title: {title} \n Content: {doc['content']} \n"

    return "Document: \n + {}".format(doc_prompt)
