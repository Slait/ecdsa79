#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECDSA Key Finder Script
======================

Скрипт для поиска и отображения информации о ECDSA ключах.
Логика работы:
1. Пользователь вводит значение k
2. Система ищет строку с указанным k, определяет r
3. Находит 4 типа ключей:
   - Ключ 1 (основной): k=k_value, r=r_value, s=r_value, z=r_value → Формула "x"
   - Ключ 2 (первый): k=k_value, s=0, d=1 → Формула "Первый ключ"
   - Ключ 3: d на 16 меньше key1.d, s=key1.s, z=key1.z-key2.z → Формула "-y"
   - Ключ 4 (зеркальный): s=-key3.s (mod 79), z=-key3.z (mod 79) → Формула "y"
4. Выводит все найденные ключи в табличном формате

Автор: Assistant
Дата создания: 2024
"""

import csv
import sys
import os

class ECDSAKeyFinder:
    """
    Класс для работы с данными ECDSA ключей
    """
    
    def __init__(self, csv_file_path="escda79.csv"):
        """
        Инициализация объекта
        
        Args:
            csv_file_path (str): Путь к CSV файлу с данными ECDSA
        """
        self.csv_file_path = csv_file_path
        self.data = []
        self.headers = []
        
    def load_data(self):
        """
        Загружает данные из CSV файла
        
        Returns:
            bool: True если данные успешно загружены, False в противном случае
        """
        try:
            print(f"🔄 Загружаю данные из файла {self.csv_file_path}...")
            
            if not os.path.exists(self.csv_file_path):
                print(f"❌ Ошибка: Файл {self.csv_file_path} не найден!")
                return False
            
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                # CSV файл использует точку с запятой как разделитель
                csv_reader = csv.reader(file, delimiter=';')
                
                # Читаем заголовки
                self.headers = next(csv_reader)
                print(f"📋 Найдены колонки: {', '.join(self.headers)}")
                
                # Читаем данные
                for row_num, row in enumerate(csv_reader, start=2):
                    if len(row) >= len(self.headers):
                        # Преобразуем строковые значения в числа где возможно
                        converted_row = []
                        for i, value in enumerate(row):
                            try:
                                # Пытаемся конвертировать в int
                                converted_row.append(int(value))
                            except ValueError:
                                # Если не получается, оставляем как строку
                                converted_row.append(value)
                        self.data.append(converted_row)
                    
                    # Показываем прогресс каждые 100000 строк
                    if row_num % 100000 == 0:
                        print(f"📊 Обработано {row_num-1} строк...")
            
            print(f"✅ Данные успешно загружены! Всего строк: {len(self.data)}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при загрузке данных: {e}")
            return False
    
    def find_r_by_k(self, k_value):
        """
        Находит значение r для заданного k
        
        Args:
            k_value (int): Значение k для поиска
            
        Returns:
            int or None: Значение r если найдено, None в противном случае
        """
        print(f"🔍 Ищу значение r для k={k_value}...")
        
        # Индекс колонки k (первая колонка, индекс 0)
        k_col_index = 0
        # Индекс колонки r (вторая колонка, индекс 1)
        r_col_index = 1
        
        for row in self.data:
            if row[k_col_index] == k_value:
                r_value = row[r_col_index]
                print(f"✅ Найдено: k={k_value}, r={r_value}")
                return r_value
        
        print(f"❌ Не найдено строки с k={k_value}")
        return None
    
    def find_target_row(self, k_value, r_value):
        """
        Находит строку где k=k_value, r=r_value, s=r_value, z=r_value
        
        Args:
            k_value (int): Значение k
            r_value (int): Значение r
            
        Returns:
            list or None: Найденная строка или None
        """
        print(f"🔍 Ищу строку с условиями: k={k_value}, r={r_value}, s={r_value}, z={r_value}...")
        
        # Индексы колонок
        k_col_index = 0  # k
        r_col_index = 1  # r
        s_col_index = 2  # s
        z_col_index = 3  # z
        
        for row in self.data:
            if (row[k_col_index] == k_value and 
                row[r_col_index] == r_value and 
                row[s_col_index] == r_value and 
                row[z_col_index] == r_value):
                print(f"✅ Найдена целевая строка!")
                return row
        
        print(f"❌ Не найдена строка с заданными условиями")
        return None
    
    def find_key2(self, k_value):
        """
        Находит Ключ 2: k=k_value, s=0, d=1
        
        Args:
            k_value (int): Значение k для поиска
            
        Returns:
            list or None: Найденная строка или None
        """
        print(f"🔍 Ищу Ключ 2: k={k_value}, s=0, d=1...")
        
        # Индексы колонок
        k_col_index = 0  # k
        s_col_index = 2  # s
        d_col_index = 4  # d
        
        for row in self.data:
            if (row[k_col_index] == k_value and 
                row[s_col_index] == 0 and 
                row[d_col_index] == 1):
                print(f"✅ Найден Ключ 2! z={row[3]}")
                return row
        
        print(f"❌ Не найден Ключ 2 с условиями: k={k_value}, s=0, d=1")
        return None
    
    def find_key3(self, key1_data, key2_data):
        """
        Находит Ключ 3: d на 16 меньше key1.d, s=key1.s, z=key1.z-key2.z
        
        Args:
            key1_data (list): Данные первого ключа
            key2_data (list): Данные второго ключа
            
        Returns:
            list or None: Найденная строка или None
        """
        key3_d = key1_data[4] - 16  # d на 16 меньше key1.d
        key3_s = key1_data[2]       # s = key1.s
        key3_z = key1_data[3] - key2_data[3]  # z = key1.z - key2.z
        
        print(f"🔍 Ищу Ключ 3: d={key3_d}, s={key3_s}, z={key3_z}...")
        
        # Индексы колонок
        d_col_index = 4  # d
        s_col_index = 2  # s
        z_col_index = 3  # z
        
        for row in self.data:
            if (row[d_col_index] == key3_d and 
                row[s_col_index] == key3_s and 
                row[z_col_index] == key3_z):
                print(f"✅ Найден Ключ 3!")
                return row
        
        print(f"❌ Не найден Ключ 3 с условиями: d={key3_d}, s={key3_s}, z={key3_z}")
        return None
    
    def find_key4(self, key3_data):
        """
        Находит Ключ 4 (зеркальный): s=-key3.s (mod 79), z=-key3.z (mod 79)
        
        Args:
            key3_data (list): Данные третьего ключа
            
        Returns:
            list or None: Найденная строка или None
        """
        key4_s = (-key3_data[2]) % 79  # s = -key3.s (mod 79)
        key4_z = (-key3_data[3]) % 79  # z = -key3.z (mod 79)
        
        print(f"🔍 Ищу Ключ 4 (зеркальный): s={key4_s}, z={key4_z}...")
        
        # Индексы колонок
        s_col_index = 2  # s
        z_col_index = 3  # z
        
        for row in self.data:
            if (row[s_col_index] == key4_s and 
                row[z_col_index] == key4_z):
                print(f"✅ Найден Ключ 4 (зеркальный)!")
                return row
        
        print(f"❌ Не найден Ключ 4 с условиями: s={key4_s}, z={key4_z}")
        return None
    
    def display_results_table(self, keys_data):
        """
        Отображает таблицу с несколькими найденными ключами
        
        Args:
            keys_data (list): Список кортежей (данные_ключа, название_формулы)
        """
        print("\n" + "="*150)
        print("🎯 РЕЗУЛЬТАТ ПОИСКА ECDSA КЛЮЧЕЙ")
        print("="*150)
        
        # Выводим заголовки
        print(f"{'k':>8}{'r':>8}{'s':>8}{'z':>8}{'d':>8}{'ks+1':>8}{'ks+z':>8}{'(ks+1)/k':>10}{'(ks+z)/k':>10}{'d-k+1':>8}{'(d-k+1)/k':>12}{'((d-k+1)/k)^77':>15}{'d-k+z':>8}{'(d-k+z)/k':>12}{'((d-k+z)/k)^77':>15}{'Формула':>12}")
        print("-" * 150)
        
        # Выводим каждый ключ
        for row_data, formula_name in keys_data:
            if row_data and len(row_data) >= 15:
                print(f"{row_data[0]:>8}{row_data[1]:>8}{row_data[2]:>8}{row_data[3]:>8}{row_data[4]:>8}{row_data[5]:>8}{row_data[6]:>8}{row_data[7]:>10}{row_data[8]:>10}{row_data[9]:>8}{row_data[10]:>12}{row_data[11]:>15}{row_data[12]:>8}{row_data[13]:>12}{row_data[14]:>15}{formula_name:>12}")
        
        print("="*150)
        
        # Дополнительная информация
        print("\n📊 ПОДРОБНАЯ ИНФОРМАЦИЯ:")
        for i, (row_data, formula_name) in enumerate(keys_data, 1):
            if row_data:
                print(f"\n   🔑 Ключ {i} ({formula_name}):")
                for j, (header, value) in enumerate(zip(self.headers, row_data)):
                    print(f"      {header}: {value}")
    
    def run(self):
        """
        Основная функция запуска программы
        """
        print("🚀 ECDSA Key Finder - Система поиска ключей ECDSA")
        print("=" * 60)
        
        # Загружаем данные
        if not self.load_data():
            print("❌ Не удалось загрузить данные. Завершение работы.")
            return
        
        while True:
            try:
                print("\n" + "-" * 60)
                print("📝 Введите значение k для поиска (или 'quit' для выхода):")
                
                user_input = input("👉 k = ").strip()
                
                # Проверка на выход
                if user_input.lower() in ['quit', 'exit', 'q', 'выход']:
                    print("👋 До свидания!")
                    break
                
                # Конвертируем в число
                k_value = int(user_input)
                
                print(f"\n🔄 Начинаю поиск для k = {k_value}")
                
                # Шаг 1: Находим r для заданного k
                r_value = self.find_r_by_k(k_value)
                if r_value is None:
                    print(f"❌ Не найдено значение r для k={k_value}")
                    continue
                
                # Шаг 2: Находим Ключ 1 - основной ключ с условиями k=k_value, r=r_value, s=r_value, z=r_value
                print(f"\n🔍 Поиск Ключа 1 (основной ключ)...")
                key1_data = self.find_target_row(k_value, r_value)
                if key1_data is None:
                    print(f"❌ Не найден Ключ 1 с требуемыми условиями")
                    continue
                
                # Шаг 3: Находим Ключ 2 - k остается статичным, s=0, d=1
                print(f"\n🔍 Поиск Ключа 2 (Первый ключ)...")
                key2_data = self.find_key2(k_value)
                if key2_data is None:
                    print(f"❌ Не найден Ключ 2")
                    # Продолжаем работу только с Ключом 1
                    keys_found = [(key1_data, "x")]
                else:
                    # Шаг 4: Находим Ключ 3 - d на 16 меньше key1.d, s=key1.s, z=key1.z-key2.z
                    print(f"\n🔍 Поиск Ключа 3 (-y)...")
                    key3_data = self.find_key3(key1_data, key2_data)
                    
                    if key3_data is None:
                        print(f"❌ Не найден Ключ 3")
                        keys_found = [(key1_data, "x"), (key2_data, "Первый ключ")]
                    else:
                        # Шаг 5: Находим Ключ 4 - зеркальный ключ
                        print(f"\n🔍 Поиск Ключа 4 (зеркальный - y)...")
                        key4_data = self.find_key4(key3_data)
                        
                        if key4_data is None:
                            print(f"❌ Не найден Ключ 4")
                            keys_found = [(key1_data, "x"), (key2_data, "Первый ключ"), (key3_data, "-y")]
                        else:
                            keys_found = [(key1_data, "x"), (key2_data, "Первый ключ"), (key3_data, "-y"), (key4_data, "y")]
                
                # Шаг 6: Выводим результаты всех найденных ключей
                print(f"\n✅ Найдено ключей: {len(keys_found)}")
                self.display_results_table(keys_found)
                
            except ValueError:
                print("❌ Ошибка: Введите корректное числовое значение для k")
            except KeyboardInterrupt:
                print("\n\n👋 Прерывание пользователем. До свидания!")
                break
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")

def main():
    """
    Точка входа в программу
    """
    try:
        finder = ECDSAKeyFinder()
        finder.run()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()