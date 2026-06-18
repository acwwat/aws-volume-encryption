#!/usr/bin/env python3
"""
Test to verify the preserve_volumes flag behavior.
This test demonstrates the current inverted logic bug.
"""

import argparse
import sys


def test_current_behavior():
    """Test current inverted behavior"""
    parser = argparse.ArgumentParser(description='Encrypts EBS volumes of an EC2 instance.')
    parser.add_argument('-i', '--instance', help='EC2 instance ID', required=False)
    parser.add_argument('-k', '--kms_key_id', help='KMS key', required=False)
    parser.add_argument('-p', '--preserve_volumes', help='Preserve original volumes',
                        required=False, action='store_false')
    
    # Test 1: No flag passed (should preserve, but doesn't)
    args1 = parser.parse_args([])
    print(f"Test 1 - No flag passed: args.preserve_volumes = {args1.preserve_volumes}")
    print(f"  Expected: True (preserve volumes)")
    print(f"  Actual: {args1.preserve_volumes}")
    print(f"  PASS" if args1.preserve_volumes else f"  FAIL - VOLUMES WILL BE DELETED!")
    
    # Test 2: Flag passed (should delete, but preserves)
    args2 = parser.parse_args(['-p'])
    print(f"\nTest 2 - Flag -p passed: args.preserve_volumes = {args2.preserve_volumes}")
    print(f"  Expected: False (delete volumes)")
    print(f"  Actual: {args2.preserve_volumes}")
    print(f"  PASS" if not args2.preserve_volumes else f"  FAIL - VOLUMES WILL BE PRESERVED!")


def test_fixed_behavior():
    """Test fixed behavior"""
    parser = argparse.ArgumentParser(description='Encrypts EBS volumes of an EC2 instance.')
    parser.add_argument('-i', '--instance', help='EC2 instance ID', required=False)
    parser.add_argument('-k', '--kms_key_id', help='KMS key', required=False)
    parser.add_argument('-p', '--preserve_volumes', help='Preserve original volumes',
                        required=False, action='store_true')
    
    # Test 1: No flag passed (should delete)
    args1 = parser.parse_args([])
    print(f"\n\nFIXED BEHAVIOR:")
    print(f"Test 1 - No flag passed: args.preserve_volumes = {args1.preserve_volumes}")
    print(f"  Expected: False (delete volumes)")
    print(f"  Actual: {args1.preserve_volumes}")
    print(f"  PASS" if not args1.preserve_volumes else f"  FAIL")
    
    # Test 2: Flag passed (should preserve)
    args2 = parser.parse_args(['-p'])
    print(f"\nTest 2 - Flag -p passed: args.preserve_volumes = {args2.preserve_volumes}")
    print(f"  Expected: True (preserve volumes)")
    print(f"  Actual: {args2.preserve_volumes}")
    print(f"  PASS" if args2.preserve_volumes else f"  FAIL")


if __name__ == "__main__":
    print("=" * 70)
    print("CURRENT INVERTED BEHAVIOR:")
    print("=" * 70)
    test_current_behavior()
    
    print("\n" + "=" * 70)
    print("FIXED BEHAVIOR:")
    print("=" * 70)
    test_fixed_behavior()
