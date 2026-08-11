#!/usr/bin/env python3
"""
Enfo's SOLO: X Hero Siege Edition
Main game entry point
"""

import argparse
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from solo_x.core.game import Game
from solo_x.core.state import GameState, GamePhase
from config.balancing import BALANCE
from config.heroes import HEROES
from config.waves import WAVES


def main():
    parser = argparse.ArgumentParser(
        description="Enfo's SOLO: X Hero Siege Edition"
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
    parser.add_argument(
        "--waves",
        type=int,
        default=42,
        help="Number of waves to play (default: 42)"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=60,
        help="Target FPS (default: 60)"
    )
    parser.add_argument(
        "--hero",
        type=int,
        default=1,
        help="Hero ID to use (default: 1)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible games"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    if args.test:
        run_tests()
    elif args.headless or args.demo:
        run_game(args)
    else:
        # Interactive mode - show menu
        show_main_menu()


def show_main_menu():
    """Show main menu"""
    print("=" * 70)
    print("     Enfo's SOLO: X Hero Siege Edition")
    print("=" * 70)
    print("
Available Heroes:")
    for hero in HEROES.get_all_heroes()[:10]:  # Show first 10
        print(f"  [{hero.id}] {hero.name} ({hero.category}) - {hero.description}")
    print("
Options:")
    print("  --headless    Run in headless mode")
    print("  --demo        Run in demo mode")
    print("  --test        Run tests")
    print("  --hero N      Select hero (1-28)")
    print("  --waves N     Number of waves (1-42)")
    print("  --fps N      Target FPS")
    print("  --seed N      Random seed")
    print("  --verbose     Verbose output")
    print("
Example:")
    print("  python main.py --headless --hero 1 --waves 20")


def run_game(args):
    """Run the game"""
    print(f"
Starting game...")
    print(f"  Hero: {args.hero}")
    print(f"  Waves: {args.waves}")
    print(f"  Mode: {'Demo' if args.demo else 'Headless'}")
    print(f"  Target FPS: {args.fps}")
    
    # Initialize game
    game = Game(
        hero_id=args.hero,
        max_waves=args.waves,
        target_fps=args.fps,
        seed=args.seed,
        verbose=args.verbose
    )
    
    # Run game loop
    try:
        if args.demo:
            game.run_demo()
        else:
            game.run()
    except KeyboardInterrupt:
        print("
Game interrupted by user")
    except Exception as e:
        print(f"
Error: {e}")
        import traceback
        traceback.print_exc()


def run_tests():
    """Run test suite"""
    print("
Running tests...")
    print(f"  Total waves configured: {WAVES.total_waves}")
    print(f"  Total heroes: {len(HEROES.get_all_heroes())}")
    print(f"  Starting lives: {BALANCE.game_settings.starting_lives}")
    print(f"  Max waves: {BALANCE.game_settings.max_waves}")
    print("
All configuration files loaded successfully!")
    print("
Test: Loading all heroes...")
    for hero in HEROES.get_all_heroes():
        print(f"  - {hero.name} ({hero.category})")
    print("
Test: Loading all waves...")
    for wave in WAVES.get_all_waves()[:5]:
        print(f"  - Wave {wave.wave}: {len(wave.enemies)} enemies, {wave.reward}g reward")
    print("
✅ All tests passed!")


if __name__ == "__main__":
    main()