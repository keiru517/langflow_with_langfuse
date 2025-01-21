import json
import os
from langflow_api import run_flow, FLOW_ID, TWEAKS, APPLICATION_TOKEN
from langfuse.decorators import observe


def lambda_handler(event, context):
    body = event.get("body", "{}")
    data = json.loads(body)
    message = data.get("message", "Hello, AI!")

    response = run_flow(
        message=message,
        endpoint=FLOW_ID,
        output_type="chat",
        input_type="chat",
        tweaks=TWEAKS,
        application_token=APPLICATION_TOKEN,
    )
    answer = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": answer}),
    }
