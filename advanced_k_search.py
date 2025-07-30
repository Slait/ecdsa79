#!/usr/bin/env python3
"""
Advanced K-Search Methods for ECDSA Analysis
Implements multiple approaches to find k from r values.
"""

import math
import time
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
# import numpy as np  # Not needed for this analysis
from ecdsa_analysis import EllipticCurve, ECDSAAnalyzer

class AdvancedKSearcher:
    """Advanced methods for finding k from r values"""
    
    def __init__(self, curve: EllipticCurve):
        self.curve = curve
        self.precomputed_r_k_map = None
        self.baby_steps = {}
        
    def precompute_r_k_mapping(self) -> Dict[int, List[int]]:
        """Precompute complete r->k mapping"""
        if self.precomputed_r_k_map is not None:
            return self.precomputed_r_k_map
            
        print("Precomputing r-k mapping...")
        r_to_k = defaultdict(list)
        
        for k in range(1, self.curve.order):
            point = self.curve.point_multiply(k, self.curve.base_point)
            if point:
                r = point[0] % self.curve.order
                r_to_k[r].append(k)
        
        self.precomputed_r_k_map = dict(r_to_k)
        return self.precomputed_r_k_map
    
    def method_1_direct_lookup(self, r: int) -> List[int]:
        """Method 1: Direct lookup using precomputed mapping"""
        if not self.precomputed_r_k_map:
            self.precompute_r_k_mapping()
        return self.precomputed_r_k_map.get(r, [])
    
    def method_2_brute_force_optimized(self, r: int) -> List[int]:
        """Method 2: Optimized brute force with early termination"""
        found_k = []
        max_k_per_r = 4  # Based on observation that max is 4 for our curve
        
        for k in range(1, self.curve.order):
            if len(found_k) >= max_k_per_r:
                break
                
            point = self.curve.point_multiply(k, self.curve.base_point)
            if point and point[0] % self.curve.order == r:
                found_k.append(k)
                
        return found_k
    
    def method_3_baby_step_giant_step(self, r: int) -> List[int]:
        """Method 3: Baby-step Giant-step algorithm"""
        n = self.curve.order
        m = int(math.sqrt(n)) + 1
        
        # Baby steps: compute iQ for i = 0, 1, ..., m-1
        if not self.baby_steps:
            print("Computing baby steps...")
            for i in range(m):
                point = self.curve.point_multiply(i, self.curve.base_point)
                if point:
                    self.baby_steps[point[0]] = i
        
        # Giant steps: look for r - jmQ for j = 0, 1, ..., m-1
        found_k = []
        giant_step = self.curve.point_multiply(m, self.curve.base_point)
        
        current_point = None  # Start with point at infinity
        for j in range(m):
            # Calculate target x-coordinate
            # We need to find point P such that P.x = r
            # Check if we have this in baby steps
            if r in self.baby_steps:
                k_candidate = self.baby_steps[r] + j * m
                if 0 < k_candidate < n:
                    # Verify
                    verify_point = self.curve.point_multiply(k_candidate, self.curve.base_point)
                    if verify_point and verify_point[0] % n == r:
                        found_k.append(k_candidate)
            
            # Update current point for next iteration
            current_point = self.curve.point_add(current_point, giant_step)
            
        return found_k
    
    def method_4_quadratic_residue_analysis(self, r: int) -> List[int]:
        """Method 4: Analyze quadratic residues pattern"""
        # For curve y² = x³ + 7, analyze when x³ + 7 is a quadratic residue
        found_k = []
        
        # First check if r is a valid x-coordinate on the curve
        y_squared = (r * r * r + 7) % self.curve.p
        
        # Check if y_squared is a quadratic residue mod p
        if self._is_quadratic_residue(y_squared, self.curve.p):
            # Find y values
            y_values = []
            for y in range(self.curve.p):
                if (y * y) % self.curve.p == y_squared:
                    y_values.append(y)
            
            # For each valid point (r, y), find k such that kQ = (r, y)
            for y in y_values:
                k = self._find_discrete_log(r, y)
                if k:
                    found_k.extend(k)
        
        return found_k
    
    def method_5_pattern_analysis(self, r: int) -> List[int]:
        """Method 5: Analyze patterns in k values"""
        if not self.precomputed_r_k_map:
            self.precompute_r_k_mapping()
        
        # Analyze patterns in the mapping
        patterns = self._analyze_k_patterns()
        
        # Try to predict k values based on patterns
        predicted_k = []
        
        # Pattern 1: k and order-k often appear together
        if r in self.precomputed_r_k_map:
            for k in self.precomputed_r_k_map[r]:
                complement = self.curve.order - k
                if complement in self.precomputed_r_k_map.get(r, []):
                    predicted_k.extend([k, complement])
        
        return list(set(predicted_k))
    
    def _is_quadratic_residue(self, a: int, p: int) -> bool:
        """Check if a is a quadratic residue modulo p using Legendre symbol"""
        if a == 0:
            return True
        return pow(a, (p - 1) // 2, p) == 1
    
    def _find_discrete_log(self, x: int, y: int) -> List[int]:
        """Find k such that kQ = (x, y)"""
        target_point = (x, y)
        found_k = []
        
        # Simple search (can be optimized)
        for k in range(1, self.curve.order):
            point = self.curve.point_multiply(k, self.curve.base_point)
            if point == target_point:
                found_k.append(k)
                
        return found_k
    
    def _analyze_k_patterns(self) -> Dict:
        """Analyze patterns in k values distribution"""
        if not self.precomputed_r_k_map:
            return {}
        
        patterns = {
            'k_counts': defaultdict(int),
            'complement_pairs': [],
            'arithmetic_sequences': [],
        }
        
        for r, k_list in self.precomputed_r_k_map.items():
            patterns['k_counts'][len(k_list)] += 1
            
            # Check for complement pairs (k, order-k)
            for k in k_list:
                complement = self.curve.order - k
                if complement in k_list and k < complement:
                    patterns['complement_pairs'].append((k, complement))
        
        return patterns
    
    def benchmark_methods(self, test_r_values: List[int]) -> Dict:
        """Benchmark all methods on given r values"""
        results = {
            'method_1_direct': [],
            'method_2_brute_force': [],
            'method_3_baby_giant': [],
            'method_4_quadratic': [],
            'method_5_pattern': [],
        }
        
        for r in test_r_values:
            print(f"\nTesting r = {r}")
            
            # Method 1
            start_time = time.time()
            k1 = self.method_1_direct_lookup(r)
            time1 = time.time() - start_time
            results['method_1_direct'].append((r, k1, time1))
            print(f"  Method 1 (Direct): k = {k1}, time = {time1:.6f}s")
            
            # Method 2
            start_time = time.time()
            k2 = self.method_2_brute_force_optimized(r)
            time2 = time.time() - start_time
            results['method_2_brute_force'].append((r, k2, time2))
            print(f"  Method 2 (Brute): k = {k2}, time = {time2:.6f}s")
            
            # Method 3
            start_time = time.time()
            k3 = self.method_3_baby_step_giant_step(r)
            time3 = time.time() - start_time
            results['method_3_baby_giant'].append((r, k3, time3))
            print(f"  Method 3 (Baby-Giant): k = {k3}, time = {time3:.6f}s")
            
            # Method 4
            start_time = time.time()
            k4 = self.method_4_quadratic_residue_analysis(r)
            time4 = time.time() - start_time
            results['method_4_quadratic'].append((r, k4, time4))
            print(f"  Method 4 (Quadratic): k = {k4}, time = {time4:.6f}s")
            
            # Method 5
            start_time = time.time()
            k5 = self.method_5_pattern_analysis(r)
            time5 = time.time() - start_time
            results['method_5_pattern'].append((r, k5, time5))
            print(f"  Method 5 (Pattern): k = {k5}, time = {time5:.6f}s")
        
        return results

def main():
    """Main testing function"""
    print("Advanced K-Search Methods Analysis")
    print("=" * 40)
    
    # Initialize
    curve = EllipticCurve()
    searcher = AdvancedKSearcher(curve)
    
    print(f"Curve order: {curve.order}")
    print(f"Base point: {curve.base_point}")
    
    # Test with some r values
    test_r_values = [2, 5, 7, 14, 16, 19]
    
    # Benchmark methods
    results = searcher.benchmark_methods(test_r_values)
    
    # Analyze results
    print("\n" + "=" * 40)
    print("BENCHMARK SUMMARY")
    print("=" * 40)
    
    for method, data in results.items():
        total_time = sum(item[2] for item in data)
        avg_time = total_time / len(data) if data else 0
        print(f"{method}: avg time = {avg_time:.6f}s, total = {total_time:.6f}s")

if __name__ == "__main__":
    main()