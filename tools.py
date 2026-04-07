"""
tools.py — Custom Tools cho TravelBuddy Agent
Thiết kế "Tay chân" cho Agent — 3 tools với mock data có mối liên hệ:
  search_flights → calculate_budget → search_hotels
"""

from langchain_core.tools import tool


# =============================================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# =============================================================================

FLIGHTS_DB: dict[tuple[str, str], list[dict]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "08:30", "arrival": "09:50", "price": 890_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "07:30", "arrival": "09:40", "price": 950_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "13:00", "arrival": "14:20", "price": 780_000,   "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "15:00", "arrival": "16:00", "price": 650_000,   "class": "economy"},
    ],
}

HOTELS_DB: dict[str, list[dict]] = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury",    "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê",     "rating": 4.5},
        {"name": "Sala Danang Beach",     "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê",     "rating": 4.3},
        {"name": "Fivitel Danang",        "stars": 3, "price_per_night": 650_000,   "area": "Sơn Trà",    "rating": 4.1},
        {"name": "Memory Hostel",         "stars": 2, "price_per_night": 250_000,   "area": "Hải Châu",   "rating": 4.6},
        {"name": "Christina's Homestay",  "stars": 2, "price_per_night": 350_000,   "area": "An Thượng",  "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort",  "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài",      "rating": 4.4},
        {"name": "Sol by Meliá",     "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường",   "rating": 4.2},
        {"name": "Lahana Resort",    "stars": 3, "price_per_night": 800_000,   "area": "Dương Đông",   "rating": 4.0},
        {"name": "9Station Hostel",  "stars": 2, "price_per_night": 200_000,   "area": "Dương Đông",   "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel",          "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central",    "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel",   "stars": 3, "price_per_night": 550_000,   "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room",    "stars": 2, "price_per_night": 180_000,   "area": "Quận 1", "rating": 4.6},
    ],
}


def _format_price(price: int) -> str:
    """Format giá tiền theo kiểu Việt Nam: 1.450.000đ"""
    return f"{price:,.0f}đ".replace(",", ".")


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    try:
        # Tra cứu FLIGHTS_DB với key (origin, destination)
        key: tuple[str, str] = (origin, destination)
        flights: list[dict] | None = FLIGHTS_DB.get(key)

        # Nếu không tìm thấy → thử tra ngược (destination, origin)
        if flights is None:
            reverse_key: tuple[str, str] = (destination, origin)
            flights = FLIGHTS_DB.get(reverse_key)

            if flights is None:
                return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

            # Có tuyến ngược → thông báo
            return (
                f"Không tìm thấy chuyến bay từ {origin} đến {destination}.\n"
                f"Tuy nhiên, có chuyến bay chiều ngược từ {destination} đến {origin}. "
                f"Bạn có muốn xem không?"
            )

        # Format danh sách chuyến bay dễ đọc
        result_lines: list[str] = [
            f"✈️ Tìm thấy {len(flights)} chuyến bay từ {origin} đến {destination}:\n"
        ]

        for i, flight in enumerate(flights, 1):
            result_lines.append(
                f"  {i}. {flight['airline']} | "
                f"Khởi hành: {flight['departure']} → Đến: {flight['arrival']} | "
                f"Hạng: {flight['class']} | "
                f"Giá: {_format_price(flight['price'])}"
            )

        return "\n".join(result_lines)

    except Exception as e:
        return f"Lỗi khi tìm kiếm chuyến bay: {str(e)}"


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    try:
        # Tra cứu HOTELS_DB[city]
        hotels: list[dict] | None = HOTELS_DB.get(city)

        if hotels is None:
            available_cities: str = ", ".join(HOTELS_DB.keys())
            return (
                f"Không tìm thấy khách sạn tại {city}. "
                f"Hiện tại hệ thống hỗ trợ: {available_cities}."
            )

        # Lọc theo max_price_per_night
        filtered: list[dict] = [
            h for h in hotels if h["price_per_night"] <= max_price_per_night
        ]

        if not filtered:
            return (
                f"Không tìm thấy khách sạn tại {city} "
                f"với giá dưới {_format_price(max_price_per_night)}/đêm. "
                f"Hãy thử tăng ngân sách."
            )

        # Sắp xếp theo rating giảm dần
        filtered.sort(key=lambda h: h["rating"], reverse=True)

        # Format đẹp
        result_lines: list[str] = [
            f"🏨 Tìm thấy {len(filtered)} khách sạn tại {city}"
            + (f" (giá dưới {_format_price(max_price_per_night)}/đêm)" if max_price_per_night < 99999999 else "")
            + ":\n"
        ]

        for i, hotel in enumerate(filtered, 1):
            stars_str: str = "⭐" * hotel["stars"]
            result_lines.append(
                f"  {i}. {hotel['name']} {stars_str}\n"
                f"     Giá: {_format_price(hotel['price_per_night'])}/đêm | "
                f"Khu vực: {hotel['area']} | "
                f"Rating: {hotel['rating']}/5.0"
            )

        return "\n".join(result_lines)

    except Exception as e:
        return f"Lỗi khi tìm kiếm khách sạn: {str(e)}"


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Parse chuỗi expenses thành dict {tên: số_tiền}
        expense_dict: dict[str, int] = {}

        if expenses.strip():
            items: list[str] = expenses.split(",")
            for item in items:
                item = item.strip()
                if ":" not in item:
                    return (
                        f"❌ Lỗi format: '{item}' không đúng định dạng. "
                        f"Vui lòng dùng format 'tên_khoản:số_tiền' "
                        f"(VD: 'vé_máy_bay:890000,khách_sạn:650000')"
                    )

                name, amount_str = item.rsplit(":", 1)
                name = name.strip()
                amount_str = amount_str.strip()

                try:
                    amount: int = int(amount_str)
                except ValueError:
                    return (
                        f"❌ Lỗi: '{amount_str}' không phải là số hợp lệ "
                        f"cho khoản '{name}'. Vui lòng nhập số nguyên."
                    )

                if amount < 0:
                    return f"❌ Lỗi: Số tiền cho '{name}' không thể âm ({amount})."

                expense_dict[name] = amount

        # Tính tổng chi phí
        total_expenses: int = sum(expense_dict.values())

        # Tính số tiền còn lại
        remaining: int = total_budget - total_expenses

        # Format bảng chi tiết
        result_lines: list[str] = ["💰 Bảng chi phí:\n"]

        for name, amount in expense_dict.items():
            # Thay dấu _ bằng khoảng trắng cho đẹp
            display_name: str = name.replace("_", " ").title()
            result_lines.append(f"  - {display_name}: {_format_price(amount)}")

        result_lines.append("  " + "-" * 30)
        result_lines.append(f"  Tổng chi: {_format_price(total_expenses)}")
        result_lines.append(f"  Ngân sách: {_format_price(total_budget)}")

        # Nếu âm → cảnh báo vượt ngân sách
        if remaining < 0:
            result_lines.append(
                f"  ⚠️ VƯỢT NGÂN SÁCH: {_format_price(abs(remaining))}! "
                f"Cần điều chỉnh."
            )
        else:
            result_lines.append(f"  ✅ Còn lại: {_format_price(remaining)}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Lỗi khi tính toán ngân sách: {str(e)}"
