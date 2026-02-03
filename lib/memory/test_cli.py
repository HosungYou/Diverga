#!/usr/bin/env python3
"""
Test CLI commands to ensure they work correctly.

Usage:
    python test_cli.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli import (
    cmd_search,
    cmd_status,
    cmd_context,
    cmd_history,
    cmd_export,
    cmd_setup,
    cmd_stats
)


def test_command(name, func, *args, **kwargs):
    """Test a single command."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")

    try:
        result = func(*args, **kwargs)
        print(result)
        print(f"\n✅ {name} passed")
        return True
    except Exception as e:
        print(f"\n❌ {name} failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all CLI tests."""
    print("Diverga Memory System - CLI Tests")
    print("="*60)

    tests = [
        ("cmd_status", cmd_status),
        ("cmd_search", cmd_search, "test"),
        ("cmd_context", cmd_context),
        ("cmd_history", cmd_history),
        ("cmd_stats", cmd_stats),
        ("cmd_setup", cmd_setup),
    ]

    passed = 0
    failed = 0

    for test in tests:
        if len(test) == 2:
            name, func = test
            args, kwargs = (), {}
        elif len(test) == 3:
            name, func, *args = test
            kwargs = {}
        else:
            name, func, *args = test[:-1]
            kwargs = test[-1] if isinstance(test[-1], dict) else {}

        if test_command(name, func, *args, **kwargs):
            passed += 1
        else:
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {passed + failed}")

    if failed == 0:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
