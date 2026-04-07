"""
test_api.py — Sanity Check: Kiểm tra kết nối API trước khi bắt đầu bài lab.
Nếu in ra câu trả lời thành công, có thể bắt đầu bài tập.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
print(llm.invoke("Xin chào?").content)
