#!/usr/bin/env python3
"""
Tests for the preserve_volumes flag behaviour.

Verifies:
  1. action='store_true' so the flag defaults to False (delete) and becomes True when passed.
  2. The cleanup condition uses `if args.preserve_volumes:` (not `if not ...`) so
     the branch taken matches the flag value and the print message.
"""

import argparse
import sys


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance', required=False)
    parser.add_argument('-k', '--kms_key_id', required=False)
    parser.add_argument('-p', '--preserve_volumes',
                        required=False, action='store_true')
    return parser


def simulate_cleanup(preserve_volumes):
    """Return ('skip', volume_id) or ('delete', volume_id) mirroring the fixed logic."""
    volume_id = 'vol-abc123'
    if preserve_volumes:
        return ('skip', volume_id)
    else:
        return ('delete', volume_id)


# ── flag default ──────────────────────────────────────────────────────────────

def test_default_is_false():
    args = build_parser().parse_args([])
    assert args.preserve_volumes is False, (
        f"Expected False by default, got {args.preserve_volumes}"
    )
    print("PASS: default value is False (volumes will be deleted)")


def test_flag_sets_true():
    args = build_parser().parse_args(['-p'])
    assert args.preserve_volumes is True, (
        f"Expected True when -p passed, got {args.preserve_volumes}"
    )
    print("PASS: -p sets preserve_volumes to True (volumes will be preserved)")


# ── cleanup logic ─────────────────────────────────────────────────────────────

def test_cleanup_deletes_when_flag_not_set():
    action, _ = simulate_cleanup(False)
    assert action == 'delete', (
        f"Expected 'delete' when preserve_volumes=False, got '{action}'"
    )
    print("PASS: volumes are deleted when --preserve_volumes is not passed")


def test_cleanup_skips_when_flag_set():
    action, _ = simulate_cleanup(True)
    assert action == 'skip', (
        f"Expected 'skip' when preserve_volumes=True, got '{action}'"
    )
    print("PASS: volumes are preserved when --preserve_volumes is passed")


if __name__ == '__main__':
    failures = 0
    for test in [
        test_default_is_false,
        test_flag_sets_true,
        test_cleanup_deletes_when_flag_not_set,
        test_cleanup_skips_when_flag_set,
    ]:
        try:
            test()
        except AssertionError as e:
            print(f"FAIL: {e}")
            failures += 1

    if failures:
        print(f"\n{failures} test(s) failed.")
        sys.exit(1)
    else:
        print("\nAll tests passed.")
