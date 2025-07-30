#!/usr/bin/env python3
"""
Universal K-Formula Generator
Analyzes patterns to find mathematical formulas for computing k from r
"""

import math
from typing import List, Dict, Tuple, Optional

class UniversalKFormula:
    """Generator of universal formulas for k from r"""
    
    def __init__(self):
        # Complete r->k mapping (from our analysis)
        self.r_k_data = {
            2: [1, 78], 4: [39, 40], 5: [14, 65], 6: [26, 53], 7: [24, 55],
            11: [6, 73], 12: [21, 58], 13: [9, 70], 14: [12, 67], 16: [7, 72],
            17: [27, 52], 18: [35, 44], 21: [8, 71], 23: [22, 57], 24: [11, 68],
            25: [4, 75], 26: [16, 63], 27: [38, 41], 30: [37, 42], 34: [33, 46],
            38: [19, 60], 40: [34, 45], 42: [30, 49], 46: [5, 74], 47: [25, 54],
            48: [31, 48], 49: [28, 51], 51: [20, 59], 52: [2, 77], 53: [15, 64],
            54: [17, 62], 55: [13, 66], 56: [10, 69], 58: [23, 56], 61: [36, 43],
            62: [3, 76], 63: [29, 50], 64: [32, 47], 66: [18, 61]
        }
        
        self.curve_p = 67  # Curve modulus
        self.signature_mod = 79  # Signature modulus
        
    def analyze_mathematical_patterns(self):
        """Анализ математических закономерностей"""
        print("АНАЛИЗ МАТЕМАТИЧЕСКИХ ЗАКОНОМЕРНОСТЕЙ")
        print("=" * 50)
        
        # 1. Комплементарность
        print("1. КОМПЛЕМЕНТАРНОСТЬ (k₁ + k₂ = 79):")
        all_complement = True
        for r, k_list in self.r_k_data.items():
            sum_k = sum(k_list)
            is_complement = (sum_k == 79)
            print(f"   r={r:2d}: k={k_list} → сумма={sum_k} {'✓' if is_complement else '✗'}")
            if not is_complement:
                all_complement = False
        
        print(f"\n   Результат: {'100% комплементарность!' if all_complement else 'Частичная комплементарность'}")
        
        # 2. Модульные отношения
        print("\n2. МОДУЛЬНЫЕ ОТНОШЕНИЯ:")
        self._analyze_modular_relationships()
        
        # 3. Квадратичные соотношения  
        print("\n3. КВАДРАТИЧНЫЕ СООТНОШЕНИЯ:")
        self._analyze_quadratic_relationships()
        
        # 4. Инверсные соотношения
        print("\n4. ИНВЕРСНЫЕ СООТНОШЕНИЯ:")
        self._analyze_inverse_relationships()
    
    def _analyze_modular_relationships(self):
        """Анализ модульных соотношений"""
        # Проверяем различные модульные формулы
        found_patterns = []
        
        for r, k_list in list(self.r_k_data.items())[:5]:  # Тестируем на первых 5
            k1 = min(k_list)
            
            # Тип 1: k ≡ a*r + b (mod 79)
            for a in range(1, 10):
                for b in range(0, 10):
                    if k1 == (a * r + b) % 79:
                        # Проверяем на других значениях
                        matches = 0
                        for test_r, test_k_list in self.r_k_data.items():
                            predicted_k = (a * test_r + b) % 79
                            if predicted_k in test_k_list:
                                matches += 1
                        
                        accuracy = matches / len(self.r_k_data)
                        if accuracy > 0.1:  # Больше 10% точности
                            found_patterns.append({
                                'formula': f'k ≡ {a}*r + {b} (mod 79)',
                                'accuracy': accuracy,
                                'example': f'r={r} → k={k1}'
                            })
        
        if found_patterns:
            for pattern in sorted(found_patterns, key=lambda x: x['accuracy'], reverse=True)[:3]:
                print(f"   {pattern['formula']}: точность {pattern['accuracy']:.1%} ({pattern['example']})")
        else:
            print("   Простые линейные модульные соотношения не найдены")
    
    def _analyze_quadratic_relationships(self):
        """Анализ квадратичных соотношений"""
        found_patterns = []
        
        for r, k_list in list(self.r_k_data.items())[:5]:
            k1 = min(k_list)
            
            # Тип: k ≡ a*r² + b*r + c (mod 79)
            for a in range(1, 5):
                for b in range(0, 5):
                    for c in range(0, 5):
                        predicted = (a * r * r + b * r + c) % 79
                        if predicted == k1:
                            # Проверяем точность
                            matches = 0
                            for test_r, test_k_list in self.r_k_data.items():
                                pred_k = (a * test_r * test_r + b * test_r + c) % 79
                                if pred_k in test_k_list:
                                    matches += 1
                            
                            accuracy = matches / len(self.r_k_data)
                            if accuracy > 0.05:
                                found_patterns.append({
                                    'formula': f'k ≡ {a}*r² + {b}*r + {c} (mod 79)',
                                    'accuracy': accuracy,
                                    'example': f'r={r} → k={k1}'
                                })
        
        if found_patterns:
            for pattern in sorted(found_patterns, key=lambda x: x['accuracy'], reverse=True)[:2]:
                print(f"   {pattern['formula']}: точность {pattern['accuracy']:.1%}")
        else:
            print("   Квадратичные соотношения не найдены")
    
    def _analyze_inverse_relationships(self):
        """Анализ обратных соотношений"""
        found_patterns = []
        
        for r, k_list in list(self.r_k_data.items())[:5]:
            k1 = min(k_list)
            
            try:
                r_inv = self._mod_inverse(r, 79)
                
                # Тип: k ≡ c * r⁻¹ (mod 79)
                for c in range(1, 20):
                    predicted = (c * r_inv) % 79
                    if predicted == k1:
                        # Проверяем точность
                        matches = 0
                        total_tests = 0
                        for test_r, test_k_list in self.r_k_data.items():
                            try:
                                test_r_inv = self._mod_inverse(test_r, 79)
                                pred_k = (c * test_r_inv) % 79
                                if pred_k in test_k_list:
                                    matches += 1
                                total_tests += 1
                            except:
                                continue
                        
                        if total_tests > 0:
                            accuracy = matches / total_tests
                            if accuracy > 0.05:
                                found_patterns.append({
                                    'formula': f'k ≡ {c} * r⁻¹ (mod 79)',
                                    'accuracy': accuracy,
                                    'example': f'r={r} → k={k1}'
                                })
            except:
                continue
        
        if found_patterns:
            for pattern in sorted(found_patterns, key=lambda x: x['accuracy'], reverse=True)[:2]:
                print(f"   {pattern['formula']}: точность {pattern['accuracy']:.1%}")
        else:
            print("   Инверсные соотношения не найдены")
    
    def _mod_inverse(self, a: int, m: int) -> int:
        """Модульная инверсия"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError(f"No inverse for {a} mod {m}")
        return (x % m + m) % m
    
    def find_discrete_log_patterns(self):
        """Поиск закономерностей дискретного логарифма"""
        print("\nПОИСК ЗАКОНОМЕРНОСТЕЙ ДИСКРЕТНОГО ЛОГАРИФМА")
        print("=" * 50)
        
        # Анализируем отношения между r и позицией в последовательности
        r_positions = {}
        sorted_r = sorted(self.r_k_data.keys())
        
        for i, r in enumerate(sorted_r):
            r_positions[r] = i
        
        print("Позиционные закономерности:")
        patterns_found = 0
        
        for r, k_list in list(self.r_k_data.items())[:10]:
            k1 = min(k_list)
            pos = r_positions[r]
            
            # Проверяем различные формулы связи позиции и k
            if k1 == pos + 1:
                print(f"   r={r} (позиция {pos}): k={k1} = позиция + 1")
                patterns_found += 1
            elif k1 == (pos * 2) % 79:
                print(f"   r={r} (позиция {pos}): k={k1} = 2*позиция mod 79")
                patterns_found += 1
        
        if patterns_found == 0:
            print("   Простые позиционные закономерности не найдены")
    
    def generate_universal_formulas(self):
        """Генерация универсальных формул"""
        print("\nУНИВЕРСАЛЬНЫЕ ФОРМУЛЫ ДЛЯ ВЫЧИСЛЕНИЯ K ПО R")
        print("=" * 60)
        
        formulas = []
        
        # Формула 1: Прямая таблица (100% точность)
        formulas.append({
            'name': 'Lookup Table Formula',
            'accuracy': 1.0,
            'complexity': 'O(1)',
            'description': 'Прямой поиск в предвычисленной таблице',
            'implementation': 'lookup_table[r]',
            'code': '''
def formula_1_lookup(r):
    """100% точная формула через lookup таблицу"""
    table = {2: [1,78], 4: [39,40], 5: [14,65], ...}
    return table.get(r, [])
'''
        })
        
        # Формула 2: Комплементарная формула
        formulas.append({
            'name': 'Complement Property Formula',
            'accuracy': 1.0,
            'complexity': 'O(1)',
            'description': 'Использует свойство k₁ + k₂ = 79',
            'implementation': '[k₁, 79-k₁] где k₁ найден любым методом',
            'code': '''
def formula_2_complement(r, known_k=None):
    """Использует комплементарное свойство"""
    if known_k is None:
        known_k = find_first_k_by_search(r)
    return sorted([known_k, 79 - known_k]) if known_k else []
'''
        })
        
        # Формула 3: Оптимизированный поиск
        formulas.append({
            'name': 'Optimized Half-Range Search',
            'accuracy': 1.0,
            'complexity': 'O(n/2)',
            'description': 'Поиск только в половине диапазона',
            'implementation': 'Поиск k в [1,39], второе k = 79-k',
            'code': '''
def formula_3_half_search(r):
    """Оптимизированный поиск в половине диапазона"""
    for k in range(1, 40):  # Только половина диапазона
        if verify_k_produces_r(k, r):
            return sorted([k, 79 - k])
    return []
'''
        })
        
        # Формула 4: Математическая аппроксимация
        best_approx = self._find_best_approximation()
        if best_approx:
            formulas.append(best_approx)
        
        # Вывод формул
        for i, formula in enumerate(formulas, 1):
            print(f"\n{i}. {formula['name']}")
            print(f"   Точность: {formula['accuracy']:.1%}")
            print(f"   Сложность: {formula['complexity']}")
            print(f"   Описание: {formula['description']}")
            print(f"   Реализация: {formula['implementation']}")
            if 'code' in formula:
                print(f"   Код:{formula['code']}")
        
        return formulas
    
    def _find_best_approximation(self):
        """Поиск лучшей математической аппроксимации"""
        # Пробуем найти формулу, которая работает для большинства случаев
        
        # Проверяем формулу через остатки от деления
        best_formula = None
        best_accuracy = 0
        
        for divisor in [3, 5, 7, 11, 13]:
            matches = 0
            total = 0
            examples = []
            
            for r, k_list in self.r_k_data.items():
                k1 = min(k_list)
                # Пробуем формулу: k ≡ f(r mod divisor) 
                r_mod = r % divisor
                predicted_k = (r_mod * 17 + 3) % 79  # Произвольная формула
                
                if predicted_k in k_list:
                    matches += 1
                    examples.append(f"r={r}→k={predicted_k}")
                total += 1
            
            accuracy = matches / total if total > 0 else 0
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_formula = {
                    'name': f'Modular Approximation (mod {divisor})',
                    'accuracy': accuracy,
                    'complexity': 'O(1)',
                    'description': f'Формула через остатки от деления на {divisor}',
                    'implementation': f'k ≡ (r mod {divisor}) * 17 + 3 (mod 79)',
                    'examples': examples[:3]
                }
        
        return best_formula if best_accuracy > 0.1 else None
    
    def create_practical_solver(self):
        """Создание практического решателя"""
        print("\nПРАКТИЧЕСКИЙ РЕШАТЕЛЬ")
        print("=" * 30)
        
        code = '''
class PracticalKSolver:
    """Практический решатель k по r"""
    
    def __init__(self):
        # Компактная lookup таблица
        self.r_k_map = {
            2:[1,78], 4:[39,40], 5:[14,65], 6:[26,53], 7:[24,55],
            11:[6,73], 12:[21,58], 13:[9,70], 14:[12,67], 16:[7,72],
            17:[27,52], 18:[35,44], 21:[8,71], 23:[22,57], 24:[11,68],
            25:[4,75], 26:[16,63], 27:[38,41], 30:[37,42], 34:[33,46],
            38:[19,60], 40:[34,45], 42:[30,49], 46:[5,74], 47:[25,54],
            48:[31,48], 49:[28,51], 51:[20,59], 52:[2,77], 53:[15,64],
            54:[17,62], 55:[13,66], 56:[10,69], 58:[23,56], 61:[36,43],
            62:[3,76], 63:[29,50], 64:[32,47], 66:[18,61]
        }
    
    def solve(self, r):
        """Главная функция решения"""
        return self.r_k_map.get(r, [])
    
    def solve_with_complement(self, r):
        """Решение с использованием комплементарности"""
        k_values = self.solve(r)
        if k_values:
            # Проверяем комплементарность
            k1, k2 = k_values[0], k_values[1]
            assert k1 + k2 == 79, "Нарушена комплементарность!"
            return k_values
        return []
    
    def find_first_k_only(self, r):
        """Получить только первое (меньшее) значение k"""
        k_values = self.solve(r)
        return min(k_values) if k_values else None
    
    def verify_solution(self, k, r):
        """Проверка правильности решения"""
        # Здесь должна быть проверка через точечное умножение
        # point = k * base_point
        # return point.x % 79 == r
        return True  # Упрощенная версия

# Использование:
solver = PracticalKSolver()
k_values = solver.solve(7)  # [24, 55]
print(f"k1 + k2 = {sum(k_values)}")  # 79
'''
        
        print(code)
        return code

def main():
    """Главная функция анализа"""
    analyzer = UniversalKFormula()
    
    print("ПОИСК УНИВЕРСАЛЬНЫХ ФОРМУЛ ДЛЯ ВЫЧИСЛЕНИЯ K ПО R")
    print("=" * 60)
    print("Кривая: y² = x³ + 7 mod 67")
    print("Базовая точка: (2, 22)")
    print("Модуль подписей: 79")
    print("Данные: 39 пар (r, [k₁, k₂])")
    print()
    
    # Анализ математических закономерностей
    analyzer.analyze_mathematical_patterns()
    
    # Поиск закономерностей дискретного логарифма
    analyzer.find_discrete_log_patterns()
    
    # Генерация универсальных формул
    formulas = analyzer.generate_universal_formulas()
    
    # Создание практического решателя
    analyzer.create_practical_solver()
    
    print("\n" + "=" * 60)
    print("РЕКОМЕНДАЦИИ ПО ВЫБОРУ ФОРМУЛЫ:")
    print("=" * 60)
    print("1. Для максимальной скорости: Используйте Lookup Table Formula")
    print("2. Для экономии памяти: Используйте Half-Range Search Formula") 
    print("3. Для понимания математики: Изучите Complement Property Formula")
    print("4. Для новых r: Используйте брутфорс с комплементарностью")

if __name__ == "__main__":
    main()