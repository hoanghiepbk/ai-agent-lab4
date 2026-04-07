"""
agent.py — TravelBuddy AI Agent sử dụng LangGraph
Triển khai vòng lặp Agent với StateGraph:
  START → agent_node ↔ tool_node → END
Agent tự quyết định gọi tool nào, bao nhiêu lần.
"""

from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

from tools import search_flights, search_hotels, calculate_budget

# Load biến môi trường từ .env
load_dotenv()


# ============================================================================
# 1. Đọc System Prompt
# ============================================================================
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT: str = f.read()


# ============================================================================
# 2. Khai báo State — quản lý lịch sử hội thoại
# ============================================================================
class AgentState(TypedDict):
    """State chứa danh sách messages, tự động merge khi thêm message mới."""
    messages: Annotated[list, add_messages]


# ============================================================================
# 3. Khởi tạo LLM và Tools
# ============================================================================
tools_list: list = [search_flights, search_hotels, calculate_budget]
llm: ChatOpenAI = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, frequency_penalty=0.3)
llm_with_tools = llm.bind_tools(tools_list)


# ============================================================================
# 4. Agent Node — "Bộ não" của Agent
# ============================================================================
def agent_node(state: AgentState) -> dict:
    """
    Node chính: nhận messages, inject system prompt nếu chưa có,
    gọi LLM với tools binding, và log kết quả.
    """
    messages: list = state["messages"]

    # Inject system prompt nếu chưa có
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    # Gọi LLM
    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"🔧 Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"💬 Trả lời trực tiếp")

    return {"messages": [response]}


# ============================================================================
# 5. Xây dựng Graph
# ============================================================================
builder: StateGraph = StateGraph(AgentState)

# Thêm nodes
builder.add_node("agent", agent_node)

tool_node: ToolNode = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Khai báo edges — kết nối các node tạo thành flow
builder.add_edge(START, "agent")                              # Bắt đầu → Agent
builder.add_conditional_edges("agent", tools_condition)       # Agent → Tools (nếu có tool_calls) hoặc END
builder.add_edge("tools", "agent")                            # Tools xong → quay lại Agent

# Compile graph
graph = builder.compile()


# ============================================================================
# 6. Chat Loop — Giao diện tương tác với người dùng
# ============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy — Trợ lý Du lịch Thông minh")
    print("  Gõ 'quit' để thoát")
    print("=" * 60)

    # Lưu lịch sử hội thoại để agent nhớ context giữa các lượt
    chat_history: list = []

    while True:
        user_input: str = input("\nBạn: ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print("\n👋 Cảm ơn bạn đã sử dụng TravelBuddy! Chúc bạn có chuyến đi vui vẻ!")
            break

        if not user_input:
            continue

        print("\n🤔 TravelBuddy đang suy nghĩ...")

        # Thêm tin nhắn mới vào lịch sử
        chat_history.append(("human", user_input))

        try:
            result = graph.invoke({"messages": chat_history})
            # Cập nhật lại lịch sử từ kết quả graph (bao gồm cả tool calls & responses)
            chat_history = result["messages"]
            final = chat_history[-1]
            print(f"\nTravelBuddy: {final.content}")
        except Exception as e:
            print(f"\n❌ Đã xảy ra lỗi: {str(e)}")
            print("Vui lòng thử lại hoặc kiểm tra kết nối API.")
            # Xóa tin nhắn lỗi khỏi history để không ảnh hưởng lần sau
            chat_history.pop()
