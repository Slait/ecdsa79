#!/usr/bin/env python3
"""
ECDSA K-Finding: Practical Usage Examples
Complete guide for using all developed tools to find k from r
"""

from ecdsa_k_solver import ECDSAKSolver

def example_1_basic_usage():
    """Example 1: Basic usage - find k for a single r value"""
    print("EXAMPLE 1: Basic Usage")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    
    # Find k for r = 19
    r = 19
    result = solver.solve_k_from_r(r)
    
    print(f"Input: r = {r}")
    print(f"Found k values: {result['k_values']}")
    print(f"Recommended k: {result['recommended_k']}")
    print(f"Method used: {result['methods_used'][0]}")
    print()

def example_2_method_comparison():
    """Example 2: Compare different methods for the same r"""
    print("EXAMPLE 2: Method Comparison")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    r = 42
    
    methods = ["lookup", "brute", "mathematical"]
    
    print(f"Finding k for r = {r} using different methods:")
    for method in methods:
        result = solver.solve_k_from_r(r, method=method)
        print(f"{method:12s}: k={result['k_values']} (time: {result['total_time']:.6f}s)")
    print()

def example_3_batch_processing():
    """Example 3: Process multiple r values at once"""
    print("EXAMPLE 3: Batch Processing")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    
    # Multiple r values to process
    r_values = [1, 7, 14, 19, 42, 55]
    
    print("Processing multiple r values:")
    batch_results = solver.batch_solve(r_values)
    
    for r, result in batch_results.items():
        k_vals = result['k_values']
        confidence = result['confidence']
        print(f"r={r:2d} → k={k_vals} (confidence: {confidence}%)")
    print()

def example_4_verification():
    """Example 4: Verify that found k values are correct"""
    print("EXAMPLE 4: Solution Verification")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    
    test_cases = [
        (1, 19),   # r=1, expected k=19
        (7, 28),   # r=7, expected k=28  
        (42, 5),   # r=42, expected k=5
    ]
    
    print("Verifying k values produce correct r:")
    for r, k in test_cases:
        is_valid = solver.verify_solution(k, r)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"k={k:2d} → r={r:2d}: {status}")
    print()

def example_5_pattern_recognition():
    """Example 5: Use pattern recognition for prediction"""
    print("EXAMPLE 5: Pattern Recognition")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    
    # Show complement pairs pattern
    print("Complement pair patterns (k, 67-k):")
    complement_r_values = [1, 15, 42, 49, 60, 61, 63]
    
    for r in complement_r_values:
        k_values = solver.solve_k_from_r(r)['k_values']
        if len(k_values) >= 2:
            pairs = []
            for i in range(0, len(k_values), 2):
                if i+1 < len(k_values):
                    k1, k2 = k_values[i], k_values[i+1]
                    if k1 + k2 == 67:
                        pairs.append(f"({k1},{k2})")
            if pairs:
                print(f"r={r:2d}: complement pairs {', '.join(pairs)}")
    print()

def example_6_performance_analysis():
    """Example 6: Analyze performance of different methods"""
    print("EXAMPLE 6: Performance Analysis")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    
    # Test with several r values
    test_r_values = [1, 7, 14, 19, 42, 55, 66]
    methods = ["lookup", "brute", "mathematical"]
    
    print(f"{'Method':<12} {'Min Time':<10} {'Max Time':<10} {'Avg Time':<10} {'Success Rate'}")
    print("-" * 60)
    
    for method in methods:
        times = []
        successes = 0
        
        for r in test_r_values:
            result = solver.solve_k_from_r(r, method=method)
            times.append(result['total_time'])
            if result['k_values']:
                successes += 1
        
        min_time = min(times)
        max_time = max(times)
        avg_time = sum(times) / len(times)
        success_rate = successes / len(test_r_values) * 100
        
        print(f"{method:<12} {min_time:<10.6f} {max_time:<10.6f} {avg_time:<10.6f} {success_rate:.1f}%")
    print()

def example_7_complete_r_k_mapping():
    """Example 7: Show complete r->k mapping for the curve"""
    print("EXAMPLE 7: Complete R-K Mapping")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    
    print("Complete r → k mapping for curve y² = x³ + 7 mod 79:")
    print("(Only showing r values that have solutions)")
    print()
    
    all_r_values = sorted(solver.r_k_lookup.keys())
    
    for i, r in enumerate(all_r_values):
        k_values = solver.r_k_lookup[r]
        k_str = str(k_values)
        print(f"r={r:2d}: k={k_str:<20}", end="")
        
        # Print 3 per line for readability
        if (i + 1) % 3 == 0:
            print()
        else:
            print("  ", end="")
    
    if len(all_r_values) % 3 != 0:
        print()
    print()

def example_8_mathematical_formulas():
    """Example 8: Demonstrate mathematical relationships"""
    print("EXAMPLE 8: Mathematical Relationships")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    
    # Show some mathematical relationships we discovered
    print("Mathematical patterns found:")
    print()
    
    print("1. Complement pairs: If k is a solution, often 67-k is also a solution")
    examples = [(1, [1, 66]), (15, [3, 64]), (42, [5, 62])]
    for r, pair in examples:
        print(f"   r={r}: k={pair[0]} and k={pair[1]} where {pair[0]}+{pair[1]}={pair[0]+pair[1]}")
    print()
    
    print("2. Multiple solutions per r value:")
    multi_solution_r = [1, 8]  # r values with 4 solutions
    for r in multi_solution_r:
        k_vals = solver.r_k_lookup[r]
        print(f"   r={r}: has {len(k_vals)} solutions: {k_vals}")
    print()
    
    print("3. r=k cases (self-mapping):")
    self_mapping = []
    for r, k_list in solver.r_k_lookup.items():
        if r in k_list:
            self_mapping.append(r)
    print(f"   r values where r∈k: {self_mapping}")
    print()

def example_9_error_handling():
    """Example 9: Handle invalid or non-existent r values"""
    print("EXAMPLE 9: Error Handling")
    print("=" * 40)
    
    solver = ECDSAKSolver()
    
    # Test with invalid r values
    invalid_r_values = [0, 25, 50, 67, 100, -5]
    
    print("Testing with invalid r values:")
    for r in invalid_r_values:
        result = solver.solve_k_from_r(r)
        if result['k_values']:
            print(f"r={r:3d}: Found k={result['k_values']}")
        else:
            print(f"r={r:3d}: No solution found")
    print()

def example_10_interactive_finder():
    """Example 10: Interactive k finder function"""
    print("EXAMPLE 10: Interactive Usage")
    print("=" * 40)
    
    def find_k_interactive(r_value):
        """Helper function for interactive use"""
        solver = ECDSAKSolver()
        result = solver.solve_k_from_r(r_value)
        
        if result['k_values']:
            print(f"✓ Found k values for r={r_value}: {result['k_values']}")
            print(f"  Recommended k: {result['recommended_k']}")
            print(f"  Confidence: {result['confidence']}%")
            
            # Verify the recommendation
            if solver.verify_solution(result['recommended_k'], r_value):
                print(f"  ✓ Verification: k={result['recommended_k']} correctly produces r={r_value}")
            else:
                print(f"  ✗ Verification failed!")
        else:
            print(f"✗ No solution found for r={r_value}")
        print()
    
    # Test the interactive function
    print("Interactive k-finder examples:")
    test_values = [1, 19, 42, 99]
    
    for r in test_values:
        find_k_interactive(r)

def main():
    """Run all examples"""
    print("ECDSA K-Finding: Complete Usage Examples")
    print("=" * 60)
    print("Curve: y² = x³ + 7 mod 79")
    print("Base point: (1, 18), Order: 67")
    print("=" * 60)
    print()
    
    # Run all examples
    example_1_basic_usage()
    example_2_method_comparison()
    example_3_batch_processing()
    example_4_verification()
    example_5_pattern_recognition()
    example_6_performance_analysis()
    example_7_complete_r_k_mapping()
    example_8_mathematical_formulas()
    example_9_error_handling()
    example_10_interactive_finder()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()