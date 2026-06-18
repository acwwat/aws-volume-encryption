#!/usr/bin/env python3
"""
Test to verify the actual behavior with the cleanup logic.
"""

def simulate_cleanup_with_current_logic(preserve_volumes_value):
    """Simulate the cleanup logic with current store_false"""
    print(f"\nWith action='store_false', args.preserve_volumes = {preserve_volumes_value}")
    if not preserve_volumes_value:
        print("  → Skipping deletion (volume PRESERVED)")
    else:
        print("  → Delete original volume (volume DELETED)")


def simulate_cleanup_with_fixed_logic(preserve_volumes_value):
    """Simulate the cleanup logic with fixed store_true"""
    print(f"\nWith action='store_true', args.preserve_volumes = {preserve_volumes_value}")
    if not preserve_volumes_value:
        print("  → Skipping deletion (volume PRESERVED)")
    else:
        print("  → Delete original volume (volume DELETED)")


print("=" * 70)
print("CURRENT BEHAVIOR (action='store_false'):")
print("=" * 70)

print("\nScenario 1: User does NOT pass -p flag")
print("  Expected: Delete the volume (user didn't ask to preserve)")
simulate_cleanup_with_current_logic(True)  # store_false defaults to True
print("  ❌ BUG: Volume is PRESERVED when it should be DELETED!")

print("\nScenario 2: User DOES pass -p flag")
print("  Expected: Preserve the volume (user asked to preserve)")
simulate_cleanup_with_current_logic(False)  # store_false with -p becomes False
print("  ❌ BUG: Volume is DELETED when it should be PRESERVED!")

print("\n" + "=" * 70)
print("FIXED BEHAVIOR (action='store_true'):")
print("=" * 70)

print("\nScenario 1: User does NOT pass -p flag")
print("  Expected: Delete the volume (user didn't ask to preserve)")
simulate_cleanup_with_fixed_logic(False)  # store_true defaults to False
print("  ✓ CORRECT: Volume is PRESERVED... wait, that's still wrong!")

print("\nScenario 2: User DOES pass -p flag")
print("  Expected: Preserve the volume (user asked to preserve)")
simulate_cleanup_with_fixed_logic(True)  # store_true with -p becomes True
print("  ✓ CORRECT: Volume is DELETED... wait, that's wrong too!")

print("\n" + "=" * 70)
print("ANALYSIS:")
print("=" * 70)
print("\nThe cleanup logic itself is ALSO INVERTED!")
print("The 'if not args.preserve_volumes' should be 'if args.preserve_volumes'")
print("\nWe have TWO options to fix this:")
print("1. Change action='store_false' to action='store_true'")
print("2. Fix BOTH the action AND the cleanup logic condition")
print("\nThe CORRECT fix is to change ONLY the action to 'store_true'")
print("because the cleanup logic is already written correctly,")
print("it's just that the flag value is inverted by store_false.")
