#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пример запуска ECDSA Key Finder
===============================

Демонстрационный скрипт показывающий как использовать созданные инструменты.
"""

import os
import sys

def main():
    print("🎯 ECDSA Key Finder - Пример использования")
    print("=" * 50)
    
    # Проверяем наличие CSV файла
    csv_file = "escda79.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Файл {csv_file} не найден!")
        print("📋 Убедитесь что CSV файл находится в том же каталоге.")
        return
    
    print(f"✅ Найден файл данных: {csv_file}")
    
    # Проверяем доступные скрипты
    scripts = [
        ("ecdsa_fast_finder.py", "⭐ Рекомендуется - самый быстрый"),
        ("ecdsa_key_finder_optimized.py", "🔧 Оптимизированный"),
        ("ecdsa_key_finder.py", "📚 Базовый")
    ]
    
    print("\n📁 Доступные скрипты:")
    for script, description in scripts:
        if os.path.exists(script):
            print(f"   ✅ {script} - {description}")
        else:
            print(f"   ❌ {script} - не найден")
    
    print("\n🚀 Способы запуска:")
    print("   1. python3 ecdsa_fast_finder.py")
    print("   2. ./ecdsa_fast_finder.py  (если исполняемый)")
    print("   3. echo '14' | python3 ecdsa_fast_finder.py  (автоматический поиск)")
    
    print("\n💡 Пример интерактивного использования:")
    print("   - Запустите скрипт")
    print("   - Введите k = 14")
    print("   - Получите результат в формате:")
    print("     k  r  s  z  d  ks+1  ks+z  (ks+1)/k  (ks+z)/k  d-k+1  (d-k+1)/k  ((d-k+1)/k)^77  d-k+z  (d-k+z)/k  ((d-k+z)/k)^77  Формула")
    print("     14 5  5  5  13 71    75    22        11        0      0          0              4      68        43              x")
    
    print("\n📖 Для подробной документации см. README.md")

if __name__ == "__main__":
    main()