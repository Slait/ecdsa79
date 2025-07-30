#!/usr/bin/env python3
"""
ECDSA Analysis for curve y² = x³ + 7 mod 67
Base point Q = (2, 22)
Signature modulus = 79

This script analyzes ECDSA signatures to find relationships between r, s, z and k values.
"""

import math
import random
from typing import List, Tuple, Optional, Dict
import itertools
from collections import defaultdict

# Curve parameters
P = 67  # Prime modulus
A = 0   # Coefficient a in y² = x³ + ax + b
B = 7   # Coefficient b in y² = x³ + ax + b
BASE_POINT = (2, 22)  # Base point Q

class EllipticCurve:
    """Elliptic curve y² = x³ + 7 mod 67"""
    
    def __init__(self):
        self.p = P
        self.a = A
        self.b = B
        self.base_point = BASE_POINT
        self.order = self._calculate_order()
        
    def _mod_inverse(self, a: int, m: int) -> int:
        """Calculate modular inverse using extended Euclidean algorithm"""
        if math.gcd(a, m) != 1:
            raise ValueError(f"No inverse exists for {a} mod {m}")
        
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
    def is_on_curve(self, point: Tuple[int, int]) -> bool:
        """Check if point is on the curve"""
        if point is None:
            return True  # Point at infinity
        x, y = point
        return (y * y) % self.p == (x * x * x + self.a * x + self.b) % self.p
    
    def point_add(self, p1: Optional[Tuple[int, int]], p2: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """Add two points on the elliptic curve"""
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        
        x1, y1 = p1
        x2, y2 = p2
        
        if x1 == x2:
            if y1 == y2:
                # Point doubling
                if y1 == 0:
                    return None
                s = (3 * x1 * x1 + self.a) * self._mod_inverse(2 * y1, self.p) % self.p
            else:
                return None  # Points are inverses
        else:
            # Point addition
            s = (y2 - y1) * self._mod_inverse(x2 - x1, self.p) % self.p
        
        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def point_multiply(self, k: int, point: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Multiply point by scalar k"""
        if k == 0:
            return None
        if k == 1:
            return point
        
        result = None
        addend = point
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1
        
        return result
    
    def _calculate_order(self) -> int:
        """Calculate the order of the base point"""
        point = self.base_point
        order = 1
        current = point
        
        while True:
            current = self.point_add(current, point)
            order += 1
            if current is None:
                break
                
        return order
    
    def generate_all_points(self) -> List[Tuple[int, int]]:
        """Generate all points on the curve"""
        points = []
        for x in range(self.p):
            y_squared = (x * x * x + self.a * x + self.b) % self.p
            for y in range(self.p):
                if (y * y) % self.p == y_squared:
                    points.append((x, y))
        return points

class ECDSAAnalyzer:
    """ECDSA signature analyzer"""
    
    def __init__(self, curve: EllipticCurve):
        self.curve = curve
        self.signatures = []
        
    def add_signature(self, r: int, s: int, z: int):
        """Add a signature to analyze"""
        self.signatures.append({'r': r, 's': s, 'z': z})
    
    def verify_signature(self, r: int, s: int, z: int, public_key: Tuple[int, int]) -> bool:
        """Verify ECDSA signature"""
        signature_mod = 79  # Signature modulus
        if r <= 0 or r >= signature_mod:
            return False
        if s <= 0 or s >= signature_mod:
            return False
        
        w = self.curve._mod_inverse(s, signature_mod)
        u1 = (z * w) % signature_mod
        u2 = (r * w) % signature_mod
        
        point1 = self.curve.point_multiply(u1, self.curve.base_point)
        point2 = self.curve.point_multiply(u2, public_key)
        point = self.curve.point_add(point1, point2)
        
        if point is None:
            return False
        
        return point[0] % self.curve.order == r
    
    def brute_force_k_search(self, r: int, s: int, z: int) -> List[int]:
        """Brute force search for k values that could produce given r"""
        possible_k = []
        signature_mod = 79  # Signature modulus
        
        for k in range(1, signature_mod):
            point = self.curve.point_multiply(k, self.curve.base_point)
            if point and point[0] % signature_mod == r:
                possible_k.append(k)
                
        return possible_k
    
    def analyze_r_k_relationship(self) -> Dict:
        """Analyze relationship between r and k values"""
        r_to_k = defaultdict(list)
        signature_mod = 79  # Signature modulus
        
        print("Analyzing r-k relationships...")
        for k in range(1, signature_mod):
            point = self.curve.point_multiply(k, self.curve.base_point)
            if point:
                r = point[0] % signature_mod
                r_to_k[r].append(k)
        
        return dict(r_to_k)
    
    def find_k_from_r(self, r: int) -> List[int]:
        """Find all possible k values for given r"""
        possible_k = []
        signature_mod = 79  # Signature modulus
        
        for k in range(1, signature_mod):
            point = self.curve.point_multiply(k, self.curve.base_point)
            if point and point[0] % signature_mod == r:
                possible_k.append(k)
                
        return possible_k

def main():
    """Main analysis function"""
    print("ECDSA Analysis for curve y² = x³ + 7 mod 67")
    print("=" * 50)
    
    # Initialize curve
    curve = EllipticCurve()
    analyzer = ECDSAAnalyzer(curve)
    
    print(f"Curve: y² = x³ + {curve.b} mod {curve.p}")
    print(f"Base point: {curve.base_point}")
    print(f"Order of base point: {curve.order}")
    print()
    
    # Verify base point is on curve
    if curve.is_on_curve(curve.base_point):
        print("✓ Base point is on the curve")
    else:
        print("✗ Base point is NOT on the curve")
    
    # Analyze r-k relationships
    r_k_map = analyzer.analyze_r_k_relationship()
    
    print("\nR-K relationship mapping:")
    print("-" * 30)
    for r, k_values in sorted(r_k_map.items()):
        print(f"r = {r:2d}: k = {k_values}")
    
    return curve, analyzer, r_k_map

if __name__ == "__main__":
    curve, analyzer, r_k_map = main()