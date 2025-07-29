#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECDSA Key Finder Script (Optimized Version)
==========================================

Оптимизированный скрипт для поиска и отображения информации о ECDSA ключах.
Работает с большими CSV файлами без полной загрузки в память.

Логика работы:
1. Пользователь вводит значение k
2. Система ищет строку с указанным k, определяет r
3. Находит строку где k=введенное_k, r=найденное_r, s=r, z=r
4. Выводит все вычисленные значения включая дополнительную колонку "Формула"

Автор: Assistant
Дата создания: 2024
"""

import csv
import sys
import os
from typing import Optional, List, Dict

class ECDSAKeyFinderOptimized:
    """
    Оптимизированный класс для работы с данными ECDSA ключей
    """
    
    def __init__(self, csv_file_path="escda79.csv"):
        """
        Инициализация объекта
        
        Args:
            csv_file_path (str): Путь к CSV файлу с данными ECDSA
        """
        self.csv_file_path = csv_file_path
        self.headers = []
        
    def load_headers(self) -> bool:
        """
        Загружает только заголовки из CSV файла
        
        Returns:
            bool: True если заголовки успешно загружены
        """
        try:
            print(f"📋 Загружаю заголовки из файла {self.csv_file_path}...")
            
            if not os.path.exists(self.csv_file_path):
                print(f"❌ Ошибка: Файл {self.csv_file_path} не найден!")
                return False
            
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file, delimiter=';')
                self.headers = next(csv_reader)
                print(f"✅ Заголовки загружены: {', '.join(self.headers)}")
                return True
                
        except Exception as e:
            print(f"❌ Ошибка при загрузке заголовков: {e}")
            return False
    
    def find_r_by_k(self, k_value: int) -> Optional[int]:
        """
        Находит значение r для заданного k, читая файл построчно
        
        Args:
            k_value (int): Значение k для поиска
            
        Returns:
            int or None: Значение r если найдено, None в противном случае
        """
        print(f"🔍 Ищу значение r для k={k_value}...")
        
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file, delimiter=';')
                next(csv_reader)  # Пропускаем заголовки
                
                line_count = 0
                for row in csv_reader:
                    line_count += 1
                    
                    # Показываем прогресс каждые 500000 строк
                    if line_count % 500000 == 0:
                        print(f"📊 Проверено {line_count} строк...")
                    
                    if len(row) >= 2:
                        try:
                            k_val = int(row[0])  # k в первой колонке
                            if k_val == k_value:
                                r_val = int(row[1])  # r во второй колонке
                                print(f"✅ Найдено: k={k_value}, r={r_val} (строка {line_count + 1})")
                                return r_val
                        except ValueError:
                            continue  # Пропускаем строки с некорректными данными
                
                print(f"❌ Не найдено строки с k={k_value} (проверено {line_count} строк)")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка при поиске r: {e}")
            return None
    
    def find_target_row(self, k_value: int, r_value: int) -> Optional[List]:
        """
        Находит строку где k=k_value, r=r_value, s=r_value, z=r_value
        
        Args:
            k_value (int): Значение k
            r_value (int): Значение r
            
        Returns:
            list or None: Найденная строка или None
        """
        print(f"🔍 Ищу строку с условиями: k={k_value}, r={r_value}, s={r_value}, z={r_value}...")
        
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file, delimiter=';')
                next(csv_reader)  # Пропускаем заголовки
                
                line_count = 0
                for row in csv_reader:
                    line_count += 1
                    
                    # Показываем прогресс каждые 500000 строк
                    if line_count % 500000 == 0:
                        print(f"📊 Проверено {line_count} строк...")
                    
                    if len(row) >= 4:
                        try:
                            k_val = int(row[0])  # k
                            r_val = int(row[1])  # r
                            s_val = int(row[2])  # s
                            z_val = int(row[3])  # z
                            
                            if (k_val == k_value and 
                                r_val == r_value and 
                                s_val == r_value and 
                                z_val == r_value):
                                
                                print(f"✅ Найдена целевая строка! (строка {line_count + 1})")
                                
                                # Конвертируем всю строку в числа где возможно
                                converted_row = []
                                for value in row:
                                    try:
                                        converted_row.append(int(value))
                                    except ValueError:
                                        converted_row.append(value)
                                
                                return converted_row
                                
                        except ValueError:
                            continue  # Пропускаем строки с некорректными данными
                
                print(f"❌ Не найдена строка с заданными условиями (проверено {line_count} строк)")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка при поиске целевой строки: {e}")
            return None
    
    def calculate_formula_value(self, row: List) -> str:
        """
        Вычисляет значение дополнительной формулы
        
        Args:
            row (list): Строка данных
            
        Returns:
            str: Вычисленное значение формулы
        """
        # Пример реализации формулы
        # В зависимости от ваших требований, здесь можно реализовать конкретную формулу
        # Пока возвращаем символическое значение 'x' как в примере
        return 'x'
    
    def display_result(self, row: List):
        """
        Отображает результат в красивом табличном формате
        
        Args:
            row (list): Строка данных для отображения
        """
        print("\n" + "="*140)
        print("🎯 РЕЗУЛЬТАТ ПОИСКА ECDSA КЛЮЧА")
        print("="*140)
        
        # Добавляем значение формулы
        formula_value = self.calculate_formula_value(row)
        extended_row = row.copy()
        extended_row.append(formula_value)
        
        # Расширенные заголовки
        extended_headers = self.headers.copy()
        extended_headers.append("Формула")
        
        # Выводим заголовки
        print(f"{'k':>6}{'r':>6}{'s':>6}{'z':>6}{'d':>6}{'ks+1':>8}{'ks+z':>8}{'(ks+1)/k':>10}{'(ks+z)/k':>10}{'d-k+1':>8}{'(d-k+1)/k':>10}{'((d-k+1)/k)^77':>15}{'d-k+z':>8}{'(d-k+z)/k':>10}{'((d-k+z)/k)^77':>15}{'Формула':>8}")
        print("-" * 140)
        
        # Выводим значения
        if len(extended_row) >= 16:
            print(f"{extended_row[0]:>6}{extended_row[1]:>6}{extended_row[2]:>6}{extended_row[3]:>6}{extended_row[4]:>6}{extended_row[5]:>8}{extended_row[6]:>8}{extended_row[7]:>10}{extended_row[8]:>10}{extended_row[9]:>8}{extended_row[10]:>10}{extended_row[11]:>15}{extended_row[12]:>8}{extended_row[13]:>10}{extended_row[14]:>15}{extended_row[15]:>8}")
        
        print("="*140)
        
        # Дополнительная информация
        print("\n📊 ПОДРОБНАЯ ИНФОРМАЦИЯ:")
        for i, (header, value) in enumerate(zip(extended_headers, extended_row)):
            print(f"   {header}: {value}")
    
    def run(self):
        """
        Основная функция запуска программы
        """
        print("🚀 ECDSA Key Finder (Optimized) - Система поиска ключей ECDSA")
        print("=" * 70)
        
        # Загружаем заголовки
        if not self.load_headers():
            print("❌ Не удалось загрузить заголовки. Завершение работы.")
            return
        
        while True:
            try:
                print("\n" + "-" * 70)
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
                
                # Шаг 2: Находим строку с условиями k=k_value, r=r_value, s=r_value, z=r_value
                target_row = self.find_target_row(k_value, r_value)
                if target_row is None:
                    print(f"❌ Не найдена строка с требуемыми условиями")
                    continue
                
                # Шаг 3: Выводим результат
                self.display_result(target_row)
                
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
        finder = ECDSAKeyFinderOptimized()
        finder.run()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()