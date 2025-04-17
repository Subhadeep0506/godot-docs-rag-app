import requests
from typing import Optional, Dict, Any
import json
import os


async def generate_response(
    query: str,
    session_id: str,
    model_name: str = "command-a-03-2025",
    category: str = "tutorials",
    sub_category: Optional[str] = "2d",
    temperature: float = 0.7,
    top_k: int = 10,
    memory_service: str = "astradb",
) -> Dict[str, Any]:
    """
    Send a query to the RAG API endpoint and return the response.

    Args:
        query (str): The user's query text
        session_id (str): Unique session identifier
        model_name (str): Name of the LLM model to use
        category (str): Category for the query
        sub_category (Optional[str]): Sub-category for the query
        temperature (float): Temperature parameter for LLM
        top_k (int): Number of top documents to retrieve
        memory_service (str): Memory service to use
        api_url (str): Base URL of the API

    Returns:
        Dict[str, Any]: API response
    """
    payload = {
        "query": query,
        "session_id": session_id,
        "state": {
            "model_name": model_name,
            "category": category,
            "sub_category": sub_category,
            "temperature": temperature,
            "top_k": top_k,
            "memory_service": memory_service,
        },
    }

    try:
        response = requests.post(
            f"{os.getenv('FASTAPI_API_URL')}/query",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return dict(response.json())["response"]
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse response: {str(e)}"}
