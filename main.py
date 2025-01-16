from fastapi import FastAPI
from langflow_api import run_flow, FLOW_ID, TWEAKS, APPLICATION_TOKEN
from langfuse.decorators import observe

app = FastAPI()


@app.post("/chat")
@observe(as_type="generation")
async def chat(message: str):
    response = run_flow(
        message=message,
        endpoint=FLOW_ID,
        output_type="chat",
        input_type="chat",
        tweaks=TWEAKS,
        application_token=APPLICATION_TOKEN,
    )
    answer = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    return {"response": answer}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
