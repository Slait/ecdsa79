#!/usr/bin/env python3
"""
AI Pattern Finder for ECDSA Analysis
Uses machine learning approaches to find hidden patterns in r, s, z, k relationships
"""

import math
import random
from typing import List, Dict, Tuple, Any
from collections import defaultdict, Counter
from ecdsa_analysis import EllipticCurve, ECDSAAnalyzer

class AIPatternFinder:
    """AI-based pattern recognition for ECDSA analysis"""
    
    def __init__(self, curve: EllipticCurve):
        self.curve = curve
        self.data_samples = []
        self.r_k_map = {}
        self.patterns = {}
        
    def generate_training_data(self, num_samples: int = 100) -> List[Dict]:
        """Generate training data with known r, s, z, k relationships"""
        training_data = []
        
        print(f"Generating {num_samples} training samples...")
        
        for i in range(num_samples):
            # Generate random private key d and nonce k
            d = random.randint(1, self.curve.order - 1)
            k = random.randint(1, self.curve.order - 1)
            
            # Calculate public key
            public_key = self.curve.point_multiply(d, self.curve.base_point)
            
            # Generate random message hash z
            z = random.randint(1, self.curve.order - 1)
            
            # Calculate ECDSA signature (r, s)
            # r = (kQ).x mod n
            k_point = self.curve.point_multiply(k, self.curve.base_point)
            if k_point is None:
                continue
                
            r = k_point[0] % self.curve.order
            if r == 0:
                continue
                
            # s = k^(-1)(z + rd) mod n
            try:
                k_inv = self.curve._mod_inverse(k, self.curve.order)
                s = (k_inv * (z + r * d)) % self.curve.order
                if s == 0:
                    continue
            except:
                continue
            
            sample = {
                'r': r,
                's': s,
                'z': z,
                'k': k,
                'd': d,
                'public_key': public_key
            }
            training_data.append(sample)
            
        self.data_samples = training_data
        print(f"Generated {len(training_data)} valid samples")
        return training_data
    
    def analyze_modular_patterns(self) -> Dict:
        """Analyze modular arithmetic patterns"""
        patterns = {
            'k_mod_patterns': {},
            'r_mod_patterns': {},
            'gcd_patterns': {},
            'quadratic_patterns': {}
        }
        
        print("Analyzing modular patterns...")
        
        for sample in self.data_samples:
            r, s, z, k = sample['r'], sample['s'], sample['z'], sample['k']
            
            # Analyze k modulo small primes
            for prime in [2, 3, 5, 7, 11, 13]:
                k_mod = k % prime
                r_mod = r % prime
                
                key = f"k_mod_{prime}"
                if key not in patterns['k_mod_patterns']:
                    patterns['k_mod_patterns'][key] = defaultdict(list)
                patterns['k_mod_patterns'][key][k_mod].append(r)
                
                key = f"r_mod_{prime}"
                if key not in patterns['r_mod_patterns']:
                    patterns['r_mod_patterns'][key] = defaultdict(list)
                patterns['r_mod_patterns'][key][r_mod].append(k)
            
            # GCD patterns
            gcd_rk = math.gcd(r, k)
            gcd_sz = math.gcd(s, z)
            patterns['gcd_patterns'].setdefault('gcd_r_k', []).append(gcd_rk)
            patterns['gcd_patterns'].setdefault('gcd_s_z', []).append(gcd_sz)
            
            # Quadratic patterns
            k_squared = (k * k) % self.curve.order
            r_squared = (r * r) % self.curve.order
            patterns['quadratic_patterns'].setdefault('k_squared', []).append(k_squared)
            patterns['quadratic_patterns'].setdefault('r_squared', []).append(r_squared)
        
        return patterns
    
    def analyze_linear_relationships(self) -> Dict:
        """Look for linear relationships between variables"""
        print("Analyzing linear relationships...")
        
        relationships = {
            'r_k_linear': [],
            'r_s_linear': [],
            'coefficient_analysis': {}
        }
        
        for sample in self.data_samples:
            r, s, z, k = sample['r'], sample['s'], sample['z'], sample['k']
            
            # Try to find linear combinations
            # Check if r ≡ ak + b (mod order) for small a, b
            for a in range(1, 10):
                for b in range(0, 10):
                    if r == (a * k + b) % self.curve.order:
                        relationships['r_k_linear'].append((a, b, r, k))
            
            # Check relationships between r and s
            for a in range(1, 10):
                for b in range(0, 10):
                    if r == (a * s + b) % self.curve.order:
                        relationships['r_s_linear'].append((a, b, r, s))
        
        return relationships
    
    def analyze_polynomial_patterns(self) -> Dict:
        """Analyze polynomial relationships"""
        print("Analyzing polynomial patterns...")
        
        poly_patterns = {
            'quadratic_r_k': [],
            'cubic_patterns': [],
            'fibonacci_like': []
        }
        
        for sample in self.data_samples:
            r, s, z, k = sample['r'], sample['s'], sample['z'], sample['k']
            
            # Quadratic: r ≡ ak² + bk + c (mod order)
            for a in range(1, 5):
                for b in range(0, 5):
                    for c in range(0, 5):
                        if r == (a * k * k + b * k + c) % self.curve.order:
                            poly_patterns['quadratic_r_k'].append((a, b, c, r, k))
            
            # Check for Fibonacci-like sequences
            # This would require more samples in sequence
        
        return poly_patterns
    
    def find_r_to_k_formulas(self) -> List[Dict]:
        """Find mathematical formulas to compute k from r"""
        print("Searching for r->k formulas...")
        
        # Build r->k mapping from our data
        r_to_k_map = defaultdict(list)
        for sample in self.data_samples:
            r_to_k_map[sample['r']].append(sample['k'])
        
        formulas = []
        
        # Method 1: Direct lookup table (most reliable)
        formula1 = {
            'name': 'Direct Lookup',
            'description': 'Use precomputed r->k mapping',
            'reliability': 1.0,
            'complexity': 'O(1)',
            'implementation': 'lookup_table[r]'
        }
        formulas.append(formula1)
        
        # Method 2: Modular inverse patterns
        # Look for patterns like k ≡ r^(-1) * constant (mod order)
        for const in range(1, 20):
            correct_predictions = 0
            total_tests = 0
            
            for r, k_list in r_to_k_map.items():
                try:
                    r_inv = self.curve._mod_inverse(r, self.curve.order)
                    predicted_k = (r_inv * const) % self.curve.order
                    
                    if predicted_k in k_list:
                        correct_predictions += 1
                    total_tests += 1
                except:
                    continue
            
            if total_tests > 0:
                accuracy = correct_predictions / total_tests
                if accuracy > 0.1:  # At least 10% accuracy
                    formula = {
                        'name': f'Modular Inverse Pattern (c={const})',
                        'description': f'k ≡ r^(-1) * {const} (mod {self.curve.order})',
                        'reliability': accuracy,
                        'complexity': 'O(log n)',
                        'implementation': f'mod_inverse(r, {self.curve.order}) * {const} % {self.curve.order}'
                    }
                    formulas.append(formula)
        
        # Method 3: Quadratic residue patterns
        for multiplier in range(1, 10):
            correct_predictions = 0
            total_tests = 0
            
            for r, k_list in r_to_k_map.items():
                # Try k ≡ sqrt(r * multiplier) (mod order)
                target = (r * multiplier) % self.curve.order
                
                # Find square roots
                for potential_k in range(1, self.curve.order):
                    if (potential_k * potential_k) % self.curve.order == target:
                        if potential_k in k_list:
                            correct_predictions += 1
                        break
                total_tests += 1
            
            if total_tests > 0:
                accuracy = correct_predictions / total_tests
                if accuracy > 0.05:
                    formula = {
                        'name': f'Quadratic Residue (m={multiplier})',
                        'description': f'k ≡ sqrt(r * {multiplier}) (mod {self.curve.order})',
                        'reliability': accuracy,
                        'complexity': 'O(sqrt(n))',
                        'implementation': f'sqrt(r * {multiplier}) mod {self.curve.order}'
                    }
                    formulas.append(formula)
        
        return sorted(formulas, key=lambda x: x['reliability'], reverse=True)
    
    def statistical_analysis(self) -> Dict:
        """Perform statistical analysis on the data"""
        print("Performing statistical analysis...")
        
        stats = {
            'r_distribution': Counter(),
            'k_distribution': Counter(),
            's_distribution': Counter(),
            'z_distribution': Counter(),
            'correlations': {}
        }
        
        r_values = [sample['r'] for sample in self.data_samples]
        k_values = [sample['k'] for sample in self.data_samples]
        s_values = [sample['s'] for sample in self.data_samples]
        z_values = [sample['z'] for sample in self.data_samples]
        
        # Distribution analysis
        stats['r_distribution'] = Counter(r_values)
        stats['k_distribution'] = Counter(k_values)
        stats['s_distribution'] = Counter(s_values)
        stats['z_distribution'] = Counter(z_values)
        
        # Simple correlation analysis
        # Calculate correlation between r and k values
        if len(r_values) > 1:
            r_mean = sum(r_values) / len(r_values)
            k_mean = sum(k_values) / len(k_values)
            
            numerator = sum((r - r_mean) * (k - k_mean) for r, k in zip(r_values, k_values))
            r_variance = sum((r - r_mean) ** 2 for r in r_values)
            k_variance = sum((k - k_mean) ** 2 for k in k_values)
            
            if r_variance > 0 and k_variance > 0:
                correlation = numerator / math.sqrt(r_variance * k_variance)
                stats['correlations']['r_k_correlation'] = correlation
        
        return stats
    
    def generate_report(self) -> str:
        """Generate comprehensive analysis report"""
        report = []
        report.append("AI PATTERN ANALYSIS REPORT")
        report.append("=" * 50)
        
        # Generate training data
        self.generate_training_data(200)
        
        # Run all analyses
        modular_patterns = self.analyze_modular_patterns()
        linear_relationships = self.analyze_linear_relationships()
        polynomial_patterns = self.analyze_polynomial_patterns()
        formulas = self.find_r_to_k_formulas()
        stats = self.statistical_analysis()
        
        # Report findings
        report.append(f"\nSample Size: {len(self.data_samples)} ECDSA signatures")
        report.append(f"Curve Order: {self.curve.order}")
        
        report.append("\nFOUND FORMULAS FOR K FROM R:")
        report.append("-" * 30)
        for formula in formulas[:5]:  # Top 5 formulas
            report.append(f"Formula: {formula['name']}")
            report.append(f"  Description: {formula['description']}")
            report.append(f"  Reliability: {formula['reliability']:.2%}")
            report.append(f"  Complexity: {formula['complexity']}")
            report.append("")
        
        report.append("\nLINEAR RELATIONSHIPS:")
        report.append("-" * 20)
        if linear_relationships['r_k_linear']:
            report.append("Found r-k linear relationships:")
            for rel in linear_relationships['r_k_linear'][:5]:
                a, b, r, k = rel
                report.append(f"  r ≡ {a}k + {b} (mod {self.curve.order}) for r={r}, k={k}")
        else:
            report.append("No simple linear relationships found")
        
        report.append("\nSTATISTICAL SUMMARY:")
        report.append("-" * 18)
        if 'r_k_correlation' in stats['correlations']:
            corr = stats['correlations']['r_k_correlation']
            report.append(f"R-K Correlation: {corr:.4f}")
        
        report.append(f"Most common r values: {stats['r_distribution'].most_common(3)}")
        report.append(f"Most common k values: {stats['k_distribution'].most_common(3)}")
        
        return "\n".join(report)

def main():
    """Main AI analysis"""
    curve = EllipticCurve()
    ai_finder = AIPatternFinder(curve)
    
    # Generate and print report
    report = ai_finder.generate_report()
    print(report)
    
    # Also save to file
    with open('ai_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\nReport saved to 'ai_analysis_report.txt'")

if __name__ == "__main__":
    main()