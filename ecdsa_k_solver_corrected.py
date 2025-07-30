#!/usr/bin/env python3
"""
ECDSA K-Solver - Universal tool for finding k from r (CORRECTED VERSION)
Curve: y² = x³ + 7 mod 67, Base: (2,22), Order: 79
Signature modulus: 79 (for d, s, z)

This is the corrected comprehensive tool combining all research methods.
"""

import time
import math
from typing import List, Dict, Optional, Tuple, Any

class ECDSAKSolverCorrected:
    """Universal ECDSA K-Solver with corrected parameters"""
    
    def __init__(self):
        # Curve parameters (CORRECTED)
        self.curve_p = 67  # Curve field prime
        self.a = 0   # Curve coefficient a
        self.b = 7   # Curve coefficient b  
        self.base_point = (2, 22)  # CORRECTED base point
        self.signature_mod = 79  # Signature modulus for d, s, z
        self.order = 79  # Order of base point (calculated)
        
        # Precomputed lookup table (CORRECTED based on new parameters)
        self.r_k_lookup = {
            2: [1, 78], 4: [39, 40], 5: [14, 65], 6: [26, 53], 7: [24, 55],
            11: [6, 73], 12: [21, 58], 13: [9, 70], 14: [12, 67], 16: [7, 72],
            17: [27, 52], 18: [35, 44], 21: [8, 71], 23: [22, 57], 24: [11, 68],
            25: [4, 75], 26: [16, 63], 27: [38, 41], 30: [37, 42], 34: [33, 46],
            38: [19, 60], 40: [34, 45], 42: [30, 49], 46: [5, 74], 47: [25, 54],
            48: [31, 48], 49: [28, 51], 51: [20, 59], 52: [2, 77], 53: [15, 64],
            54: [17, 62], 55: [13, 66], 56: [10, 69], 58: [23, 56], 61: [36, 43],
            62: [3, 76], 63: [29, 50], 64: [32, 47], 66: [18, 61]
        }
        
        # Complement pairs for pattern recognition (updated)
        self.complement_pairs = {
            2: [(1, 78)], 5: [(14, 65)], 6: [(26, 53)], 7: [(24, 55)],
            48: [(31, 48)], 52: [(2, 77)], 62: [(3, 76)]
        }
    
    def mod_inverse(self, a: int, m: int) -> int:
        """Calculate modular inverse using extended Euclidean algorithm"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
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
                if y1 == 0:
                    return None
                s = (3 * x1 * x1 + self.a) * self.mod_inverse(2 * y1, self.curve_p) % self.curve_p
            else:
                return None
        else:
            s = (y2 - y1) * self.mod_inverse(x2 - x1, self.curve_p) % self.curve_p
        
        x3 = (s * s - x1 - x2) % self.curve_p
        y3 = (s * (x1 - x3) - y1) % self.curve_p
        
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
    
    # ================== SOLVING METHODS ==================
    
    def solve_method_1_lookup(self, r: int) -> List[int]:
        """Method 1: Direct lookup table (fastest, 100% accurate)"""
        return self.r_k_lookup.get(r, [])
    
    def solve_method_2_brute_force(self, r: int) -> List[int]:
        """Method 2: Brute force search (100% accurate, slower)"""
        found_k = []
        for k in range(1, self.signature_mod):
            point = self.point_multiply(k, self.base_point)
            if point and point[0] % self.signature_mod == r:
                found_k.append(k)
        return found_k
    
    def solve_method_3_complement_pairs(self, r: int) -> List[int]:
        """Method 3: Use complement pair patterns (fast heuristic)"""
        if r in self.complement_pairs:
            found_k = []
            for k1, k2 in self.complement_pairs[r]:
                found_k.extend([k1, k2])
            return found_k
        return []
    
    def solve_method_4_mathematical(self, r: int) -> List[int]:
        """Method 4: Mathematical approach using curve properties"""
        # Check if r corresponds to a valid point on curve
        y_squared = (r * r * r + self.b) % self.curve_p
        
        # Find y coordinates if they exist
        y_values = []
        for y in range(self.curve_p):
            if (y * y) % self.curve_p == y_squared:
                y_values.append(y)
        
        if not y_values:
            return []
        
        # For each valid point, try to find k (simple search)
        found_k = []
        for y in y_values:
            target = (r, y)
            for k in range(1, self.signature_mod):
                if self.point_multiply(k, self.base_point) == target:
                    found_k.append(k)
                    break
        
        return found_k
    
    # ================== MAIN SOLVER ==================
    
    def solve_k_from_r(self, r: int, method: str = "auto") -> Dict[str, Any]:
        """
        Main solver function - finds k from r using specified method
        
        Args:
            r: The r value from ECDSA signature
            method: "auto", "lookup", "brute", "complement", "mathematical", "all"
        
        Returns:
            Dictionary with results, timing, and method info
        """
        result = {
            'r': r,
            'methods_used': [],
            'k_values': [],
            'total_time': 0,
            'recommended_k': None,
            'confidence': 0
        }
        
        start_time = time.time()
        
        if method == "auto":
            # Smart automatic method selection
            if r in self.r_k_lookup:
                # Use lookup for known r values
                k_vals = self.solve_method_1_lookup(r)
                result['methods_used'].append('lookup')
                result['k_values'] = k_vals
                result['confidence'] = 100
            elif r in self.complement_pairs:
                # Use complement pairs for pattern-based prediction
                k_vals = self.solve_method_3_complement_pairs(r)
                result['methods_used'].append('complement_pairs')
                result['k_values'] = k_vals
                result['confidence'] = 80
            else:
                # Fall back to brute force for unknown r
                k_vals = self.solve_method_2_brute_force(r)
                result['methods_used'].append('brute_force')
                result['k_values'] = k_vals
                result['confidence'] = 100
                
        elif method == "lookup":
            result['k_values'] = self.solve_method_1_lookup(r)
            result['methods_used'].append('lookup')
            result['confidence'] = 100
            
        elif method == "brute":
            result['k_values'] = self.solve_method_2_brute_force(r)
            result['methods_used'].append('brute_force')
            result['confidence'] = 100
            
        elif method == "complement":
            result['k_values'] = self.solve_method_3_complement_pairs(r)
            result['methods_used'].append('complement_pairs')
            result['confidence'] = 80
            
        elif method == "mathematical":
            result['k_values'] = self.solve_method_4_mathematical(r)
            result['methods_used'].append('mathematical')
            result['confidence'] = 75
            
        elif method == "all":
            # Run all methods and compare
            methods = [
                ('lookup', self.solve_method_1_lookup),
                ('brute_force', self.solve_method_2_brute_force),
                ('complement', self.solve_method_3_complement_pairs),
                ('mathematical', self.solve_method_4_mathematical)
            ]
            
            all_results = {}
            for name, method_func in methods:
                method_start = time.time()
                k_vals = method_func(r)
                method_time = time.time() - method_start
                all_results[name] = {'k_values': k_vals, 'time': method_time}
                result['methods_used'].append(name)
            
            # Use lookup result as primary if available
            if all_results['lookup']['k_values']:
                result['k_values'] = all_results['lookup']['k_values']
                result['confidence'] = 100
            else:
                # Find consensus among methods
                all_k = []
                for method_result in all_results.values():
                    all_k.extend(method_result['k_values'])
                result['k_values'] = list(set(all_k))
                result['confidence'] = 85
            
            result['detailed_results'] = all_results
        
        result['total_time'] = time.time() - start_time
        
        # Set recommended k (smallest value if multiple found)
        if result['k_values']:
            result['recommended_k'] = min(result['k_values'])
        
        return result
    
    def verify_solution(self, k: int, r: int) -> bool:
        """Verify that k actually produces the given r value"""
        point = self.point_multiply(k, self.base_point)
        if point:
            return point[0] % self.signature_mod == r
        return False
    
    def batch_solve(self, r_list: List[int], method: str = "auto") -> Dict[int, Dict]:
        """Solve multiple r values efficiently"""
        results = {}
        for r in r_list:
            results[r] = self.solve_k_from_r(r, method)
        return results
    
    def print_solution_report(self, r: int, solution: Dict):
        """Print formatted solution report"""
        print(f"\n{'='*50}")
        print(f"ECDSA K-Solver Report for r = {r}")
        print(f"{'='*50}")
        
        if solution['k_values']:
            print(f"✓ Solution found!")
            print(f"  K values: {solution['k_values']}")
            print(f"  Recommended k: {solution['recommended_k']}")
            print(f"  Confidence: {solution['confidence']}%")
            print(f"  Methods used: {', '.join(solution['methods_used'])}")
            print(f"  Solve time: {solution['total_time']:.6f}s")
            
            # Verify solution
            if solution['recommended_k']:
                is_valid = self.verify_solution(solution['recommended_k'], r)
                print(f"  Verification: {'✓ PASSED' if is_valid else '✗ FAILED'}")
        else:
            print(f"✗ No solution found for r = {r}")
        
        if 'detailed_results' in solution:
            print(f"\n  Detailed method comparison:")
            for method, details in solution['detailed_results'].items():
                k_vals = details['k_values']
                time_taken = details['time']
                print(f"    {method:12s}: k={k_vals} ({time_taken:.6f}s)")
    
    def analyze_patterns(self):
        """Analyze patterns in the corrected r-k mapping"""
        print("Pattern Analysis for Corrected Parameters:")
        print("=" * 50)
        print(f"Curve: y² = x³ + 7 mod {self.curve_p}")
        print(f"Base point: {self.base_point}")
        print(f"Signature modulus: {self.signature_mod}")
        print(f"Total r values with solutions: {len(self.r_k_lookup)}")
        print()
        
        # Complement pair analysis
        print("Complement Pairs (k + k' = 79):")
        complement_count = 0
        for r, k_list in self.r_k_lookup.items():
            pairs = []
            for i in range(len(k_list)):
                for j in range(i+1, len(k_list)):
                    if k_list[i] + k_list[j] == self.signature_mod:
                        pairs.append((k_list[i], k_list[j]))
                        complement_count += 1
            if pairs:
                print(f"  r={r:2d}: {pairs}")
        
        print(f"\nTotal complement pairs found: {complement_count}")
        
        # Distribution analysis
        k_counts = {}
        for k_list in self.r_k_lookup.values():
            count = len(k_list)
            k_counts[count] = k_counts.get(count, 0) + 1
        
        print(f"\nSolution distribution:")
        for count, freq in sorted(k_counts.items()):
            print(f"  {count} solutions per r: {freq} cases ({freq/len(self.r_k_lookup)*100:.1f}%)")

def main():
    """Interactive ECDSA K-Solver demonstration with corrected parameters"""
    print("ECDSA K-Solver - Universal Tool (CORRECTED)")
    print("Curve: y² = x³ + 7 mod 67")
    print("Base point: (2, 22), Order: 79") 
    print("Signature modulus: 79")
    print("="*50)
    
    solver = ECDSAKSolverCorrected()
    
    # Pattern analysis
    solver.analyze_patterns()
    
    print("\n" + "="*50)
    print("DEMONSTRATION - Finding k for various r values:")
    print("-" * 50)
    
    # Demo with various r values
    demo_r_values = [2, 7, 14, 25, 42, 55, 99]  # Include invalid r for testing
    
    for r in demo_r_values:
        solution = solver.solve_k_from_r(r, method="auto")
        
        if solution['k_values']:
            k_str = str(solution['k_values'])
            print(f"r={r:2d} → k={k_str:15s} (confidence: {solution['confidence']}%)")
        else:
            print(f"r={r:2d} → No solution found")
    
    # Detailed analysis for a specific case
    print(f"\n{'='*60}")
    print("DETAILED ANALYSIS for r = 7")
    print(f"{'='*60}")
    
    detailed_solution = solver.solve_k_from_r(7, method="all")
    solver.print_solution_report(7, detailed_solution)

if __name__ == "__main__":
    main()