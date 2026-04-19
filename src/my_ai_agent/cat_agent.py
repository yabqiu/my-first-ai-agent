from os import path

from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, ToolMessage

from my_ai_agent.tools import read_file, write_file, web_fetch
from my_ai_agent.telegram import send_message_to_telegram_bot

load_dotenv()

workspace = path.abspath(path.join(path.dirname(__file__), "../../workspace"))

cat_agent = create_agent(
    model="bedrock:us.anthropic.claude-haiku-4-5-20251001-v1:0",
    # model="ollama:gemma4:e4b",
    tools=[read_file, write_file, web_fetch, send_message_to_telegram_bot],
    system_prompt=f"""Your are a good assistant to help seek new cats from a shelter website
    
    all file operations are limited in folder {workspace} 
    """
)

cat_list_url = ("https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals2.aspx?species=Cat&sex=A"
                "&agegroup=All&location=&site=&onhold=A&orderby=Name&colnum=3&authkey="
                "u1eehnph8i3tg2yldjiy4bgv5uiw3i6wgnh8wudohp8uckr0hr&recAmount=&detailsInPopup=No&featuredPet=Include,")
task_prompt = f"""fetch cat list from url {cat_list_url}

Each cat entry on this page contains:
 - Cat URL
 - Cat ID (It can be extract from Cat URL with `id` query parameter)
 - Name
 - Photo
 - Breed
 - Age
 - Sex (Male/Neutered or Female/Spayed)
 
For each found new cat, send a Telegram message to Bot 'Seek Cat' in HTML in following `Telegram message format`

### Telegram message format

```html
<b>🐱 New Cat Found!</b>
<b>Name:</b> {{Name}}
<b>Sex:</b> {{Sex}}
<b>Breed:</b> {{Breed}}
<b>Age:</b> {{Age}}
{{Photo}}
<a href="{{Cat URL}}">View Full Profile</a>
```

Use local file 'found_cat_ids.txt' to store Cat IDs and determine if new cat.
"""

for chunk in cat_agent.stream(
        {"messages": [{"role": "user", "content": task_prompt}]},
        stream_mode="updates"
):
    messages = chunk.get('model', chunk.get('tools'))['messages']
    for message in messages:
        if isinstance(message, AIMessage):
            print("AIMessage----")
            if len(message.content) > 0:
                print(message.content)
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    print("tool: ", tool_call['name'], tool_call['id'], " args: omitted")
        elif isinstance(message, ToolMessage):
            print("ToolMessage---")
            print("tool: ", message.name, message.tool_call_id)
        else:
            print(type(message), "----")
            print(message.content)