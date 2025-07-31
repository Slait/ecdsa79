#!/usr/bin/env python3
"""
Искусственный интеллект для анализа ECDSA подписей
Поиск математических формул для нахождения k из r,s,z
"""

import csv

class ECDSAAnalyzer:
    def __init__(self):
        self.n = 79
        self.data = []
        
    def mod_inverse(self, a, m):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            return None
        return (x % m + m) % m
    
    def load_data(self, filename, max_rows=5000):
        print(f"Загружаю данные из {filename}...")
        try:
            with open(filename, 'r') as f:
                reader = csv.DictReader(f, delimiter=';')
                count = 0
                for row in reader:
                    if count >= max_rows:
                        break
                    self.data.append({
                        'k': int(row['k']),
                        'r': int(row['r']),
                        's': int(row['s']),
                        'z': int(row['z']),
                        'd': int(row['d'])
                    })
                    count += 1
            print(f"Загружено {len(self.data)} записей")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    
    def find_k_formula(self):
        print("\n=== ПОИСК ФОРМУЛЫ ДЛЯ k ===")
        print("Тестирую: k ≡ s⁻¹(z + rd) (mod 79)")
        
        successful = 0
        sample_size = min(len(self.data), 1000)
        examples = []
        
        for i in range(sample_size):
            row = self.data[i]
            k_true, r, s, z, d = row['k'], row['r'], row['s'], row['z'], row['d']
            
            if s != 0:
                s_inv = self.mod_inverse(s, self.n)
                if s_inv:
                    k_calc = (s_inv * (z + r * d)) % self.n
                    if k_calc == k_true:
                        successful += 1
                        if len(examples) < 5:
                            examples.append({
                                'r': r, 's': s, 'z': z, 'd': d,
                                'k_true': k_true, 'k_calc': k_calc
                            })
                            
        accuracy = successful / sample_size
        print(f"Точность: {successful}/{sample_size} ({accuracy*100:.1f}%)")
        
        print("\nПримеры успешного нахождения k:")
        for i, ex in enumerate(examples):
            print(f"  {i+1}. r={ex['r']}, s={ex['s']}, z={ex['z']}, d={ex['d']}")
            print(f"     k_истинное={ex['k_true']}, k_найденное={ex['k_calc']}")
            
        return accuracy, examples
    
    def generate_report(self):
        print("\n" + "="*60)
        print("ОТЧЕТ: МАТЕМАТИЧЕСКИЕ ФОРМУЛЫ ДЛЯ НАХОЖДЕНИЯ k")
        print("="*60)
        
        print("\nОСНОВНАЯ ФОРМУЛА (РЕКОМЕНДУЕМАЯ):")
        print("  k ≡ s⁻¹(z + rd) (mod 79)")
        print("\nГДЕ:")
        print("  s⁻¹ - обратный элемент s по модулю 79")
        print("  r, s - компоненты подписи ECDSA")
        print("  z - хеш сообщения")
        print("  d - приватный ключ")
        
        print("\nАЛГОРИТМ ВЫЧИСЛЕНИЯ:")
        print("  1. Проверить s ≠ 0")
        print("  2. Найти s⁻¹ mod 79 (расширенный алгоритм Евклида)")
        print("  3. Вычислить k = s⁻¹(z + rd) mod 79")
        
    def run_analysis(self):
        print("🤖 ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ ДЛЯ АНАЛИЗА ECDSA")
        print("Поиск формул для нахождения k из r,s,z")
        print("-" * 60)
        
        if not self.load_data('escda79.csv'):
            return False
            
        self.find_k_formula()
        self.generate_report()
        
        print("\n✅ АНАЛИЗ ЗАВЕРШЕН!")
        return True

def main():
    analyzer = ECDSAAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
