import requests
import json
from llm.prompt_builder import build_prompt

def query_phi4(user_text: str, csv_data: str) -> dict:
    prompt = build_prompt(user_text, csv_data)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi4", "prompt": prompt, "stream": False}
    )
    response.raise_for_status()

    output = response.json()["response"]

    start = output.find("<json>")
    end = output.find("</json>")

    if start == -1 or end == -1:
        raise ValueError("Impossibile estrarre la risposta JSON dal modello")

    json_data = output[start + len("<json>"):end]
    return json.loads(json_data.strip())

