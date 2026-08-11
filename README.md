# Enfo's SOLO: X Hero Siege Edition

A survival game inspired by Warcraft 3 and Enfo's Team Survival. Built with Python and ECS architecture.

## Features
- 28 unique heroes across 3 categories (Tanks, Damage Dealers, Supports)
- 42 waves of enemies with 6 bosses
- ECS (Entity Component System) architecture
- Spellbringer magic system
- Gambit automation system
- Deep crafting economy

## Quick Start

### Running the Game

**Windows:**
```
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Or directly:**
```bash
python launcher.py      # Interactive menu
python main.py --headless   # Headless mode
python main.py --demo      # Demo mode
python main.py --test      # Run tests
```

### Generate All Files
```bash
python generate_project.py
```

## Project Structure
- `config/` - Game configuration and data
- `src/solo_x/` - Core game systems (ECS, entities, pathfinding, etc.)
- `tests/` - Unit tests

## License
MIT License

## Author
Findus Stenberg - Professional Game Developer (16 years experience)
