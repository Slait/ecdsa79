#!/usr/bin/env python3
"""
ECDSA Analysis for Project - Corrected Parameters
Curve: y² = x³ + 7 mod 67
Base Point: (2, 22)
Signature Modulus: 79
"""

class EllipticCurve:
    """Elliptic curve y² = x³ + 7 mod 67"""
    
    def __init__(self):
        self.p = 67  # Curve modulus
        self.a = 0   # Coefficient a
        self.b = 7   # Coefficient b
        self.base_point = (2, 22)  # Base point Q
        self.signature_mod = 79    # Modulus for signatures
        self.order = 79           # Order of base point
    
    def _mod_inverse(self, a, m=None):
        """Calculate modular inverse"""
        if m is None:
            m = self.signature_mod
            
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError(f"No modular inverse for {a} mod {m}")
        return (x % m + m) % m
    
    def point_add(self, P, Q):
        """Add two points on the elliptic curve"""
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2:
            if y1 == y2:
                # Point doubling
                s = (3 * x1 * x1 + self.a) * self._mod_inverse(2 * y1, self.p) % self.p
            else:
                # Points are additive inverses
                return None
        else:
            # Regular point addition
            s = (y2 - y1) * self._mod_inverse(x2 - x1, self.p) % self.p
        
        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def point_multiply(self, k, point):
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