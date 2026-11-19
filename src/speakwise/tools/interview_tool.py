
from google.genai import types

from speakwise.llm_client import client, MODEL
from speakwise.schemas.tools.interview import InterviewResult


SYSTEM_PROMPT = """
You are the Interview Practice Tool of SpeakWise AI.

Your responsibility is to help users practice and improve
their interview communication.

You support two modes:

1. ask_question:
   - Generate a relevant interview question.
   - Consider the candidate's role and experience level.
   - Do not provide the answer.
   - Leave feedback, improved_answer, strengths and
     areas_to_improve empty.
   - Provide an empty follow_up_question.

2. evaluate_answer:
   - Evaluate the candidate's answer.
   - Assess relevance, clarity, structure and communication.
   - Identify strengths and areas for improvement.
   - Provide constructive feedback.
   - Generate an improved sample answer.
   - Suggest a relevant follow-up interview question.

Additional instructions:
- Be constructive and realistic.
- Do not invent candidate experience or achievements.
- Preserve the candidate's actual experience in improved answers.
- Never confuse the two modes.

Return a structured response matching the provided schema.
"""


def conduct_interview(
    role: str,
    mode: str,
    question: str = "",
    candidate_answer: str = "",
    experience_level: str = "Entry level"
) -> InterviewResult:

    if not role or not role.strip():
        raise ValueError("Interview role cannot be empty")

    if mode not in ["ask_question", "evaluate_answer"]:
        raise ValueError("Invalid interview mode")

    if mode == "evaluate_answer" and not candidate_answer.strip():
        raise ValueError("Candidate answer cannot be empty")

    if mode == "evaluate_answer" and not question.strip():
        raise ValueError("Interview question cannot be empty")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"""
            MODE:
            {mode}

            JOB ROLE:
            {role}

            EXPERIENCE LEVEL:
            {experience_level}

            INTERVIEW QUESTION:
            {question}

            CANDIDATE ANSWER:
            {candidate_answer}
            """,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=InterviewResult,
                temperature=0.4
            )
        )

        if response.parsed is not None:
            return InterviewResult.model_validate(response.parsed)

        if response.text:
            return InterviewResult.model_validate_json(response.text)

        raise ValueError("Gemini returned an empty response")

    except ValueError:
        raise

    except Exception as e:
        raise RuntimeError(
            f"Interview practice failed: {str(e)}"
        ) from e
