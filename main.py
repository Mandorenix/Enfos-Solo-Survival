#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(description="SOLO X Hero Siege Edition")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        print("Tests ready")
    elif args.headless:
        print("Headless mode ready")
    elif args.demo:
        print("Demo mode ready")
    else:
        print("SOLO X Hero Siege Edition - Use --headless, --demo, or --test")


if __name__ == "__main__":
    main()