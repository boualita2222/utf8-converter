#!/usr/bin/env python3
"""
Convertisseur - code à accès 3

Petit outil CLI pour convertir des nombres décimaux en base-3 (ternaire)
et inversement, et pour valider/uniformiser des codes d'accès sur 3 chiffres
composés des chiffres 0,1,2.
"""
import sys


def to_ternary(n: int, length: int = 3) -> str:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return "0".zfill(length)
    digits = []
    while n:
        digits.append(str(n % 3))
        n //= 3
    s = ''.join(reversed(digits))
    return s.zfill(length)


def from_ternary(s: str) -> int:
    s = s.strip()
    if any(ch not in '012' for ch in s):
        raise ValueError("Invalid ternary string: only digits 0,1,2 allowed")
    return int(s, 3)


def validate_code(code: str, length: int = 3) -> str:
    code = code.strip()
    # Allow decimal numbers to be converted to ternary
    if code.isdigit() and any(ch not in '012' for ch in code):
        # treat as decimal -> convert
        n = int(code)
        return to_ternary(n, length)
    # Otherwise ensure it's ternary and correct length
    if any(ch not in '012' for ch in code):
        raise ValueError("Code must contain only digits 0,1,2 or be a decimal integer")
    return code.zfill(length)


def print_usage():
    print("Usage:")
    print("  script-main.py to-ternary <decimal> [length]")
    print("  script-main.py from-ternary <ternary_string>")
    print("  script-main.py validate <code> [length]")


def main(argv):
    if len(argv) < 2:
        print_usage()
        return 1
    cmd = argv[1]
    try:
        if cmd == 'to-ternary' and len(argv) >= 3:
            n = int(argv[2])
            length = int(argv[3]) if len(argv) >= 4 else 3
            print(to_ternary(n, length))
            return 0
        if cmd == 'from-ternary' and len(argv) == 3:
            print(from_ternary(argv[2]))
            return 0
        if cmd == 'validate' and len(argv) >= 3:
            length = int(argv[3]) if len(argv) >= 4 else 3
            print(validate_code(argv[2], length))
            return 0
        print_usage()
        return 1
    except Exception as e:
        print("Error:", e)
        return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
