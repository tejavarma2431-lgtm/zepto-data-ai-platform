import os
import json
import requests
from typing import TypedDict

import chromadb
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, START, END


CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "zepto_policies"
MODEL_NAME = "all-MiniLM-L6-v2"

MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"


class GraphState(TypedDict):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


SYSTEM_PROMPT_TEMPLATE = """
Role:
You are Zepto's policy support assistant.

Context:
{context}

Task:
Answer the user's question using only the information provided in the context.

Format:
Return valid JSON with exactly these fields:
answer, sources, confidence.

Length:
Keep the answer concise and limited to 2-4 sentences.

Negative constraint:
Do not answer using information that is not present in the provided context.
If the context does not contain enough information to answer the question, clearly say that the information is not available in the provided context.

Few-shot example:

User:
How long does standard delivery take?

Context:
Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation.

Assistant:
{
    "answer": "Standard delivery takes 10 to 30 minutes after order confirmation.",
    "sources": ["doc_01"],
    "confidence": 1.0
}
"""


def call_real_llm(prompt: str):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is required when MOCK_LLM=0."
        )

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": os.getenv(
                "GROQ_MODEL",
                "llama-3.1-8b-instant"
            ),
            "messages": [
                {
                    "role": "system",
                    "content": prompt,
                }
            ],
            "temperature": 0,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = client.get_collection(
    COLLECTION_NAME
)


def classify_intent(state: GraphState):

    query = state["query"].lower()

    if MOCK_LLM:

        policy_keywords = [
            "delivery",
            "return",
            "refund",
            "membership",
            "tracking",
            "cancel",
            "gift card",
            "support hours",
        ]

        if any(
            keyword in query
            for keyword in policy_keywords
        ):
            intent = "policy_question"
        else:
            intent = "general_question"

        return {
            "intent": intent
        }

    prompt = f"""
Classify the following user query into exactly one category:

policy_question
general_question

A policy_question asks about Zepto policies such as:
- delivery
- returns
- refunds
- membership
- order tracking
- cancellation
- gift cards
- customer support

A general_question is anything unrelated to Zepto policies.

User query:
{state["query"]}

Return only valid JSON in this format:

{{
    "intent": "policy_question"
}}

or

{{
    "intent": "general_question"
}}
"""

    for attempt in range(3):

        try:

            raw_response = call_real_llm(prompt)

            parsed_response = json.loads(
                raw_response
            )

            intent = parsed_response["intent"]

            if intent not in [
                "policy_question",
                "general_question"
            ]:
                raise ValueError(
                    "Invalid intent returned by LLM."
                )

            return {
                "intent": intent
            }

        except Exception:

            if attempt == 2:
                raise RuntimeError(
                    "ERROR: Intent classification "
                    "failed after 3 attempts."
                )


def retrieve_and_answer(state: GraphState):

    query = state["query"]

    query_embedding = model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    top_document = results["documents"][0][0]

    top_source = results["metadatas"][0][0]["source"]

    snippet = top_document[:200]

    if MOCK_LLM:

        answer = (
            "Based on the retrieved context: "
            f"{snippet}"
        )

        return {
            "answer": answer,
            "sources": [
                top_source.replace(".txt", "")
            ],
            "confidence": 1.0
        }

    context_parts = []

    for i in range(3):

        document = results["documents"][0][i]

        source = results["metadatas"][0][i]["source"]

        context_parts.append(
            f"Source: {source}\n"
            f"Content: {document}"
        )

    context = "\n\n".join(context_parts)

    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        context=context
    )

    for attempt in range(3):

        try:

            raw_response = call_real_llm(
                prompt
            )

            parsed_response = json.loads(
                raw_response
            )

            validated = AskResponse.model_validate(
                parsed_response
            )

            return {
                "answer": validated.answer,
                "sources": validated.sources,
                "confidence": validated.confidence
            }

        except Exception as error:

            if attempt == 2:

                return {
                    "answer": (
                        "ERROR: The real LLM response "
                        "failed validation."
                    ),
                    "sources": [],
                    "confidence": 0.0
                }

    return {
        "answer": "ERROR: Unable to generate response.",
        "sources": [],
        "confidence": 0.0
    }


def direct_answer(state: GraphState):

    if MOCK_LLM:

        return {
            "answer": (
                "I can only answer questions about "
                "Zepto policies right now."
            ),
            "sources": [],
            "confidence": 1.0
        }

    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        context=(
            "No policy context was retrieved because "
            "this is a general question."
        )
    )

    for attempt in range(3):

        try:

            raw_response = call_real_llm(
                prompt
            )

            parsed_response = json.loads(
                raw_response
            )

            validated = AskResponse.model_validate(
                parsed_response
            )

            return {
                "answer": validated.answer,
                "sources": [],
                "confidence": validated.confidence
            }

        except Exception:

            if attempt == 2:

                return {
                    "answer": (
                        "ERROR: The real LLM response "
                        "failed validation."
                    ),
                    "sources": [],
                    "confidence": 0.0
                }

    return {
        "answer": "ERROR: Unable to generate response.",
        "sources": [],
        "confidence": 0.0
    }


def route_by_intent(state: GraphState):

    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


graph_builder = StateGraph(GraphState)


graph_builder.add_node(
    "classify_intent",
    classify_intent
)

graph_builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

graph_builder.add_node(
    "direct_answer",
    direct_answer
)


graph_builder.add_edge(
    START,
    "classify_intent"
)


graph_builder.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    {
        "retrieve_and_answer":
            "retrieve_and_answer",

        "direct_answer":
            "direct_answer",
    }
)


graph_builder.add_edge(
    "retrieve_and_answer",
    END
)

graph_builder.add_edge(
    "direct_answer",
    END
)


graph = graph_builder.compile()


app = FastAPI(
    title="Zepto Support Assistant"
)


@app.post(
    "/ask",
    response_model=AskResponse
)
def ask(request: AskRequest):

    result = graph.invoke(
        {
            "query": request.query
        }
    )

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )