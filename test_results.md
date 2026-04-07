# Test Results — Lab 4: TravelBuddy AI Agent

## Test 1 — Direct Answer (Không cần tool)

```
Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

 TravelBuddy đang suy nghĩ...
💬 Trả lời trực tiếp

TravelBuddy: Chào bạn! Có nhiều điểm đến tuyệt vời tại Việt Nam mà bạn có thể cân nhắc. Dưới đây là một số gợi ý:

1. **Đà Nẵng**: Nơi có bãi biển đẹp, cầu Vàng nổi tiếng và nhiều danh lam thắng cảnh như Bà Nà Hills, Ngũ Hành Sơn.

2. **Phú Quốc**: Hòn đảo lý tưởng cho việc nghỉ dưỡng, với những bãi biển tuyệt đẹp và không khí trong lành. Bạn có thể tham gia vào nhiều hoạt động giải trí dưới nước như lặn biển và tham quan đảo.

3. **Hồ Chí Minh**: Thành phố nhộn nhịp với nhiều điểm tham quan văn hóa, ẩm thực phong phú và cuộc sống về đêm sôi động.

4. **Hà Nội**: Thủ đô với nhiều di tích lịch sử, văn hóa. Bạn có thể thưởng thức món phở nổi tiếng và tham quan Hoàn Kiếm, Văn Miếu Quốc Tử Giám.

Bạn thích điểm đến nào hoặc có ý tưởng gì về ngân sách và thời gian đi du lịch không? Hãy cho mình biết để mình giúp bạn lên kế hoạch tốt nhất nhé!
```

**Kết quả:** ✅ PASS — Agent chào hỏi thân thiện, hỏi thêm sở thích/ngân sách/thời gian, KHÔNG gọi tool nào.

---

## Test 2 — Single Tool Call

```
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

🤔 TravelBuddy đang suy nghĩ...
🔧 Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})

TravelBuddy: ✈️ Tìm thấy 4 chuyến bay từ Hà Nội đến Đà Nẵng:

1. **Vietnam Airlines**
   - Khởi hành: 06:00 → Đến: 07:20
   - Hạng: Economy
   - Giá: 1.450.000đ

2. **VietJet Air**
   - Khởi hành: 08:30 → Đến: 09:50
   - Hạng: Economy
   - Giá: 890.000đ (Rẻ nhất!)

3. **Bamboo Airways**
   - Khởi hành: 11:00 → Đến: 12:20
   - Hạng: Economy
   - Giá: 1.200.000đ

4. **Vietnam Airlines**
   - Khởi hành: 14:00 → Đến: 15:20
   - Hạng: Business
   - Giá: 2.800.000đ

Nếu bạn muốn tiết kiệm, mình gợi ý chuyến VietJet Air lúc 08:30 với giá chỉ 890.000đ. Bạn muốn mình tìm thêm khách sạn ở Đà Nẵng không?
```

**Kết quả:** ✅ PASS — Gọi đúng search_flights("Hà Nội", "Đà Nẵng"), liệt kê đủ 4 chuyến.

---

## Test 3 — Multi-Step Tool Chaining

```
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

🤔 TravelBuddy đang suy nghĩ...
🔧 Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
🔧 Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000'})
🔧 Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1950000})
💬 Trả lời trực tiếp

TravelBuddy: Dưới đây là kế hoạch chuyến đi của bạn từ Hà Nội đến Phú Quốc 2 đêm với ngân sách 5 triệu đồng:

### Chuyến bay:
1. **VietJet Air**
   - Khởi hành: 16:00 → Đến: 18:15
   - Hạng: Economy
   - Giá: 1.100.000đ

### Khách sạn:
Sau khi trừ vé máy bay, bạn còn lại 3.900.000đ. Dưới đây là một số lựa chọn khách sạn phù hợp:

1. **Sol by Meliá**
   - Giá: 1.500.000đ/đêm
   - Khu vực: Bãi Trường
   - Rating: 4.2/5.0

   Tổng chi cho 2 đêm: 3.000.000đ

2. **Lahana Resort**
   - Giá: 800.000đ/đêm
   - Khu vực: Dương Đông
   - Rating: 4.0/5.0

   Tổng chi cho 2 đêm: 1.600.000đ

3. **9Station Hostel**
   - Giá: 200.000đ/đêm
   - Khu vực: Dương Đông
   - Rating: 4.5/5.0

   Tổng chi cho 2 đêm: 400.000đ

### Tổng chi phí ước tính:
- **Vé máy bay:** 1.100.000đ
- **Khách sạn (Sol by Meliá - 2 đêm):** 3.000.000đ
- **Tổng chi:** 4.100.000đ

### Còn lại: 900.000đ

### Gợi ý thêm:
- Với ngân sách còn lại, bạn có thể dùng để ăn uống, tham quan, hoặc vận chuyển trong Phú Quốc.
- Hãy nhớ khám phá các bãi biển đẹp ở Phú Quốc nhé!

Nếu bạn đồng ý với kế hoạch này hoặc cần thay đổi gì, hãy cho tôi biết nhé!
```

**Kết quả:** ✅ PASS — Agent tự chuỗi 3 tools: flights → hotels → budget. Chọn vé rẻ nhất, khách sạn vừa tầm giá, tổng hợp chi phí hoàn chỉnh.

---

## Test 4 — Missing Info / Clarification

```
Bạn: Tôi muốn đặt khách sạn

🤔 TravelBuddy đang suy nghĩ...
💬 Trả lời trực tiếp

TravelBuddy: Để giúp bạn đặt khách sạn, mình cần thêm một số thông tin:

1. **Điểm đến**: Bạn muốn ở thành phố nào (Đà Nẵng, Phú Quốc, Hồ Chí Minh hay Hà Nội)? 
2. **Ngày check-in và check-out**: Bạn dự định ở bao lâu?
3. **Ngân sách mỗi đêm**: Bạn muốn chi bao nhiêu cho mỗi đêm lưu trú?
4. **Số lượng người ở**: Có bao nhiêu người trong nhóm của bạn?

Hãy cung cấp thông tin trên để mình có thể tìm khách sạn phù hợp cho bạn nhé!
```

**Kết quả:** ✅ PASS — Agent hỏi lại 3 thông tin cần thiết (thành phố, số đêm, ngân sách), KHÔNG gọi tool vội.

---

## Test 5 — Guardrail / Refusal

```
Bạn: Giải giúp tôi bài tập lập trình Python về linked list

🤔 TravelBuddy đang suy nghĩ...
💬 Trả lời trực tiếp

TravelBuddy: Xin lỗi, nhưng mình không thể giúp bạn về lập trình hay bài tập học thuật. Tuy nhiên, nếu bạn đang tìm kiếm một nơi để du lịch hoặc đặt khách sạn, mình rất vui lòng hỗ trợ bạn! Bạn có muốn tìm hiểu thêm về một điểm đến nào đó không?
```

**Kết quả:** ✅ PASS — Agent từ chối lịch sự, nói rõ chỉ hỗ trợ du lịch, KHÔNG cố gắng giải bài tập.
