# Snake Ventures Game

A modern implementation of the classic Snake game with multiple difficulty levels, dynamic themes, and resizable window support.

![Screenshot 2025-05-28 053940](https://github.com/user-attachments/assets/acc8d688-ee3f-4f1e-92df-ccae021a1944)

## Available Versions

This repository contains both Windows and Linux versions of the game:

### Windows Version (`/Windows` folder)
- Ready-to-run executable: `SnakeGame.exe`
- No installation required
- Windows 10 or later supported

### Linux Version (`/Linux` folder)
- Debian package format (.deb)
- Supports Debian-based distributions (Ubuntu, Linux Mint, etc.)
- Requires Python 3.8+ and pygame (auto-installed)

## Features
- Three difficulty levels:
  - Easy: No boundaries, slower speed
  - Medium: With boundaries, medium speed
  - Hard: With boundaries, fastest speed
- Dynamic color themes for each difficulty level:
  - Easy: Limegreen snake
  - Medium: Orange snake
  - Hard: Neon cyan snake
- Animated title with figure-8 snake pattern
- Rainbow color effects
- Clean white text UI for better readability across all modes
- Resizable game window
- Red glowing game over screen with hover effects
- Score tracking and Pause functionality
- Return to menu option while paused
- Return to menu and Restart option when GAME OVER

## Installation & Running

### Windows
1. Navigate to the `Windows` folder
2. Double-click `SnakeGame.exe` to start playing
3. Choose your difficulty level and enjoy!

### Linux
1. Navigate to the `Linux` folder
2. Open terminal and run:
```bash
cd snake-game
chmod +x DEBIAN/postinst
dpkg-deb --build .
sudo dpkg -i ../snake-game.deb
sudo apt-get install -f  # Install dependencies if needed
```
3. Launch the game through:
   - Applications menu under "Games"
   - Terminal command: `snake-game`
   - Desktop icon

## Controls
- Arrow keys: Control snake direction
- ESC: Pause game
- M (while paused): Return to main menu
- SPACE: Restarts the game with current selected difficulty level
- Mouse: Menu navigation and button clicks

## Source Code
Both versions include the source code in their respective `Source Code` folders.

For detailed instructions specific to each platform, please refer to:
- Windows version: `/Windows/README.md`
- Linux version: `/Linux/README.md` 
