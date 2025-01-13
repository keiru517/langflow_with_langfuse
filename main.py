from langfuse.decorators import langfuse_context, observe
from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse()


@observe(as_type="generation")
def nested_generation():
    prompt = langfuse.get_prompt("Test")

    response = (
        openai.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=100,
            messages=[
                {"role": "system", "content": prompt.compile()},
                {
                    "role": "user",
                    "content": "Once upon a time in a galaxy far, far away...",
                },
            ],
            langfuse_prompt=prompt,
        )
        .choices[0]
        .message.content
    )
    print(response)


@observe()
def main():
    nested_generation()


main()
