from groq import Groq

from app.prompts import system_prompt, user_prompt
from app.settings import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY,
)

class GroqClient:
    def __init__(
        self,
        model,
        temperature=1.0,
    ):
        self.model = model
        self.temperature = temperature

    def predict(self, context):
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt.format(content=context["content"], question=context["question"])},
            ],
            model=self.model,
            temperature=self.temperature,
            response_format={"type": "json_object"},
        )

        content = chat_completion.choices[0].message.content

        return content