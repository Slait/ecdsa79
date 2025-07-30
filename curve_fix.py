#!/usr/bin/env python3
"""
Find valid base point for curve y² = x³ + 7 mod 79
"""

def is_on_curve(x, y, p=79, b=7):
    """Check if point (x,y) is on curve y² = x³ + 7 mod p"""
    return (y * y) % p == (x * x * x + b) % p

def find_curve_points(p=79, b=7):
    """Find all points on the curve"""
    points = []
    for x in range(p):
        y_squared = (x * x * x + b) % p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))
    return points

def main():
    print("Finding all points on curve y² = x³ + 7 mod 79")
    print("=" * 45)
    
    # Check if (2, 22) is on curve
    if is_on_curve(2, 22):
        print("✓ Point (2, 22) is on the curve")
    else:
        print("✗ Point (2, 22) is NOT on the curve")
        # Let's check what y values work for x=2
        x = 2
        y_squared = (x * x * x + 7) % 79
        print(f"For x=2: y² ≡ {y_squared} (mod 79)")
        
        valid_y = []
        for y in range(79):
            if (y * y) % 79 == y_squared:
                valid_y.append(y)
        print(f"Valid y values for x=2: {valid_y}")
    
    # Find all points on the curve
    points = find_curve_points()
    print(f"\nTotal points on curve: {len(points)}")
    print("All points:")
    for i, point in enumerate(points):
        print(f"({point[0]:2d}, {point[1]:2d})", end="  ")
        if (i + 1) % 6 == 0:
            print()
    print()
    
    # Find a good generator point
    print("\nTesting potential generator points:")
    from ecdsa_analysis import EllipticCurve
    
    for point in points[:10]:  # Test first 10 points
        try:
            curve = EllipticCurve()
            curve.base_point = point
            order = curve._calculate_order()
            print(f"Point {point}: order = {order}")
        except:
            print(f"Point {point}: calculation failed")

if __name__ == "__main__":
    main()