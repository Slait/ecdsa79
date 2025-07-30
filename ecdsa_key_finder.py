#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECDSA Key Finder Script (Extended Version with 15 Keys)
=======================================================

Правильная логика поиска 15 ключей:
1. Ключ1: k=k, r=r, s=r, z=r → "x"
2. Ключ2: k=k, r=r, s=0, d=1 → "Первый ключ" (запоминаем z)
3. Ключ3: k=k, r=r, s=0, z=ключ2.z*16, d=16 → "16 ключ"
4. Ключ4: k=k, r=r, s=ключ1.s-ключ3.s, z=ключ1.z-ключ3.z → "-y"
5. Ключ5: k=k, r=r, s=-ключ4.s, z=-ключ4.z → "y"
6. Ключ6: k=k, r=r, s=ключ1.s*ключ1.d, z=ключ1.z*ключ1.d → "x^2 секретно"
7. Ключ7: k=k, r=r, s=ключ5.s*ключ5.d, z=ключ5.z*ключ5.d → "y^2 секретно"
8. Ключ8: k=k, r=r, s=ключ6.s+ключ7.s, z=ключ6.z+ключ7.z → "x^2+y^2 секретно"
9. Ключ9: k=k, r=r, s=ключ3.s*16, z=ключ3.z*16 → "16^2=19, (x+y)^2=x^2 + 2xy + y^2"
10. Ключ10: k=k, r=r, s=ключ6.s+ключ7.s, z=-ключ6.z+ключ7.z → "x^2+y^2 секретно"
11. Ключ11: k=k, r=r, s=ключ5.s*16, z=ключ5.z*16 → "(x+y)*y=16*y=y^2+xy"
12. Ключ12: k=k, r=ключ1.r, s=ключ1.s*16, z=ключ1.z*16 → "(x+y)*x=16*x=x^2+xy"
13. Ключ13: k=k, r=ключ1.r, s=ключ1.s-ключ5.s, z=ключ1.z-ключ5.z → "(x - y)"
14. Ключ14: k=k, r=ключ1.r, s=ключ5.s-ключ1.s, z=ключ5.z-ключ1.z → "(y - x) ниже диапазона"
15. Ключ15: k=k, r=ключ1.r, s=ключ9.s-(32*ключ5.s), z=ключ9.z-(32*ключ5.z) → "x^2-y^2"

Все расчеты по модулю 79
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
        """Находит все 15 ключей для заданного k"""
        print(f"🔍 Поиск всех ключей для k={k_value}")
        
        # Фильтруем только строки с нужным k
        k_rows = [row for row in self.data if row[0] == k_value]
        print(f"📊 Найдено {len(k_rows)} строк с k={k_value}")
        
        if not k_rows:
            print(f"❌ Нет данных для k={k_value}")
            return []
        
        # Ключ 1: k=k, r=r, s=r, z=r
        key1 = None
        for row in k_rows:
            if row[2] == row[1] and row[3] == row[1]:  # s=r и z=r
                key1 = row
                key1_k = key1[0]  # k
                key1_r = key1[1]  # r
                key1_s = key1[2]  # s
                key1_z = key1[3]  # z
                print(f"✅ Ключ 1: k={key1_k}, r={key1_r}, s={key1_s}, z={key1_z}")
                break
        
        if not key1:
            print(f"❌ Ключ 1 не найден (k={k_value}, s=r, z=r)")
            return []
        
        # Ключ 2: k=k, r=key1.r, s=0, d=1
        key2 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == 0 and row[4] == 1:  # r=key1.r, s=0, d=1
                key2 = row
                key2_z = row[3]  # запоминаем z
                print(f"✅ Ключ 2: k={row[0]}, r={row[1]}, s={row[2]}, z={key2_z}, d={row[4]}")
                break
        
        if not key2:
            print(f"❌ Ключ 2 не найден (k={k_value}, r={key1_r}, s=0, d=1)")
            return [(key1, "x")]
        
        # Ключ 3: k=k, r=key1.r, s=0, z=key2.z*16, d=16
        key3_z = (key2_z * 16) % 79
        key3 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == 0 and row[3] == key3_z and row[4] == 16:
                key3 = row
                print(f"✅ Ключ 3: k={row[0]}, r={row[1]}, s={row[2]}, z={key3_z}, d={row[4]}")
                break
        
        if not key3:
            print(f"❌ Ключ 3 не найден (k={k_value}, r={key1_r}, s=0, z={key3_z}, d=16)")
            return [(key1, "x"), (key2, "Первый ключ")]
        
        # Ключ 4: k=k, r=key1.r, s=key1.s-key3.s, z=key1.z-key3.z
        key4_s = (key1_s - key3[2]) % 79
        key4_z = (key1_z - key3[3]) % 79
        key4 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key4_s and row[3] == key4_z:
                key4 = row
                print(f"✅ Ключ 4: k={row[0]}, r={row[1]}, s={key4_s}, z={key4_z}")
                break
        
        if not key4:
            print(f"❌ Ключ 4 не найден (k={k_value}, r={key1_r}, s={key4_s}, z={key4_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ")]
        
        # Ключ 5: k=k, r=key1.r, s=-key4.s, z=-key4.z
        key5_s = (-key4_s) % 79
        key5_z = (-key4_z) % 79
        key5 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key5_s and row[3] == key5_z:
                key5 = row
                print(f"✅ Ключ 5: k={row[0]}, r={row[1]}, s={key5_s}, z={key5_z}")
                break
        
        if not key5:
            print(f"❌ Ключ 5 не найден (k={k_value}, r={key1_r}, s={key5_s}, z={key5_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y")]
        
        # Ключ 6: k=k, r=r, s=key1.s*key1.d, z=key1.z*key1.d
        key6_s = (key1_s * key1[4]) % 79  # s = key1.s * key1.d
        key6_z = (key1_z * key1[4]) % 79  # z = key1.z * key1.d
        key6 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key6_s and row[3] == key6_z:
                key6 = row
                print(f"✅ Ключ 6: k={row[0]}, r={row[1]}, s={key6_s}, z={key6_z}")
                break
        
        if not key6:
            print(f"❌ Ключ 6 не найден (k={k_value}, r={key1_r}, s={key6_s}, z={key6_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y")]
        
        # Ключ 7: k=k, r=key1.r, s=key5.s*key5.d, z=key5.z*key5.d
        key7_s = (key5[2] * key5[4]) % 79  # s = key5.s * key5.d
        key7_z = (key5[3] * key5[4]) % 79  # z = key5.z * key5.d
        key7 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key7_s and row[3] == key7_z:
                key7 = row
                print(f"✅ Ключ 7: k={row[0]}, r={row[1]}, s={key7_s}, z={key7_z}")
                break
        
        if not key7:
            print(f"❌ Ключ 7 не найден (k={k_value}, r={key1_r}, s={key7_s}, z={key7_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно")]
        
        # Ключ 8: k=k, r=key1.r, s=key6.s+key7.s, z=key6.z+key7.z
        key8_s = (key6_s + key7_s) % 79
        key8_z = (key6_z + key7_z) % 79
        key8 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key8_s and row[3] == key8_z:
                key8 = row
                print(f"✅ Ключ 8: k={row[0]}, r={row[1]}, s={key8_s}, z={key8_z}")
                break
        
        if not key8:
            print(f"❌ Ключ 8 не найден (k={k_value}, r={key1_r}, s={key8_s}, z={key8_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно"), (key7, "y^2 секретно")]
        
        # Ключ 9: k=k, r=key1.r, s=key3.s*16, z=key3.z*16
        key9_s = (key3[2] * 16) % 79
        key9_z = (key3[3] * 16) % 79
        key9 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key9_s and row[3] == key9_z:
                key9 = row
                print(f"✅ Ключ 9: k={row[0]}, r={row[1]}, s={key9_s}, z={key9_z}")
                break
        
        if not key9:
            print(f"❌ Ключ 9 не найден (k={k_value}, r={key1_r}, s={key9_s}, z={key9_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно"), (key7, "y^2 секретно"), (key8, "x^2+y^2 секретно")]
        
        # Ключ 10: k=k, r=key1.r, s=key6.s+key7.s, z=-key6.z+key7.z
        key10_s = (key6_s + key7_s) % 79
        key10_z = (-key6_z + key7_z) % 79
        key10 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key10_s and row[3] == key10_z:
                key10 = row
                print(f"✅ Ключ 10: k={row[0]}, r={row[1]}, s={key10_s}, z={key10_z}")
                break
        
        if not key10:
            print(f"❌ Ключ 10 не найден (k={k_value}, r={key1_r}, s={key10_s}, z={key10_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно"), (key7, "y^2 секретно"), (key8, "x^2+y^2 секретно"), (key9, "16^2=19, (x+y)^2=x^2 + 2xy + y^2")]
        
        # Ключ 11: k=k, r=key1.r, s=key5.s*16, z=key5.z*16
        key11_s = (key5[2] * 16) % 79
        key11_z = (key5[3] * 16) % 79
        key11 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key11_s and row[3] == key11_z:
                key11 = row
                print(f"✅ Ключ 11: k={row[0]}, r={row[1]}, s={key11_s}, z={key11_z}")
                break
        
        if not key11:
            print(f"❌ Ключ 11 не найден (k={k_value}, r={key1_r}, s={key11_s}, z={key11_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно"), (key7, "y^2 секретно"), (key8, "x^2+y^2 секретно"), (key9, "16^2=19, (x+y)^2=x^2 + 2xy + y^2"), (key10, "x^2+y^2 секретно")]
        
        # Ключ 12: k=k, r=key1.r, s=key1.s*16, z=key1.z*16
        key12_s = (key1_s * 16) % 79
        key12_z = (key1_z * 16) % 79
        key12 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key12_s and row[3] == key12_z:
                key12 = row
                print(f"✅ Ключ 12: k={row[0]}, r={row[1]}, s={key12_s}, z={key12_z}")
                break
        
        if not key12:
            print(f"❌ Ключ 12 не найден (k={k_value}, r={key1_r}, s={key12_s}, z={key12_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно"), (key7, "y^2 секретно"), (key8, "x^2+y^2 секретно"), (key9, "16^2=19, (x+y)^2=x^2 + 2xy + y^2"), (key10, "x^2+y^2 секретно"), (key11, "(x+y)*y=16*y=y^2+xy")]
        
        # Ключ 13: k=k, r=key1.r, s=key1.s-key5.s, z=key1.z-key5.z
        key13_s = (key1_s - key5[2]) % 79
        key13_z = (key1_z - key5[3]) % 79
        key13 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key13_s and row[3] == key13_z:
                key13 = row
                print(f"✅ Ключ 13: k={row[0]}, r={row[1]}, s={key13_s}, z={key13_z}")
                break
        
        if not key13:
            print(f"❌ Ключ 13 не найден (k={k_value}, r={key1_r}, s={key13_s}, z={key13_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно"), (key7, "y^2 секретно"), (key8, "x^2+y^2 секретно"), (key9, "16^2=19, (x+y)^2=x^2 + 2xy + y^2"), (key10, "x^2+y^2 секретно"), (key11, "(x+y)*y=16*y=y^2+xy"), (key12, "(x+y)*x=16*x=x^2+xy")]
        
        # Ключ 14: k=k, r=key1.r, s=key5.s-key1.s, z=key5.z-key1.z
        key14_s = (key5[2] - key1_s) % 79
        key14_z = (key5[3] - key1_z) % 79
        key14 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key14_s and row[3] == key14_z:
                key14 = row
                print(f"✅ Ключ 14: k={row[0]}, r={row[1]}, s={key14_s}, z={key14_z}")
                break
        
        if not key14:
            print(f"❌ Ключ 14 не найден (k={k_value}, r={key1_r}, s={key14_s}, z={key14_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно"), (key7, "y^2 секретно"), (key8, "x^2+y^2 секретно"), (key9, "16^2=19, (x+y)^2=x^2 + 2xy + y^2"), (key10, "x^2+y^2 секретно"), (key11, "(x+y)*y=16*y=y^2+xy"), (key12, "(x+y)*x=16*x=x^2+xy"), (key13, "(x - y)")]
        
        # Ключ 15: k=k, r=key1.r, s=key9.s-(32*key5.s), z=key9.z-(32*key5.z)
        key15_s = (key9_s - (32 * key5[2])) % 79
        key15_z = (key9_z - (32 * key5[3])) % 79
        key15 = None
        for row in k_rows:
            if row[1] == key1_r and row[2] == key15_s and row[3] == key15_z:
                key15 = row
                print(f"✅ Ключ 15: k={row[0]}, r={row[1]}, s={key15_s}, z={key15_z}")
                break
        
        if not key15:
            print(f"❌ Ключ 15 не найден (k={k_value}, r={key1_r}, s={key15_s}, z={key15_z})")
            return [(key1, "x"), (key2, "Первый ключ"), (key3, "16 ключ"), (key4, "-y"), (key5, "y"), (key6, "x^2 секретно"), (key7, "y^2 секретно"), (key8, "x^2+y^2 секретно"), (key9, "16^2=19, (x+y)^2=x^2 + 2xy + y^2"), (key10, "x^2+y^2 секретно"), (key11, "(x+y)*y=16*y=y^2+xy"), (key12, "(x+y)*x=16*x=x^2+xy"), (key13, "(x - y)"), (key14, "(y - x) ниже диапазона")]
        
        return [
            (key1, "x"),
            (key2, "Первый ключ"),
            (key3, "16 ключ"),
            (key4, "-y"),
            (key5, "y"),
            (key6, "x^2 секретно"),
            (key7, "y^2 секретно"),
            (key8, "x^2+y^2 секретно"),
            (key9, "16^2=19, (x+y)^2=x^2 + 2xy + y^2"),
            (key10, "x^2+y^2 секретно"),
            (key11, "(x+y)*y=16*y=y^2+xy"),
            (key12, "(x+y)*x=16*x=x^2+xy"),
            (key13, "(x - y)"),
            (key14, "(y - x) ниже диапазона"),
            (key15, "x^2-y^2")
        ]
    
    def display_table(self, keys_data):
        """Выводит таблицу ключей"""
        if not keys_data:
            print("❌ Нет данных для отображения")
            return
            
        print("\n" + "="*180)
        print("🎯 РЕЗУЛЬТАТ ПОИСКА ECDSA КЛЮЧЕЙ (15 КЛЮЧЕЙ)")
        print("="*180)
        
        # Заголовки
        print(f"{'k':>6}{'r':>6}{'s':>6}{'z':>6}{'d':>6}{'ks+1':>8}{'ks+z':>8}{'(ks+1)/k':>10}{'(ks+z)/k':>10}{'d-k+1':>8}{'(d-k+1)/k':>10}{'((d-k+1)/k)^77':>15}{'d-k+z':>8}{'(d-k+z)/k':>10}{'((d-k+z)/k)^77':>15}{'Формула':>30}")
        print("-" * 180)
        
        # Данные
        for row_data, formula in keys_data:
            if len(row_data) >= 15:
                print(f"{row_data[0]:>6}{row_data[1]:>6}{row_data[2]:>6}{row_data[3]:>6}{row_data[4]:>6}{row_data[5]:>8}{row_data[6]:>8}{row_data[7]:>10}{row_data[8]:>10}{row_data[9]:>8}{row_data[10]:>10}{row_data[11]:>15}{row_data[12]:>8}{row_data[13]:>10}{row_data[14]:>15}{formula:>30}")
        
        print("="*180)
        
        # Детали расчетов
        print("\n📊 ДЕТАЛИ РАСЧЕТОВ:")
        for i, (row_data, formula) in enumerate(keys_data, 1):
            k, r, s, z, d = row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]
            print(f"🔑 Ключ {i} ({formula}): k={k}, r={r}, s={s}, z={z}, d={d}")
            
            if i == 2:  # Ключ 2
                print(f"   └── Запомнили z={z} для следующих расчетов")
            elif i == 3:  # Ключ 3
                prev_z = keys_data[1][0][3]  # z из ключа 2
                print(f"   └── z = {prev_z} * 16 = {(prev_z * 16) % 79} (mod 79)")
            elif i == 4:  # Ключ 4
                key1_s, key1_z = keys_data[0][0][2], keys_data[0][0][3]
                key3_s, key3_z = keys_data[2][0][2], keys_data[2][0][3]
                print(f"   └── s = {key1_s} - {key3_s} = {(key1_s - key3_s) % 79} (mod 79)")
                print(f"   └── z = {key1_z} - {key3_z} = {(key1_z - key3_z) % 79} (mod 79)")
            elif i == 5:  # Ключ 5
                key4_s, key4_z = keys_data[3][0][2], keys_data[3][0][3]
                print(f"   └── s = -{key4_s} = {(-key4_s) % 79} (mod 79)")
                print(f"   └── z = -{key4_z} = {(-key4_z) % 79} (mod 79)")
            elif i == 6:  # Ключ 6
                key1_s, key1_z, key1_d = keys_data[0][0][2], keys_data[0][0][3], keys_data[0][0][4]
                print(f"   └── s = {key1_s} * {key1_d} = {(key1_s * key1_d) % 79} (mod 79)")
                print(f"   └── z = {key1_z} * {key1_d} = {(key1_z * key1_d) % 79} (mod 79)")
            elif i == 7:  # Ключ 7
                key5_s, key5_z, key5_d = keys_data[4][0][2], keys_data[4][0][3], keys_data[4][0][4]
                print(f"   └── s = {key5_s} * {key5_d} = {(key5_s * key5_d) % 79} (mod 79)")
                print(f"   └── z = {key5_z} * {key5_d} = {(key5_z * key5_d) % 79} (mod 79)")
            elif i == 8:  # Ключ 8
                key6_s, key6_z = keys_data[5][0][2], keys_data[5][0][3]
                key7_s, key7_z = keys_data[6][0][2], keys_data[6][0][3]
                print(f"   └── s = {key6_s} + {key7_s} = {(key6_s + key7_s) % 79} (mod 79)")
                print(f"   └── z = {key6_z} + {key7_z} = {(key6_z + key7_z) % 79} (mod 79)")
            elif i == 9:  # Ключ 9
                key3_s, key3_z = keys_data[2][0][2], keys_data[2][0][3]
                print(f"   └── s = {key3_s} * 16 = {(key3_s * 16) % 79} (mod 79)")
                print(f"   └── z = {key3_z} * 16 = {(key3_z * 16) % 79} (mod 79)")
            elif i == 10:  # Ключ 10
                key6_s, key6_z = keys_data[5][0][2], keys_data[5][0][3]
                key7_s, key7_z = keys_data[6][0][2], keys_data[6][0][3]
                print(f"   └── s = {key6_s} + {key7_s} = {(key6_s + key7_s) % 79} (mod 79)")
                print(f"   └── z = -{key6_z} + {key7_z} = {(-key6_z + key7_z) % 79} (mod 79)")
            elif i == 11:  # Ключ 11
                key5_s, key5_z = keys_data[4][0][2], keys_data[4][0][3]
                print(f"   └── s = {key5_s} * 16 = {(key5_s * 16) % 79} (mod 79)")
                print(f"   └── z = {key5_z} * 16 = {(key5_z * 16) % 79} (mod 79)")
            elif i == 12:  # Ключ 12
                key1_s, key1_z = keys_data[0][0][2], keys_data[0][0][3]
                print(f"   └── s = {key1_s} * 16 = {(key1_s * 16) % 79} (mod 79)")
                print(f"   └── z = {key1_z} * 16 = {(key1_z * 16) % 79} (mod 79)")
            elif i == 13:  # Ключ 13
                key1_s, key1_z = keys_data[0][0][2], keys_data[0][0][3]
                key5_s, key5_z = keys_data[4][0][2], keys_data[4][0][3]
                print(f"   └── s = {key1_s} - {key5_s} = {(key1_s - key5_s) % 79} (mod 79)")
                print(f"   └── z = {key1_z} - {key5_z} = {(key1_z - key5_z) % 79} (mod 79)")
            elif i == 14:  # Ключ 14
                key1_s, key1_z = keys_data[0][0][2], keys_data[0][0][3]
                key5_s, key5_z = keys_data[4][0][2], keys_data[4][0][3]
                print(f"   └── s = {key5_s} - {key1_s} = {(key5_s - key1_s) % 79} (mod 79)")
                print(f"   └── z = {key5_z} - {key1_z} = {(key5_z - key1_z) % 79} (mod 79)")
            elif i == 15:  # Ключ 15
                key9_s, key9_z = keys_data[8][0][2], keys_data[8][0][3]
                key5_s, key5_z = keys_data[4][0][2], keys_data[4][0][3]
                print(f"   └── s = {key9_s} - (32 * {key5_s}) = {(key9_s - (32 * key5_s)) % 79} (mod 79)")
                print(f"   └── z = {key9_z} - (32 * {key5_z}) = {(key9_z - (32 * key5_z)) % 79} (mod 79)")
    
    def run(self):
        print("🚀 ECDSA Key Finder - Расширенная версия с 15 ключами")
        print("="*60)
        
        # Быстрая загрузка
        try:
            self.load_data_fast()
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return
        
        while True:
            try:
                print("\n" + "-"*60)
                user_input = input("👉 Введите k (или 'quit'): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Выход")
                    break
                
                k_value = int(user_input)
                
                # Поиск всех 15 ключей
                keys_data = self.find_keys_for_k(k_value)
                
                # Вывод результата
                if keys_data:
                    self.display_table(keys_data)
                    print(f"\n✅ Найдено ключей: {len(keys_data)}/15")
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