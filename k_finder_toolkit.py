#!/usr/bin/env python3
"""
K-Finder Toolkit - Practical tool for finding k from r in ECDSA
Curve: y² = x³ + 7 mod 79, Base point: (1, 18), Order: 67
"""

import time
from typing import List, Optional, Dict, Tuple
from ecdsa_analysis import EllipticCurve

class KFinderToolkit:
    """Practical toolkit for finding k from r values"""
    
    def __init__(self):
        self.curve = EllipticCurve()
        self.r_k_lookup = self._build_lookup_table()
        
    def _build_lookup_table(self) -> Dict[int, List[int]]:
        """Build optimized r->k lookup table"""
        print("Building r->k lookup table...")
        lookup = {}
        
        for k in range(1, self.curve.order):
            point = self.curve.point_multiply(k, self.curve.base_point)
            if point:
                r = point[0] % self.curve.order
                if r not in lookup:
                    lookup[r] = []
                lookup[r].append(k)
        
        print(f"Lookup table built: {len(lookup)} unique r values")
        return lookup
    
    def find_k_from_r(self, r: int, method: str = "all") -> Dict[str, List[int]]:
        """
        Find all possible k values for given r
        
        Args:
            r: The r value from ECDSA signature
            method: "lookup", "brute", "mathematical", or "all"
        
        Returns:
            Dictionary with method names and found k values
        """
        results = {}
        
        if method in ["lookup", "all"]:
            results["lookup"] = self._method_lookup(r)
        
        if method in ["brute", "all"]:
            results["brute_force"] = self._method_brute_force(r)
        
        if method in ["mathematical", "all"]:
            results["mathematical"] = self._method_mathematical(r)
        
        return results
    
    def _method_lookup(self, r: int) -> List[int]:
        """Method 1: Direct lookup (fastest)"""
        return self.r_k_lookup.get(r, [])
    
    def _method_brute_force(self, r: int) -> List[int]:
        """Method 2: Brute force verification"""
        found_k = []
        for k in range(1, self.curve.order):
            point = self.curve.point_multiply(k, self.curve.base_point)
            if point and point[0] % self.curve.order == r:
                found_k.append(k)
        return found_k
    
    def _method_mathematical(self, r: int) -> List[int]:
        """Method 3: Mathematical approach using curve properties"""
        found_k = []
        
        # Check if r is a valid x-coordinate on the curve
        y_squared = (r * r * r + 7) % self.curve.p
        
        # Find corresponding y values if they exist
        y_values = []
        for y in range(self.curve.p):
            if (y * y) % self.curve.p == y_squared:
                y_values.append(y)
        
        # For each valid point (r, y), find discrete log
        for y in y_values:
            target_point = (r, y)
            # Use baby-step giant-step for discrete log
            k = self._discrete_log_bsgs(target_point)
            if k:
                found_k.extend(k)
        
        return list(set(found_k))
    
    def _discrete_log_bsgs(self, target_point: Tuple[int, int]) -> List[int]:
        """Baby-step Giant-step discrete logarithm"""
        n = self.curve.order
        m = int(n**0.5) + 1
        
        # Baby steps: store jQ for j = 0, 1, ..., m-1
        baby_steps = {}
        current = None  # Point at infinity
        
        for j in range(m):
            if current == target_point:
                return [j]
            baby_steps[current] = j
            current = self.curve.point_add(current, self.curve.base_point)
        
        # Giant steps: compute target - i*mQ for i = 0, 1, ..., m-1
        gamma = self.curve.point_multiply(m, self.curve.base_point)
        y = target_point
        
        for i in range(m):
            if y in baby_steps:
                k = i * m + baby_steps[y]
                if 0 < k < n:
                    return [k]
            # y = y - gamma
            if gamma:
                neg_gamma = (gamma[0], (-gamma[1]) % self.curve.p)
                y = self.curve.point_add(y, neg_gamma)
        
        return []
    
    def analyze_r_patterns(self) -> Dict:
        """Analyze patterns in r->k mappings"""
        patterns = {
            'distribution': {},
            'complement_pairs': [],
            'periodic_patterns': [],
            'mathematical_relations': []
        }
        
        # Distribution analysis
        k_counts = {}
        for r, k_list in self.r_k_lookup.items():
            count = len(k_list)
            k_counts[count] = k_counts.get(count, 0) + 1
        patterns['distribution'] = k_counts
        
        # Complement pairs (k, order-k)
        for r, k_list in self.r_k_lookup.items():
            for k in k_list:
                complement = self.curve.order - k
                if complement in k_list and k < complement:
                    patterns['complement_pairs'].append((r, k, complement))
        
        # Look for arithmetic progressions
        for r, k_list in self.r_k_lookup.items():
            if len(k_list) >= 3:
                k_sorted = sorted(k_list)
                for i in range(len(k_sorted) - 2):
                    if (k_sorted[i+1] - k_sorted[i]) == (k_sorted[i+2] - k_sorted[i+1]):
                        diff = k_sorted[i+1] - k_sorted[i]
                        patterns['periodic_patterns'].append((r, k_sorted[i:i+3], diff))
        
        return patterns
    
    def verify_k_r_pair(self, k: int, r: int) -> bool:
        """Verify that k generates the given r value"""
        point = self.curve.point_multiply(k, self.curve.base_point)
        if point:
            return point[0] % self.curve.order == r
        return False
    
    def find_optimal_k(self, r: int, preferences: Dict = None) -> Optional[int]:
        """
        Find the "best" k value for given r based on preferences
        
        Args:
            r: The r value
            preferences: Dict with criteria like 'smallest', 'largest', 'middle'
        """
        if preferences is None:
            preferences = {'criterion': 'smallest'}
        
        k_values = self.r_k_lookup.get(r, [])
        if not k_values:
            return None
        
        criterion = preferences.get('criterion', 'smallest')
        
        if criterion == 'smallest':
            return min(k_values)
        elif criterion == 'largest':
            return max(k_values)
        elif criterion == 'middle':
            sorted_k = sorted(k_values)
            return sorted_k[len(sorted_k) // 2]
        elif criterion == 'random':
            import random
            return random.choice(k_values)
        
        return k_values[0]
    
    def batch_find_k(self, r_list: List[int]) -> Dict[int, List[int]]:
        """Find k values for multiple r values efficiently"""
        results = {}
        for r in r_list:
            results[r] = self.r_k_lookup.get(r, [])
        return results
    
    def print_summary(self):
        """Print summary of the toolkit capabilities"""
        print("K-Finder Toolkit Summary")
        print("=" * 30)
        print(f"Curve: y² = x³ + 7 mod {self.curve.p}")
        print(f"Base point: {self.curve.base_point}")
        print(f"Order: {self.curve.order}")
        print()
        
        # R-K mapping statistics
        total_r_values = len(self.r_k_lookup)
        k_distribution = {}
        for k_list in self.r_k_lookup.values():
            count = len(k_list)
            k_distribution[count] = k_distribution.get(count, 0) + 1
        
        print("R-K Mapping Statistics:")
        print(f"  Total unique r values: {total_r_values}")
        print(f"  K-values per r distribution: {k_distribution}")
        
        # Show some examples
        print("\nExamples:")
        for i, (r, k_list) in enumerate(list(self.r_k_lookup.items())[:5]):
            print(f"  r={r}: k={k_list}")
        
        # Patterns analysis
        patterns = self.analyze_r_patterns()
        print(f"\nFound patterns:")
        print(f"  Complement pairs: {len(patterns['complement_pairs'])}")
        print(f"  Arithmetic progressions: {len(patterns['periodic_patterns'])}")

def main():
    """Demonstration of the K-Finder Toolkit"""
    print("ECDSA K-Finder Toolkit")
    print("=" * 40)
    
    # Initialize toolkit
    toolkit = KFinderToolkit()
    toolkit.print_summary()
    
    print("\n" + "=" * 40)
    print("DEMONSTRATION")
    print("=" * 40)
    
    # Test some r values
    test_r_values = [1, 7, 14, 19, 42, 55]
    
    for r in test_r_values:
        print(f"\nTesting r = {r}:")
        
        # Find k using all methods
        results = toolkit.find_k_from_r(r, method="all")
        
        # Compare results
        lookup_k = results.get("lookup", [])
        brute_k = results.get("brute_force", [])
        math_k = results.get("mathematical", [])
        
        print(f"  Lookup method: {lookup_k}")
        print(f"  Brute force:   {brute_k}")
        print(f"  Mathematical:  {math_k}")
        
        # Verify consistency
        if lookup_k == brute_k:
            print("  ✓ Lookup and brute force match")
        else:
            print("  ✗ Methods disagree!")
        
        # Find optimal k
        optimal = toolkit.find_optimal_k(r, {'criterion': 'smallest'})
        if optimal:
            print(f"  Optimal k (smallest): {optimal}")
            
            # Verify
            if toolkit.verify_k_r_pair(optimal, r):
                print("  ✓ Verification passed")
            else:
                print("  ✗ Verification failed!")
    
    # Batch processing example
    print(f"\nBatch processing {test_r_values}:")
    batch_results = toolkit.batch_find_k(test_r_values)
    for r, k_list in batch_results.items():
        print(f"  r={r}: {k_list}")

if __name__ == "__main__":
    main()