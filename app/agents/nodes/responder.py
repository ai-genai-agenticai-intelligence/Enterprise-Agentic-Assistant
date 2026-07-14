import logfire

from app.agents.state import AgentState
from app.gateway import get_langchain_llm


llm = get_langchain_llm(feature="responder")


def generate_node(state: AgentState):
    """Answer using retrieved documentation and the conversation history."""
    query = state["current_query"]
    history = "\n".join(
        f"{'User' if message['role'] == 'user' else 'Assistant'}: {message['content']}"
        for message in state["messages"][:-1]
    )
    user_message = state["messages"][-1]["content"] if state["messages"] else ""

    if query == "CONVERSATIONAL":
        prompt = (
            "You are a friendly and helpful Enterprise AI Assistant. Answer the user's "
            "latest message using the conversation history.\n\n"
            f"CONVERSATION HISTORY:\n{history}\n\nLATEST MESSAGE:\n{user_message}"
        )
    else:
        context = "\n\n".join(state["documents"])[:25000]
        prompt = (
            "You are a Senior Technical Architect. Answer using the technical context. "
            "If the context does not contain the answer, say so.\n\n"
            f"TECHNICAL CONTEXT:\n{context}\n\nCONVERSATION HISTORY:\n{history}\n\n"
            f"USER QUESTION:\n{user_message}"
        )

    with logfire.span("LLM Synthesis"):
        try:
            content = llm.invoke(prompt).content
            return {
                "final_answer": content,
                "status": "Response generated.",
                "plan": state["plan"],
                "messages": [{"role": "assistant", "content": content}],
            }
        except Exception as exc:
            logfire.error(f"LLM generation failed: {exc}")
            raise
