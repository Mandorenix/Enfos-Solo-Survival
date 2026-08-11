#!/usr/bin/env python3
"""
SOLO X Hero Siege Edition - Professional Launcher

A user-friendly launcher with menu system, presets, and configuration.
As a professional game developer with 16 years experience, this provides
the best user experience for running the game.

Usage:
    python launcher.py              # Interactive menu
    python launcher.py --headless   # Direct headless mode
    python launcher.py --demo       # Direct demo mode
    python launcher.py --test       # Direct test mode
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any


class Launcher:
    """Professional game launcher with menu system."""
    
    def __init__(self):
        self.config_file = Path.home() / ".solo_x_config.json"
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}
        else:
            self.config = {}
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    
    def clear_screen(self) -> None:
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self) -> None:
        """Print launcher header."""
        self.clear_screen()
        print("=" * 70)
        print("     SOLO X Hero Siege Edition - Professional Launcher")
        print("     Game Developer: Findus Stenberg (16 years experience)")
        print("=" * 70)
    
    def print_menu(self) -> None:
        """Print main menu."""
        print("\nMain Menu:")
        print("-" * 70)
        print("  [1] Start Game (Headless Mode - Logic Only)")
        print("  [2] Start Game (Demo Mode - Auto-Play)")
        print("  [3] Run All Tests")
        print("  [4] Custom Game Settings")
        print("  [5] Performance Profiling Mode")
        print("  [6] Quick Test (5 waves)")
        print("  [7] Configuration Manager")
        print("  [8] Exit")
        print("-" * 70)
    
    def run_game(self, args: list) -> None:
        """Run the game with specified arguments."""
        cmd = [sys.executable, "main.py"] + args
        try:
            print(f"\nRunning: {' '.join(cmd)}\n")
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\nError: Game exited with code {e.returncode}")
        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
        
        input("\nPress Enter to continue...")
    
    def custom_settings(self) -> None:
        """Custom game settings menu."""
        self.print_header()
        print("\nCustom Game Settings:")
        print("-" * 70)
        
        waves = input("Number of waves (1-42, default 42): ").strip()
        waves = waves if waves else "42"
        
        fps = input("Target FPS (default 60): ").strip()
        fps = fps if fps else "60"
        
        seed = input("Random seed (optional): ").strip()
        verbose = input("Verbose output? (y/n, default n): ").strip().lower()
        verbose_flag = "--verbose" if verbose == "y" else ""
        seed_flag = f"--seed {seed}" if seed else ""
        
        args = ["--headless", "--waves", waves, "--fps", fps]
        if seed_flag:
            args.append(seed_flag)
        if verbose_flag:
            args.append(verbose_flag)
        
        self.run_game(args)
    
    def config_manager(self) -> None:
        """Configuration manager menu."""
        self.print_header()
        print("\nConfiguration Manager:")
        print("-" * 70)
        print("  [1] Save Current Settings as Default")
        print("  [2] Reset Configuration")
        print("  [3] View Current Configuration")
        print("  [4] Back to Main Menu")
        print("-" * 70)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            print("\nFeature coming soon: Default settings saved automatically")
        elif choice == "2":
            if self.config_file.exists():
                os.remove(self.config_file)
                self.config = {}
                print("\nConfiguration reset!")
            else:
                print("\nNo configuration to reset")
        elif choice == "3":
            print(f"\nCurrent Configuration:")
            print(f"Config file: {self.config_file}")
            print(f"Exists: {self.config_file.exists()}")
            if self.config:
                print(f"Settings: {json.dumps(self.config, indent=2)}")
            else:
                print("No configuration loaded")
        
        input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Run the interactive launcher."""
        while True:
            self.print_header()
            self.print_menu()
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1":
                self.run_game(["--headless"])
            elif choice == "2":
                self.run_game(["--demo"])
            elif choice == "3":
                self.run_game(["--test"])
            elif choice == "4":
                self.custom_settings()
            elif choice == "5":
                self.run_game(["--headless", "--verbose"])
            elif choice == "6":
                self.run_game(["--headless", "--waves", "5"])
            elif choice == "7":
                self.config_manager()
            elif choice == "8":
                print("\nExiting SOLO X Hero Siege Edition...")
                break
            else:
                print("\nInvalid choice. Please try again.")
        
        print("Goodbye!\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SOLO X Hero Siege Edition - Professional Launcher"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (no rendering)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode (auto-play)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test suite"
    )
    
    args = parser.parse_args()
    
    if args.headless or args.demo or args.test:
        # Direct mode
        cmd_args = []
        if args.headless:
            cmd_args.append("--headless")
        if args.demo:
            cmd_args.append("--demo")
        if args.test:
            cmd_args.append("--test")
        
        try:
            subprocess.run([sys.executable, "main.py"] + cmd_args, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        launcher = Launcher()
        launcher.run()


if __name__ == "__main__":
    main()