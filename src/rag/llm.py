import os
import time

from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError


MODEL_NAME = "gemini-2.5-flash"


class GeminiLLM:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(api_key=api_key)

    def generate(self, system_prompt, user_prompt):

        max_retries = 3

        for attempt in range(max_retries):

            try:

                response = self.client.models.generate_content(
                    model=MODEL_NAME,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.2,
                    ),
                )

                return response.text

            except ServerError:

                if attempt == max_retries - 1:
                    return (
                        "The scientific reasoning and evidence retrieval "
                        "completed successfully, but the language model is "
                        "temporarily unavailable. Please try again."
                    )

                time.sleep(2 * (attempt + 1))

            except ClientError as e:

                error_message = str(e)

                return (
                    "The environmental reasoning and scientific evidence "
                    "retrieval completed successfully, but the Gemini "
                    "language model could not generate the final response.\n\n"
                    f"API error: {error_message}"
                )

            except Exception as e:

                return (
                    "The environmental reasoning and scientific evidence "
                    "retrieval completed successfully, but an unexpected "
                    "language-model error occurred.\n\n"
                    f"Error: {str(e)}"
                )