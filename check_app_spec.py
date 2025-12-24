#!/usr/bin/env python3
"""
Production Gates Validator for AURORA

Validates that all production gates pass before deployment.
Fails CI if any gate has 'passes': false.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


def load_app_spec(spec_path: Path = Path("app_spec.json")) -> Dict[str, Any]:
    """Load app_spec.json"""
    if not spec_path.exists():
        print(f"[FAIL] ERROR: {spec_path} not found")
        sys.exit(1)

    with open(spec_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_gates(spec: Dict[str, Any]) -> bool:
    """
    Validate all production gates.
    Returns True if all pass, False otherwise.
    """
    gates = spec.get("production_gates", {})

    if not gates:
        print("[FAIL] ERROR: No production gates found in app_spec.json")
        return False

    failed_gates = []
    passed_gates = []

    print("=" * 80)
    print("AURORA PRODUCTION GATES VALIDATION")
    print("=" * 80)
    print()

    for step_name, step_data in gates.items():
        step_passes = step_data.get("passes", False)
        description = step_data.get("description", "No description")
        validation_items = step_data.get("validation", [])

        status_icon = "[PASS]" if step_passes else "[FAIL]"
        status_text = "PASS" if step_passes else "FAIL"

        print(f"{status_icon} {step_name}: {status_text}")
        print(f"   Description: {description}")

        if validation_items:
            print(f"   Validation checklist ({len(validation_items)} items):")
            for item in validation_items:
                print(f"      • {item}")

        print()

        if step_passes:
            passed_gates.append(step_name)
        else:
            failed_gates.append(step_name)

    # Summary
    print("=" * 80)
    print(f"SUMMARY: {len(passed_gates)} passed, {len(failed_gates)} failed")
    print("=" * 80)
    print()

    if failed_gates:
        print("[FAIL] FAILED GATES:")
        for gate in failed_gates:
            print(f"   • {gate}")
        print()
        print("[RESTART] ACTION REQUIRED:")
        print("   According to app_spec.json restart_condition:")
        print("   >>> Restart from step_1_architecture_design <<<")
        print()
        return False
    else:
        print("[PASS] ALL PRODUCTION GATES PASSED")
        print()
        print("[READY] System is ready for deployment")
        print()
        return True


def main():
    """Main entry point"""
    try:
        spec = load_app_spec()

        project_name = spec.get("project_name", "Unknown Project")
        version = spec.get("version", "Unknown Version")
        architecture = spec.get("architecture", "Unknown Architecture")

        print()
        print(f"Project: {project_name}")
        print(f"Version: {version}")
        print(f"Architecture: {architecture}")
        print()

        all_passed = validate_gates(spec)

        if not all_passed:
            sys.exit(1)  # Fail CI
        else:
            sys.exit(0)  # Pass CI

    except json.JSONDecodeError as e:
        print(f"[FAIL] ERROR: Invalid JSON in app_spec.json: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[FAIL] ERROR: Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
