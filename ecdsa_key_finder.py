#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECDSA Key Finder Script
======================

Скрипт для поиска и отображения информации о ECDSA ключах.
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
    
    def calculate_formula_value(self, row):
        """
        Вычисляет значение дополнительной формулы (пример реализации)
        
        Args:
            row (list): Строка данных
            
        Returns:
            str: Вычисленное значение формулы
        """
        # Пример вычисления формулы
        # В реальной задаче здесь должна быть конкретная формула
        # Пока возвращаем символическое значение 'x'
        return 'x'
    
    def display_result(self, row):
        """
        Отображает результат в красивом табличном формате
        
        Args:
            row (list): Строка данных для отображения
        """
        print("\n" + "="*120)
        print("🎯 РЕЗУЛЬТАТ ПОИСКА ECDSA КЛЮЧА")
        print("="*120)
        
        # Добавляем значение формулы
        formula_value = self.calculate_formula_value(row)
        extended_row = row.copy()
        extended_row.append(formula_value)
        
        # Расширенные заголовки
        extended_headers = self.headers.copy()
        extended_headers.append("Формула")
        
        # Выводим заголовки
        header_line = ""
        for header in extended_headers:
            header_line += f"{header:>12}"
        print(header_line)
        print("-" * len(header_line))
        
        # Выводим значения
        value_line = ""
        for value in extended_row:
            value_line += f"{value:>12}"
        print(value_line)
        
        print("="*120)
        
        # Дополнительная информация
        print("\n📊 ПОДРОБНАЯ ИНФОРМАЦИЯ:")
        for i, (header, value) in enumerate(zip(extended_headers, extended_row)):
            print(f"   {header}: {value}")
    
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
        finder = ECDSAKeyFinder()
        finder.run()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()