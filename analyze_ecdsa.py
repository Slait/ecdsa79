#!/usr/bin/env python3
"""
Искусственный интеллект для анализа ECDSA подписей
и поиска математических зависимостей для нахождения k из r,s,z

Эллиптическая кривая: y² = x³ + 7 (mod 67)
Базовая точка: (2, 22) (mod 67)
Модуль для d,k,s,z: 79
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import itertools
from typing import List, Dict, Tuple, Optional

class ECDSAAnalyzer:
    def __init__(self, csv_file: str):
        """Инициализация анализатора ECDSA"""
        self.csv_file = csv_file
        self.p = 67  # модуль для эллиптической кривой
        self.n = 79  # модуль для d,k,s,z
        self.base_point = (2, 22)
        self.data = None
        self.patterns = {}
        self.formulas = []
        
    def load_data(self):
        """Загрузка данных из CSV файла"""
        print("Загружаю данные из CSV файла...")
        try:
            # Читаем первые строки для понимания структуры
            self.data = pd.read_csv(self.csv_file, sep=';', nrows=50000)
            print(f"Загружено {len(self.data)} записей для анализа")
            print(f"Столбцы: {list(self.data.columns)}")
            return True
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return False
    
    def basic_statistics(self):
        """Базовая статистика по данным"""
        print("\n=== БАЗОВАЯ СТАТИСТИКА ===")
        print("Первые 10 записей:")
        print(self.data.head(10))
        
        print("\nОписательная статистика:")
        print(self.data.describe())
        
        print("\nУникальные значения:")
        for col in ['k', 'r', 's', 'z', 'd']:
            if col in self.data.columns:
                unique_count = self.data[col].nunique()
                print(f"{col}: {unique_count} уникальных значений")
            
    def analyze_ecdsa_properties(self):
        """Анализ основных свойств ECDSA"""
        print("\n=== АНАЛИЗ СВОЙСТВ ECDSA ===")
        
        # Проверяем базовые математические соотношения
        print("1. Проверяем формулу s = k^(-1)(z + rd) mod n")
        correct_s = 0
        total = min(len(self.data), 1000)  # Анализируем первые 1000 записей
        
        for idx in range(total):
            row = self.data.iloc[idx]
            k, r, s, z, d = int(row['k']), int(row['r']), int(row['s']), int(row['z']), int(row['d'])
            
            try:
                if k != 0:
                    # Вычисляем k^(-1) mod 79
                    k_inv = pow(k, -1, self.n)
                    # Проверяем s = k^(-1)(z + rd) mod 79
                    expected_s = (k_inv * (z + r * d)) % self.n
                    if expected_s == s:
                        correct_s += 1
            except:
                pass
                
        print(f"Корректных подписей: {correct_s}/{total} ({100*correct_s/total:.2f}%)")
        
        # Анализ зависимости k от других параметров
        print("\n2. Поиск зависимостей для k")
        self.find_k_patterns()
        
    def find_k_patterns(self):
        """Поиск паттернов для определения k"""
        print("\n=== ПОИСК ПАТТЕРНОВ ДЛЯ k ===")
        
        # Анализ корреляций
        print("Анализирую корреляции между параметрами...")
        
        numeric_cols = ['k', 'r', 's', 'z', 'd']
        for col in numeric_cols:
            if col != 'k' and col in self.data.columns:
                corr = np.corrcoef(self.data['k'].head(1000), self.data[col].head(1000))[0,1]
                print(f"Корреляция k-{col}: {corr:.4f}")
                
        # Поиск модульных зависимостей
        self.find_modular_patterns()
        
    def find_modular_patterns(self):
        """Поиск модульных паттернов"""
        print("\n=== ПОИСК МОДУЛЬНЫХ ПАТТЕРНОВ ===")
        
        potential_formulas = []
        sample_size = min(1000, len(self.data))
        
        # Проверяем различные линейные комбинации
        for a in range(1, 6):
            for b in range(1, 6):
                for c in range(1, 6):
                    formula_results = []
                    for idx in range(sample_size):
                        row = self.data.iloc[idx]
                        r, s, z, k = int(row['r']), int(row['s']), int(row['z']), int(row['k'])
                        
                        # k ≡ ar + bs + cz (mod 79)
                        calculated_k = (a * r + b * s + c * z) % self.n
                        formula_results.append(calculated_k == k)
                        
                    accuracy = sum(formula_results) / len(formula_results)
                    if accuracy > 0.05:  # Если формула работает более чем в 5% случаев
                        potential_formulas.append({
                            'formula': f'k ≡ {a}r + {b}s + {c}z (mod 79)',
                            'accuracy': accuracy,
                            'coefficients': (a, b, c)
                        })
                        
        # Сортируем по точности
        potential_formulas.sort(key=lambda x: x['accuracy'], reverse=True)
        
        print("Найденные потенциальные формулы:")
        for formula in potential_formulas[:10]:
            print(f"  {formula['formula']}: точность {formula['accuracy']:.3f}")
            
        return potential_formulas
        
    def symbolic_analysis(self):
        """Символьный анализ"""
        print("\n=== СИМВОЛЬНЫЙ АНАЛИЗ ===")
        
        print("Анализирую обратные соотношения ECDSA...")
        
        # Для каждой записи пытаемся найти k через обращение
        successful_inversions = 0
        failed_inversions = 0
        sample_size = min(1000, len(self.data))
        
        for idx in range(sample_size):
            row = self.data.iloc[idx]
            k_val, r_val, s_val, z_val, d_val = (
                int(row['k']), int(row['r']), int(row['s']), 
                int(row['z']), int(row['d'])
            )
            
            try:
                if s_val != 0:
                    s_inv = pow(s_val, -1, self.n)
                    calculated_k = (s_inv * (z_val + r_val * d_val)) % self.n
                    
                    if calculated_k == k_val:
                        successful_inversions += 1
                    else:
                        failed_inversions += 1
            except:
                failed_inversions += 1
                
        print(f"Успешных обращений: {successful_inversions}")
        print(f"Неудачных обращений: {failed_inversions}")
        
        # Поиск альтернативных формул
        self.find_alternative_formulas()
        
    def find_alternative_formulas(self):
        """Поиск альтернативных формул для k"""
        print("\nИщу альтернативные способы вычисления k...")
        
        formulas_found = []
        sample_size = min(1000, len(self.data))
        
        for idx in range(sample_size):
            row = self.data.iloc[idx]
            k_val, r_val, s_val, z_val = (
                int(row['k']), int(row['r']), int(row['s']), int(row['z'])
            )
            
            # Проверяем простые арифметические соотношения
            candidates = [
                ('r + s + z', (r_val + s_val + z_val) % self.n),
                ('r * s + z', (r_val * s_val + z_val) % self.n),
                ('r + s * z', (r_val + s_val * z_val) % self.n),
                ('(r + s) * z', ((r_val + s_val) * z_val) % self.n),
                ('r * s * z', (r_val * s_val * z_val) % self.n),
                ('r^2 + s + z', (r_val * r_val + s_val + z_val) % self.n),
                ('r + s^2 + z', (r_val + s_val * s_val + z_val) % self.n),
                ('r + s + z^2', (r_val + s_val + z_val * z_val) % self.n),
            ]
            
            for formula_name, calculated_value in candidates:
                if calculated_value == k_val:
                    formulas_found.append({
                        'formula': formula_name,
                        'row': idx,
                        'values': (k_val, r_val, s_val, z_val)
                    })
                    
        # Группируем найденные формулы
        formula_counts = defaultdict(int)
        for f in formulas_found:
            formula_counts[f['formula']] += 1
            
        print("Частота срабатывания альтернативных формул:")
        for formula, count in sorted(formula_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / sample_size) * 100
            if percentage > 0.1:
                print(f"  {formula}: {count} раз ({percentage:.2f}%)")
                
        return formula_counts
        
    def generate_report(self):
        """Генерация итогового отчета"""
        print("\n" + "="*60)
        print("ИТОГОВЫЙ ОТЧЕТ АНАЛИЗА ECDSA")
        print("="*60)
        
        print(f"\nПараметры анализа:")
        print(f"  Эллиптическая кривая: y² ≡ x³ + 7 (mod {self.p})")
        print(f"  Базовая точка: {self.base_point}")
        print(f"  Модуль для k,s,z,d: {self.n}")
        print(f"  Количество проанализированных записей: {len(self.data)}")
        
        print(f"\nОсновные выводы:")
        print(f"  1. ECDSA использует стандартную формулу s ≡ k⁻¹(z + rd) (mod {self.n})")
        print(f"  2. Для нахождения k из известных r,s,z,d используется формула:")
        print(f"     k ≡ s⁻¹(z + rd) (mod {self.n})")
        print(f"  3. Альтернативные простые формулы показывают низкую эффективность")
        
        print(f"\nРекомендуемые формулы для нахождения k:")
        print(f"  ГЛАВНАЯ ФОРМУЛА: k ≡ s⁻¹(z + rd) (mod 79)")
        print(f"  где s⁻¹ - мультипликативное обращение s по модулю 79")
        
    def run_full_analysis(self):
        """Запуск полного анализа"""
        print("Запускаю полный анализ ECDSA подписей...")
        
        if not self.load_data():
            return False
            
        self.basic_statistics()
        self.analyze_ecdsa_properties()
        self.symbolic_analysis()
        self.generate_report()
        
        return True

def main():
    """Главная функция"""
    print("Искусственный интеллект для анализа ECDSA подписей")
    print("Поиск математических формул для нахождения k из r,s,z")
    print("-" * 60)
    
    analyzer = ECDSAAnalyzer('escda79.csv')
    
    success = analyzer.run_full_analysis()
    
    if success:
        print("\nАнализ завершен успешно!")
    else:
        print("\nПроизошла ошибка при анализе.")
        
    return analyzer

if __name__ == "__main__":
    analyzer = main()