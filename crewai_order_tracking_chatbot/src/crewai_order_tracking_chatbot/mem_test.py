from mem0 import Memory
from dotenv import load_dotenv

load_dotenv()
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "chatbot_memory",
            "path": "./chroma_db",
        },
    },
}

memory = Memory.from_config(config)

relevant_info=memory.search(query="Tell me the details of order number 936848", limit=6, user_id="default_user")
context_lst=[entry["memory"] for entry in relevant_info['results']]

for context in context_lst:
    print(context)