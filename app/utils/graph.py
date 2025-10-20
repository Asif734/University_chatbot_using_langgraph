from typing import List, Any, Literal, Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
from app.services.retriever_service import retriever
from app.core.config import settings

# -----------------------------
# ⚙️ Initialize LLM
# -----------------------------
llm = OllamaLLM(model=settings.LLM_MODEL, temperature=0.7)

# -----------------------------
# 🧠 Define RAG State Schema (TypedDict)
# -----------------------------
class RAGState(TypedDict):
    question: Annotated[str, "Input"]     # read-only input
    context: str | None
    docs: List[Any] | None
    answer: str | None
    route: Literal["greeting", "rag"] | None

# -----------------------------
# 💬 Greeting Dictionary
# -----------------------------
GREETING_RESPONSES = {
    "hello": "Hello there! 👋 How can I help you today?",
    "hi": "Hi! 😊 What would you like to know?",
    "hey": "Hey! 👋 How are you doing?",
    "good morning": "Good morning! ☀️ Hope your day is going well!",
    "good afternoon": "Good afternoon! 🌞 How can I assist you?",
    "good evening": "Good evening! 🌙 What brings you here today?",
    "how are you": "I'm just a bunch of algorithms, but I'm feeling great! 😄 How about you?",
    "what's up": "Not much, just waiting to chat with you! 🤖",
}

def detect_greeting(q: str) -> bool:
    q = q.lower().strip()
    return any(key in q for key in GREETING_RESPONSES.keys())

def get_greeting_response(q: str) -> str:
    q = q.lower()
    for key, resp in GREETING_RESPONSES.items():
        if key in q:
            return resp
    return "Hey there! 😊 How can I help you today?"

# -----------------------------
# 🧩 Helper
# -----------------------------
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# -----------------------------
# 📜 Prompt
# -----------------------------
prompt = PromptTemplate.from_template(
    """Use the following context to answer the question.
If it's small talk, respond naturally and friendly.
Answer in the same language as the question.
If you don't know, say 'I don’t know' — do not fabricate.

Context: {context}
Question: {question}
Answer:"""
)

# -----------------------------
# 🧩 Node Functions
# -----------------------------
def router(state: RAGState) -> RAGState:
    if detect_greeting(state["question"]):
        state["route"] = "greeting"
    else:
        state["route"] = "rag"
    return state

def greeting_agent(state: RAGState) -> RAGState:
    state["answer"] = get_greeting_response(state["question"])
    return state

def retrieve(state: RAGState) -> RAGState:
    docs = retriever.invoke(state["question"])
    state["docs"] = docs
    state["context"] = format_docs(docs)
    return state

def generate(state: RAGState) -> RAGState:
    response = (prompt | llm | StrOutputParser()).invoke({
        "context": state["context"],
        "question": state["question"],
    })
    state["answer"] = response
    return state

# -----------------------------
# 🧭 Build Graph
# -----------------------------
graph = StateGraph(RAGState)
graph.add_node("router", router)
graph.add_node("greeting_agent", greeting_agent)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

# routing logic
def route_decision(state: RAGState):
    return "greeting_agent" if state["route"] == "greeting" else "retrieve"

graph.set_entry_point("router")
graph.add_conditional_edges("router", route_decision)
graph.add_edge("greeting_agent", END)
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

# -----------------------------
# ✅ Compile
# -----------------------------
rag_graph = graph.compile()
