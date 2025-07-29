#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для демонстрации функциональности ECDSA Key Finder
=================================================================

Этот скрипт демонстрирует логику поиска 4 типов ключей.
"""

def demonstrate_key_search_logic():
    """
    Демонстрирует логику поиска ключей
    """
    print("🎯 ДЕМОНСТРАЦИЯ ЛОГИКИ ПОИСКА ECDSA КЛЮЧЕЙ")
    print("=" * 60)
    
    k_value = 14  # Пример значения k
    
    print(f"📝 Входные данные: k = {k_value}")
    print("\n🔍 ЭТАПЫ ПОИСКА:")
    
    # Этап 1: Поиск r
    print(f"\n1️⃣ Ищем любую строку с k={k_value}")
    print(f"   └── Находим r = 5 (пример)")
    
    # Этап 2: Ключ 1 - основной
    print(f"\n2️⃣ Ключ 1 (основной) - Формула 'x':")
    print(f"   Условия: k={k_value}, r=5, s=5, z=5")
    print(f"   └── Результат: [14, 5, 5, 5, 13, 71, 75, 22, 11, 0, 0, 0, 4, 68, 43]")
    
    # Этап 3: Ключ 2 - первый ключ
    print(f"\n3️⃣ Ключ 2 (первый ключ) - Формула 'Первый ключ':")
    print(f"   Условия: k={k_value}, s=0, d=1")
    print(f"   └── Запоминаем z этой строки")
    
    # Этап 4: Ключ 3
    print(f"\n4️⃣ Ключ 3 - Формула '-y':")
    print(f"   Условия:")
    print(f"   • d = key1.d - 16 = 13 - 16 = -3")
    print(f"   • s = key1.s = 5")
    print(f"   • z = key1.z - key2.z")
    
    # Этап 5: Ключ 4 - зеркальный
    print(f"\n5️⃣ Ключ 4 (зеркальный) - Формула 'y':")
    print(f"   Условия:")
    print(f"   • s = -key3.s (mod 79)")
    print(f"   • z = -key3.z (mod 79)")
    
    print(f"\n📊 ИТОГОВАЯ ТАБЛИЦА:")
    print("=" * 120)
    print(f"{'k':>8}{'r':>8}{'s':>8}{'z':>8}{'d':>8}{'...':>8}{'Формула':>12}")
    print("-" * 120)
    print(f"{'14':>8}{'5':>8}{'5':>8}{'5':>8}{'13':>8}{'...':>8}{'x':>12}")
    print(f"{'14':>8}{'?':>8}{'0':>8}{'?':>8}{'1':>8}{'...':>8}{'Первый ключ':>12}")
    print(f"{'?':>8}{'?':>8}{'5':>8}{'?':>8}{'-3':>8}{'...':>8}{'-y':>12}")
    print(f"{'?':>8}{'?':>8}{'?':>8}{'?':>8}{'?':>8}{'...':>8}{'y':>12}")
    print("=" * 120)

def show_modular_arithmetic_example():
    """
    Демонстрирует модульную арифметику для зеркального ключа
    """
    print("\n\n🧮 ПРИМЕР МОДУЛЬНОЙ АРИФМЕТИКИ (mod 79):")
    print("=" * 50)
    
    example_s = 25
    example_z = 40
    
    mirror_s = (-example_s) % 79
    mirror_z = (-example_z) % 79
    
    print(f"Исходные значения Ключа 3:")
    print(f"   s = {example_s}")
    print(f"   z = {example_z}")
    
    print(f"\nЗеркальные значения Ключа 4:")
    print(f"   s = -{example_s} mod 79 = {mirror_s}")
    print(f"   z = -{example_z} mod 79 = {mirror_z}")
    
    print(f"\nПроверка:")
    print(f"   ({example_s} + {mirror_s}) mod 79 = {(example_s + mirror_s) % 79}")
    print(f"   ({example_z} + {mirror_z}) mod 79 = {(example_z + mirror_z) % 79}")

def main():
    """
    Основная функция демонстрации
    """
    demonstrate_key_search_logic()
    show_modular_arithmetic_example()
    
    print(f"\n\n🚀 ЗАПУСК РЕАЛЬНОГО СКРИПТА:")
    print("   python3 ecdsa_key_finder.py")
    print("\n💡 Введите k=14 для тестирования описанной логики")

if __name__ == "__main__":
    main()