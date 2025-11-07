import os
import json
from openai import OpenAI
from typing import Dict, List, Optional, Any

AI_INTEGRATIONS_OPENAI_API_KEY = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
AI_INTEGRATIONS_OPENAI_BASE_URL = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")

openai = OpenAI(
    api_key=AI_INTEGRATIONS_OPENAI_API_KEY,
    base_url=AI_INTEGRATIONS_OPENAI_BASE_URL
)

def parse_chat_to_decision(chat_message: str) -> Optional[Dict[str, Any]]:
    """
    Parse a natural language chat message into a structured decision prompt.
    
    Args:
        chat_message: User's natural language description of a decision
        
    Returns:
        Dictionary with 'scenario' and 'options' keys, or None if parsing fails
    """
    
    system_prompt = """You are a decision extraction assistant. Your job is to parse natural language descriptions into structured decision prompts.

Extract the following from the user's message:
1. scenario: A clear, concise description of the decision context
2. options: A list of 2-4 distinct choices or alternatives

Rules:
- If the user mentions specific options, extract them
- If options are implied but not explicit, infer reasonable alternatives
- Each option should be a short, actionable choice
- The scenario should be a question or statement of the decision problem

Return ONLY a JSON object with this exact structure:
{
    "scenario": "string describing the decision",
    "options": ["option 1", "option 2", ...]
}"""

    user_prompt = f"""Parse this decision description:

{chat_message}

Extract the scenario and options as JSON."""

    try:
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        response = openai.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=1024
        )
        
        content = response.choices[0].message.content
        if not content:
            return None
            
        parsed = json.loads(content)
        
        if "scenario" not in parsed or "options" not in parsed:
            return None
            
        if not isinstance(parsed["options"], list) or len(parsed["options"]) < 2:
            return None
            
        return {
            "scenario": parsed["scenario"],
            "options": parsed["options"][:4]
        }
        
    except Exception as e:
        print(f"Error parsing chat message: {e}")
        return None
