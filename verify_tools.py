# -*- coding: utf-8 -*-
"""verify_tools.py — Kiểm tra 3 tools hoạt động đúng"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from tools import search_flights, search_hotels, calculate_budget

print("=" * 60)
print("TEST 1: search_flights('Hà Nội', 'Đà Nẵng')")
print("=" * 60)
result = search_flights.invoke({"origin": "Hà Nội", "destination": "Đà Nẵng"})
print(result)
print()

print("=" * 60)
print("TEST 2: search_flights reverse ('Đà Nẵng', 'Hà Nội')")
print("=" * 60)
result = search_flights.invoke({"origin": "Đà Nẵng", "destination": "Hà Nội"})
print(result)
print()

print("=" * 60)
print("TEST 3: search_flights not found")
print("=" * 60)
result = search_flights.invoke({"origin": "Đà Nẵng", "destination": "Phú Quốc"})
print(result)
print()

print("=" * 60)
print("TEST 4: search_hotels('Phú Quốc', max_price=1000000)")
print("=" * 60)
result = search_hotels.invoke({"city": "Phú Quốc", "max_price_per_night": 1000000})
print(result)
print()

print("=" * 60)
print("TEST 5: search_hotels('Đà Nẵng') - tất cả")
print("=" * 60)
result = search_hotels.invoke({"city": "Đà Nẵng"})
print(result)
print()

print("=" * 60)
print("TEST 6: calculate_budget(5000000, 'vé_máy_bay:1100000,khách_sạn:1600000')")
print("=" * 60)
result = calculate_budget.invoke({"total_budget": 5000000, "expenses": "vé_máy_bay:1100000,khách_sạn:1600000"})
print(result)
print()

print("=" * 60)
print("TEST 7: calculate_budget vượt ngân sách")
print("=" * 60)
result = calculate_budget.invoke({"total_budget": 2000000, "expenses": "vé_máy_bay:1500000,khách_sạn:1600000"})
print(result)
print()

print("=" * 60)
print("TEST 8: calculate_budget format sai")
print("=" * 60)
result = calculate_budget.invoke({"total_budget": 5000000, "expenses": "vé_máy_bay-1100000"})
print(result)
print()

print("ALL TESTS COMPLETED!")
