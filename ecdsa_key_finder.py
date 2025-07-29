#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECDSA Key Finder Script (Fixed Version)
=======================================

Скрипт для поиска ECDSA ключей с правильной логикой.
k всегда статичный, поиск только среди строк с одинаковым k.
Все расчеты по модулю 79.

Логика:
1. Ключ 1: k=k_value, r=r_value, s=r_value, z=r_value → "x"
2. Ключ 2: k=k_value, s=0, d=1 → "Первый ключ"  
3. Ключ 3: k=k_value, d=key1.d-16, s=key1.s, z=(key1.z-key2.z)%79 → "-y"
4. Ключ 4: k=k_value, s=(-key3.s)%79, z=(-key3.z)%79 → "y"
"""

import csv
import sys
import os

class ECDSAKeyFinder:
    def __init__(self, csv_file_path="escda79.csv"):
        self.csv_file_path = csv_file_path
        self.data = []
        self.headers = []
        
    def load_data_fast(self):
        """Быстрая загрузка без проверок"""
        with open(self.csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=';')
            self.headers = next(csv_reader)
            
            for row in csv_reader:
                converted_row = []
                for value in row:
                    try:
                        converted_row.append(int(value))
                    except:
                        converted_row.append(value)
                self.data.append(converted_row)
        
        print(f"✅ Загружено {len(self.data)} строк")
    
    def find_keys_for_k(self, k_value):
        """Находит все ключи для заданного k"""
        print(f"🔍 Поиск всех ключей для k={k_value}")
        
        # Фильтруем только строки с нужным k
        k_rows = [row for row in self.data if row[0] == k_value]
        print(f"📊 Найдено {len(k_rows)} строк с k={k_value}")
        
        if not k_rows:
            print(f"❌ Нет данных для k={k_value}")
            return []
        
        # Ключ 1: находим первую строку для определения r
        first_row = k_rows[0]
        r_value = first_row[1]
        print(f"🔑 Определено r={r_value}")
        
        # Ключ 1: k=k_value, r=r_value, s=r_value, z=r_value
        key1 = None
        for row in k_rows:
            if row[1] == r_value and row[2] == r_value and row[3] == r_value:
                key1 = row
                print(f"✅ Ключ 1 найден")
                break
        
        if not key1:
            print(f"❌ Ключ 1 не найден")
            return []
        
        # Ключ 2: k=k_value, s=0, d=1
        key2 = None
        for row in k_rows:
            if row[2] == 0 and row[4] == 1:  # s=0, d=1
                key2 = row
                print(f"✅ Ключ 2 найден, z={row[3]}")
                break
        
        if not key2:
            print(f"❌ Ключ 2 не найден")
            return [(key1, "x")]
        
        # Ключ 3: k=k_value, d=key1.d-16, s=key1.s, z=(key1.z-key2.z)%79
        key3_d = (key1[4] - 16) % 79
        key3_s = key1[2]
        key3_z = (key1[3] - key2[3]) % 79
        
        key3 = None
        for row in k_rows:
            if row[4] == key3_d and row[2] == key3_s and row[3] == key3_z:
                key3 = row
                print(f"✅ Ключ 3 найден: d={key3_d}, s={key3_s}, z={key3_z}")
                break
        
        if not key3:
            print(f"❌ Ключ 3 не найден (d={key3_d}, s={key3_s}, z={key3_z})")
            return [(key1, "x"), (key2, "Первый ключ")]
        
        # Ключ 4: k=k_value, s=(-key3.s)%79, z=(-key3.z)%79
        key4_s = (-key3[2]) % 79
        key4_z = (-key3[3]) % 79
        
        key4 = None
        for row in k_rows:
            if row[2] == key4_s and row[3] == key4_z:
                key4 = row
                print(f"✅ Ключ 4 найден: s={key4_s}, z={key4_z}")
                break
        
        if not key4:
            print(f"❌ Ключ 4 не найден (s={key4_s}, z={key4_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "-y")]
        
        return [(key1, "x"), (key2, "Первый ключ"), (key3, "-y"), (key4, "y")]
    
    def display_table(self, keys_data):
        """Выводит таблицу ключей"""
        if not keys_data:
            print("❌ Нет данных для отображения")
            return
            
        print("\n" + "="*150)
        print("🎯 РЕЗУЛЬТАТ ПОИСКА ECDSA КЛЮЧЕЙ")
        print("="*150)
        
        # Заголовки
        print(f"{'k':>6}{'r':>6}{'s':>6}{'z':>6}{'d':>6}{'ks+1':>8}{'ks+z':>8}{'(ks+1)/k':>10}{'(ks+z)/k':>10}{'d-k+1':>8}{'(d-k+1)/k':>10}{'((d-k+1)/k)^77':>15}{'d-k+z':>8}{'(d-k+z)/k':>10}{'((d-k+z)/k)^77':>15}{'Формула':>12}")
        print("-" * 150)
        
        # Данные
        for row_data, formula in keys_data:
            if len(row_data) >= 15:
                print(f"{row_data[0]:>6}{row_data[1]:>6}{row_data[2]:>6}{row_data[3]:>6}{row_data[4]:>6}{row_data[5]:>8}{row_data[6]:>8}{row_data[7]:>10}{row_data[8]:>10}{row_data[9]:>8}{row_data[10]:>10}{row_data[11]:>15}{row_data[12]:>8}{row_data[13]:>10}{row_data[14]:>15}{formula:>12}")
        
        print("="*150)
        
        # Детали
        print("\n📊 ДЕТАЛИ:")
        for i, (row_data, formula) in enumerate(keys_data, 1):
            print(f"🔑 Ключ {i} ({formula}): k={row_data[0]}, r={row_data[1]}, s={row_data[2]}, z={row_data[3]}, d={row_data[4]}")
    
    def run(self):
        print("🚀 ECDSA Key Finder - Быстрая версия")
        print("="*50)
        
        # Быстрая загрузка
        try:
            self.load_data_fast()
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return
        
        while True:
            try:
                print("\n" + "-"*50)
                user_input = input("👉 Введите k (или 'quit'): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Выход")
                    break
                
                k_value = int(user_input)
                
                # Поиск всех ключей
                keys_data = self.find_keys_for_k(k_value)
                
                # Вывод результата
                if keys_data:
                    self.display_table(keys_data)
                    print(f"\n✅ Найдено ключей: {len(keys_data)}")
                else:
                    print("❌ Ключи не найдены")
                
            except ValueError:
                print("❌ Введите число")
            except KeyboardInterrupt:
                print("\n👋 Выход")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")

def main():
    finder = ECDSAKeyFinder()
    finder.run()

if __name__ == "__main__":
    main()