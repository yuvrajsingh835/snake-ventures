# Snake Ventures - Linux Version

## Installation
1. Open terminal in this directory
2. Run the following commands:
```bash
cd snake-game
chmod +x DEBIAN/postinst
dpkg-deb --build .
sudo dpkg -i ../snake-game.deb
sudo apt-get install -f  # Install dependencies if needed
```

## Running the Game
You can launch the game in three ways:
1. From the Applications menu under "Games"
2. Type `snake-game` in terminal
3. Click the desktop icon

## Features
- Resizable game window
- Dynamic color themes for each difficulty level
- Clean white text UI for better readability
- Pause functionality (ESC or Pause button)
- Score tracking
- Return to menu option while paused

## Files Included
- `snake-game/`: Debian package source
  - `DEBIAN/`: Package control files
  - `usr/`: Game files and executables
- `Source Code/`: Contains the Python source code

## System Requirements
- Linux distribution with dpkg (Debian, Ubuntu, etc.)
- Python 3.8 or higher
- Python-Pygame package (automatically installed)

## Controls
- Arrow keys: Control snake direction
- ESC: Pause game
- M (while paused): Return to main menu
- Mouse: Menu navigation and button clicks

## Package Information
- Package name: snake-game
- Version: 1.0.0
- Architecture: amd64
- Dependencies: python3 (>= 3.8), python3-pygame 