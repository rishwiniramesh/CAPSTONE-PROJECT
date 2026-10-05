import base64
import mimetypes
import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()


class MultimodalAI:
    """
    Hugging Face multimodal AI service.

    It can analyze:
    - project text
    - PDFs converted to text
    - images
    - diagrams
    - screenshots
    """

    def __init__(self):

        token = os.getenv("HF_TOKEN")

        if not token:
            raise RuntimeError(
                "HF_TOKEN was not found in .env"
            )

        self.client = InferenceClient(
            api_key=token,
            provider="auto",
        )

        # Current VLM example from Hugging Face docs.
        # Provider can be changed later if needed.
        self.model = os.getenv(
            "HF_MODEL",
            "zai-org/GLM-5.3-Flash:baseten",
        )

    def _image_to_data_url(
        self,
        image_bytes: bytes,
        filename: str,
    ) -> str:

        mime_type, _ = mimetypes.guess_type(filename)

        if mime_type is None:
            mime_type = "image/png"

        encoded_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        return (
            f"data:{mime_type};base64,{encoded_image}"
        )

    def analyze_project(
        self,
        project_text: str,
        images: list[tuple[str, bytes]] | None = None,
    ) -> str:

        project_text = project_text[:50000]

        prompt = f"""
You are an AI-based software project management assistant.

Analyze the supplied software project.

PROJECT DOCUMENTATION
=====================
{project_text}

Your job is to understand the project and produce a useful
project-management analysis.

Return the result using these sections:

# 1. Project Overview
Explain what the project is and its purpose.

# 2. Main Objectives
List the major objectives.

# 3. Main Modules
Identify the major software modules/components.

# 4. Functional Requirements
Extract the important functional requirements.

# 5. Suggested Development Tasks
Convert the requirements and project information into
practical software-development tasks.

For each task provide:
- Task
- Priority
- Reason

# 6. Project Risks
Identify likely technical, security, schedule,
requirement, or implementation risks.

For each risk provide:
- Risk
- Severity
- Recommendation

# 7. Missing or Unclear Requirements
Identify information that is incomplete, ambiguous,
or missing.

# 8. Recommended Next Steps
Give a practical sequence of actions for the development team.

IMPORTANT:
Use only information supported by the uploaded project.
Do not invent facts.
Clearly mark assumptions when necessary.
"""

        content = [
            {
                "type": "text",
                "text": prompt,
            }
        ]

        if images:

            for filename, image_bytes in images[:5]:

                image_url = self._image_to_data_url(
                    image_bytes,
                    filename,
                )

                content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    }
                )

                content.append(
                    {
                        "type": "text",
                        "text": (
                            f"Analyze this project image: "
                            f"{filename}"
                        ),
                    }
                )

        response = (
            self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
                temperature=0.2,
                max_tokens=4000,
            )
        )

        return response.choices[0].message.content