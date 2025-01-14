import requests
from typing import Optional
import os

from dotenv import load_dotenv

from langfuse.decorators import langfuse_context, observe
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
    "ChatInput-jJLjK": {
        "files": "",
        "background_color": "",
        "chat_icon": "",
        # "input_value": "",
        "sender": "User",
        "sender_name": "User",
        "session_id": "",
        "should_store_message": True,
        "text_color": "",
    },
    "OpenAIModel-h1Tvh": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "input_value": "",
        "json_mode": False,
        "max_tokens": None,
        "model_kwargs": {},
        "model_name": "gpt-4o-mini",
        "openai_api_base": "",
        "output_schema": {},
        "seed": 1,
        "stream": False,
        "system_message": "",
        "temperature": 0.1,
    },
    "ChatOutput-hqnWM": {
        "background_color": "",
        "chat_icon": "",
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": "",
        "should_store_message": True,
        "text_color": "",
    },
}


@observe(as_type="generation")
def run_flow(
    message: str,
    endpoint: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        # get prompt from langfuse
        prompt = langfuse.get_prompt("Test")
        langfuse_context.update_current_observation(prompt=prompt)

        # update the system message with the prompt
        tweaks["OpenAIModel-h1Tvh"]["system_message"] = prompt.compile()
        payload["tweaks"] = tweaks

    if application_token:
        headers = {
            "Authorization": "Bearer " + application_token,
            "Content-Type": "application/json",
        }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


@observe()
def main():
    response = run_flow(
        message="",  # message to send to the flow
        endpoint=FLOW_ID,
        output_type="chat",
        input_type="chat",
        tweaks=TWEAKS,
        application_token=APPLICATION_TOKEN,
    )
    answer = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    print(answer)


if __name__ == "__main__":
    main()
