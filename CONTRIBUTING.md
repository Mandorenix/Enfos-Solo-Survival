# Contributing to Enfo's SOLO: X Hero Siege Edition

We welcome contributions! Please follow these guidelines.

## Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python -m pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Mandorenix/Enfos-Solo-Survival.git
cd Enfos-Solo-Survival

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venvScriptsactivate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all public functions and classes
- Keep lines under 88 characters
- Use descriptive variable names

## Testing

All code should be tested. Run tests with:

```bash
python -m pytest tests/ -v
```

## Pull Request Guidelines

1. **Title**: Clear and descriptive
2. **Description**: Explain what the PR does and why
3. **Tests**: Include tests for new functionality
4. **Documentation**: Update documentation if needed
5. **Changelog**: Add entry to CHANGELOG.md if applicable

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

## Code of Conduct

Be respectful and inclusive. Follow standard open source contribution guidelines.
