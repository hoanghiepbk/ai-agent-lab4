# TravelBuddy AI Agent 🌍✈️

TravelBuddy là một "Trợ lý Du lịch Thông minh" được xây dựng trong khuôn khổ **Lab 4**, sử dụng mô hình ngôn ngữ lớn (LLM) và nhận thức ngữ cảnh thông qua framework vòng lặp của **LangChain** và **LangGraph**.

Mục tiêu cốt lõi của TravelBuddy không chỉ là trả lời các câu hỏi chatbot rời rạc, mà là thể hiện khả năng "suy nghĩ" thực thụ: Agent có thể **HÀNH ĐỘNG đa bước (Multi-Step Tool Chaining)** — tự động tìm vé máy bay, tính toán chênh lệch ngân sách và tra cứu khách sạn phù hợp để tung ra một gợi ý trọn gói tối ưu cho khách hàng.

---

## 🛠 Cấu trúc Dự án

Dự án có kiến trúc xoay quanh LangGraph `StateGraph`, qua đó Agent tự động định hướng cách dùng công cụ trong quá trình trao đổi với user.

```text
lab4_agent/
├── agent.py               # Node trung tâm của đồ thị (LangGraph StateGraph & Chat loop)
├── tools.py               # 3 "Tay chân" công cụ của Agent (Mock Database, hàm xử lý giá)
├── system_prompt.txt      # Định hình logic cốt lõi ("Não bộ") với Persona và Constraints
├── .env                   # Tệp chứa OpenAI API Key bảo mật
├── test_api.py            # Sanity checks cho kết nối LLM
├── test_results.md        # Logs test case để đối chiếu đầu ra
└── requirements.txt       # Danh sách thư viện liên quan
```

### 🧩 3 Công Cụ Cốt Lõi (Tools)
Agent được tích hợp sẵn 3 chức năng độc lập nhưng mang **tính mắt xích** với nhau:
1. `search_flights`: Tìm tuyến bay giữa các thành phố Việt Nam, tự động gợi ý chuyến bay ngược mều rỗng trạm.
2. `search_hotels`: Lọc khách sạn theo ngân sách max, tự động sắp xếp ưu tiên theo Rating Review.
3. `calculate_budget`: Trích xuất chuỗi tổng hợp và tính bảng tài chính, tung cảnh báo nếu vượt rào hạn mức túi tiền.

---

## 🚀 Hướng Dẫn Khởi Chạy

### Yêu cầu trước
- Python 3.10 trở lên
- Đã có tài khoản và API Key của tổ chức `OpenAI`

### Bước 1: Clone và Truy cập
Mở terminal và clone kho lưu trữ (nếu bạn chưa lấy nguồn code về máy):
```bash
git clone https://github.com/USERNAME/ai-agent-lab4.git
cd ai-agent-lab4
```

### Bước 2: Thiết lập môi trường ảo
Nên sử dụng môi trường ảo (virtual environment) để tránh đụng độ thư viện:
```bash
python -m venv venv

# Kích hoạt trên Windows:
.\venv\Scripts\activate
# Kích hoạt trên Mac/Linux:
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện Phụ thuộc
```bash
pip install langchain langchain-openai langgraph python-dotenv
```

### Bước 4: Chèn biến môi trường (.env)
1. Thư mục hiện tại đã có file rỗng `.env` (Hoặc bạn hãy tạo mới 1 file tên là `.env`)
2. Nhập API Key của bạn vào dưới định dạng sau:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Bước 5: Chạy Sanity Check (Kiểm tra ổn định)
Để đảm bảo cấu hình kết nối mạng thông suốt tới OpenAI, thực thi:
```bash
python test_api.py
```
*(Nếu in ra câu chào từ ChatGPT tức là hoạt động ổn).*

### Bước 6: Khởi chạy Agent AI 🤖
Bắt đầu cuộc hội thoại chính với TravelBuddy:
```bash
python agent.py
```
*Lúc này giao diện CLI Loop sẽ mở. Bạn có thể trò chuyện với AI, ví dụ: "Tôi ở Hà Nội, mình muốn tìm vé bay vào Phú Quốc 2 đêm, budget tầm 5 củ nhé. Giúp mình nha!".*

---

## 🛡️ Tính Năng An Toàn (Guardrails)
Dự án được bọc trong các Constraints từ Sys-Prompt. Qua đó agent sẽ **lịch sự từ chối an toàn** ở các tình huống như:
- Hỏi về mã code/Toán học ngoài chủ đề.
- Dò hạch thông tin tài chính/chính trị.
- Cố gắng tra cứu các sân bay/thành thị nằm ngoài Mock Database hỗ trợ.
