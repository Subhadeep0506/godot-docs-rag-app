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
            timeout=60,
        )
        response.raise_for_status()
        return dict(response.json())["response"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}") from e
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse API response: {str(e)}") from e


async def generate_reddit_response(
    query: str,
    session_id: str,
    reddit_username: str,
    relevance: str,
    model_name: str = "command-a-03-2025",
    category: str = None,
    sub_category: Optional[str] = None,
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
            "reddit_username": reddit_username,
            "relevance": relevance,
        },
    }

    try:
        response = requests.post(
            f"{os.getenv('FASTAPI_API_URL')}/query/reddit",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60,
        )
        response.raise_for_status()
        return dict(response.json())["response"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}") from e
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse API response: {str(e)}") from e
