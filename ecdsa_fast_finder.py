#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECDSA Fast Key Finder Script
============================

Сверхбыстрый скрипт для поиска ECDSA ключей с использованием grep.
Оптимизирован для работы с очень большими CSV файлами.

Логика работы:
1. Пользователь вводит значение k
2. Система быстро ищет строку с указанным k с помощью grep, определяет r
3. Находит строку где k=введенное_k, r=найденное_r, s=r, z=r
4. Выводит все вычисленные значения включая дополнительную колонку "Формула"

Автор: Assistant
Дата создания: 2024
"""

import subprocess
import sys
import os
import re

class ECDSAFastFinder:
    """
    Сверхбыстрый класс для работы с данными ECDSA ключей
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
        Загружает заголовки из CSV файла
        
        Returns:
            bool: True если заголовки успешно загружены
        """
        try:
            print(f"📋 Загружаю заголовки из файла {self.csv_file_path}...")
            
            if not os.path.exists(self.csv_file_path):
                print(f"❌ Ошибка: Файл {self.csv_file_path} не найден!")
                return False
            
            # Читаем первую строку с заголовками
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()
                self.headers = first_line.split(';')
                print(f"✅ Заголовки загружены: {', '.join(self.headers)}")
                return True
                
        except Exception as e:
            print(f"❌ Ошибка при загрузке заголовков: {e}")
            return False
    
    def find_r_by_k_fast(self, k_value: int) -> int:
        """
        Быстро находит значение r для заданного k с помощью grep
        
        Args:
            k_value (int): Значение k для поиска
            
        Returns:
            int or None: Значение r если найдено, None в противном случае
        """
        print(f"🔍 Ищу значение r для k={k_value} (используя grep)...")
        
        try:
            # Используем grep для быстрого поиска строки, начинающейся с "k_value;"
            grep_pattern = f"^{k_value};"
            cmd = ['grep', '-m', '1', grep_pattern, self.csv_file_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                # Нашли строку, извлекаем r (вторая колонка)
                line = result.stdout.strip()
                fields = line.split(';')
                
                if len(fields) >= 2:
                    r_value = int(fields[1])
                    print(f"✅ Найдено: k={k_value}, r={r_value}")
                    return r_value
                else:
                    print(f"❌ Некорректный формат строки: {line}")
                    return None
            else:
                print(f"❌ Не найдено строки с k={k_value}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"❌ Превышено время ожидания при поиске k={k_value}")
            return None
        except Exception as e:
            print(f"❌ Ошибка при поиске r: {e}")
            return None
    
    def find_target_row_fast(self, k_value: int, r_value: int) -> list:
        """
        Быстро находит строку где k=k_value, r=r_value, s=r_value, z=r_value
        
        Args:
            k_value (int): Значение k
            r_value (int): Значение r
            
        Returns:
            list or None: Найденная строка или None
        """
        print(f"🔍 Ищу строку с условиями: k={k_value}, r={r_value}, s={r_value}, z={r_value} (используя grep)...")
        
        try:
            # Используем grep для поиска строки с нужным паттерном
            # Паттерн: k;r;r;r;...
            grep_pattern = f"^{k_value};{r_value};{r_value};{r_value};"
            cmd = ['grep', '-m', '1', grep_pattern, self.csv_file_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                # Нашли строку
                line = result.stdout.strip()
                fields = line.split(';')
                
                print(f"✅ Найдена целевая строка!")
                
                # Конвертируем в числа где возможно
                converted_row = []
                for field in fields:
                    try:
                        converted_row.append(int(field))
                    except ValueError:
                        converted_row.append(field)
                
                return converted_row
            else:
                print(f"❌ Не найдена строка с заданными условиями")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"❌ Превышено время ожидания при поиске целевой строки")
            return None
        except Exception as e:
            print(f"❌ Ошибка при поиске целевой строки: {e}")
            return None
    
    def calculate_formula_value(self, row: list) -> str:
        """
        Вычисляет значение дополнительной формулы
        
        Args:
            row (list): Строка данных
            
        Returns:
            str: Вычисленное значение формулы
        """
        # Пример реализации формулы
        # В зависимости от ваших требований, здесь можно реализовать конкретную формулу
        # Пока возвращаем символическое значение 'x' как в вашем примере
        return 'x'
    
    def display_result(self, row: list):
        """
        Отображает результат в красивом табличном формате
        
        Args:
            row (list): Строка данных для отображения
        """
        print("\n" + "="*150)
        print("🎯 РЕЗУЛЬТАТ ПОИСКА ECDSA КЛЮЧА")
        print("="*150)
        
        # Добавляем значение формулы
        formula_value = self.calculate_formula_value(row)
        extended_row = row.copy()
        extended_row.append(formula_value)
        
        # Расширенные заголовки
        extended_headers = self.headers.copy()
        extended_headers.append("Формула")
        
        # Выводим в табличном формате как в вашем примере
        print(f"{'k':>8}{'r':>8}{'s':>8}{'z':>8}{'d':>8}{'ks+1':>8}{'ks+z':>8}{'(ks+1)/k':>10}{'(ks+z)/k':>10}{'d-k+1':>8}{'(d-k+1)/k':>12}{'((d-k+1)/k)^77':>15}{'d-k+z':>8}{'(d-k+z)/k':>12}{'((d-k+z)/k)^77':>15}{'Формула':>10}")
        print("-" * 150)
        
        # Выводим значения (убеждаемся что у нас достаточно колонок)
        if len(extended_row) >= 16:
            print(f"{extended_row[0]:>8}{extended_row[1]:>8}{extended_row[2]:>8}{extended_row[3]:>8}{extended_row[4]:>8}{extended_row[5]:>8}{extended_row[6]:>8}{extended_row[7]:>10}{extended_row[8]:>10}{extended_row[9]:>8}{extended_row[10]:>12}{extended_row[11]:>15}{extended_row[12]:>8}{extended_row[13]:>12}{extended_row[14]:>15}{extended_row[15]:>10}")
        else:
            # Если колонок меньше, выводим что есть
            formatted_values = []
            for i, value in enumerate(extended_row):
                formatted_values.append(f"{value:>8}")
            print("".join(formatted_values))
        
        print("="*150)
        
        # Дополнительная информация
        print("\n📊 ПОДРОБНАЯ ИНФОРМАЦИЯ:")
        for i, (header, value) in enumerate(zip(extended_headers, extended_row)):
            print(f"   {header}: {value}")
        
        print(f"\n💡 Пример вывода как в задаче:")
        if len(extended_row) >= 16:
            print(f"{extended_row[0]}\t{extended_row[1]}\t{extended_row[2]}\t{extended_row[3]}\t{extended_row[4]}\t{extended_row[5]}\t{extended_row[6]}\t{extended_row[7]}\t{extended_row[8]}\t{extended_row[9]}\t{extended_row[10]}\t{extended_row[11]}\t{extended_row[12]}\t{extended_row[13]}\t{extended_row[14]}\t{extended_row[15]}")
    
    def run(self):
        """
        Основная функция запуска программы
        """
        print("🚀 ECDSA Fast Key Finder - Сверхбыстрая система поиска ключей ECDSA")
        print("=" * 80)
        
        # Проверяем наличие grep
        try:
            subprocess.run(['grep', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Команда 'grep' не найдена. Убедитесь что grep установлен в системе.")
            return
        
        # Загружаем заголовки
        if not self.load_headers():
            print("❌ Не удалось загрузить заголовки. Завершение работы.")
            return
        
        while True:
            try:
                print("\n" + "-" * 80)
                print("📝 Введите значение k для поиска (или 'quit' для выхода):")
                
                user_input = input("👉 k = ").strip()
                
                # Проверка на выход
                if user_input.lower() in ['quit', 'exit', 'q', 'выход']:
                    print("👋 До свидания!")
                    break
                
                # Конвертируем в число
                k_value = int(user_input)
                
                print(f"\n🔄 Начинаю быстрый поиск для k = {k_value}")
                
                # Шаг 1: Быстро находим r для заданного k
                r_value = self.find_r_by_k_fast(k_value)
                if r_value is None:
                    print(f"❌ Не найдено значение r для k={k_value}")
                    continue
                
                # Шаг 2: Быстро находим строку с условиями
                target_row = self.find_target_row_fast(k_value, r_value)
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
        finder = ECDSAFastFinder()
        finder.run()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()