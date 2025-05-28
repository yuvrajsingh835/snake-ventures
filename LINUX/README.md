# Snake Ventures - Linux Installation Guide

## Building and Installing the Debian Package

If you're using Windows Subsystem for Linux (WSL) or need to build the package on a Linux system, follow these steps to properly build and install the game.

### Prerequisites
- Debian-based Linux system or WSL
- `dpkg` and `dpkg-deb` tools installed
- `sudo` privileges

### Building the Package

1. First, create a temporary build directory in the Linux filesystem:
```bash
cd ~
sudo rm -rf /tmp/snake-build
mkdir -p /tmp/snake-build
```

2. Copy the game files to the temporary directory:
```bash
# If using WSL with Windows files:
cp -r /mnt/c/Users/YOUR_USERNAME/path/to/"Snake Ventures"/LINUX/snake-game/* /tmp/snake-build/

# If on native Linux:
cp -r /path/to/snake-game/* /tmp/snake-build/
```

3. Set up the correct directory structure and permissions:
```bash
cd /tmp/snake-build
sudo chown -R root:root .
sudo chmod -R 755 .
sudo find . -type f -exec chmod 644 {} \;
sudo chmod 755 DEBIAN/postinst
sudo chmod 755 usr/games/snake-ventures
sudo chmod 755 usr/share/snake-ventures/main.py
```

4. Build the package in /tmp (native Linux filesystem):
```bash
cd /tmp
sudo dpkg-deb --build snake-build
sudo mv snake-build.deb snake-ventures_1.2.0_all.deb
```

### Installing the Package

1. Remove any previous installation:
```bash
sudo apt remove snake-ventures
```

2. Install the new package:
```bash
sudo dpkg -i snake-ventures_1.2.0_all.deb
sudo apt-get install -f  # Install any missing dependencies
```

3. (Optional) Copy the built package back to your Windows directory if using WSL:
```bash
cp /tmp/snake-ventures_1.2.0_all.deb /mnt/c/Users/YOUR_USERNAME/path/to/"Snake Ventures"/LINUX/
```

### Verifying the Installation

1. Check if the package is installed:
```bash
dpkg -l | grep snake-ventures
```

2. Run the game:
```bash
snake-ventures
```

### Troubleshooting

If you encounter permission issues during installation:
1. Check file permissions:
```bash
ls -l /tmp/snake-build/DEBIAN/postinst
ls -l /tmp/snake-build/usr/games/snake-ventures
ls -l /tmp/snake-build/usr/share/snake-ventures/main.py
```

2. Verify package contents:
```bash
dpkg-deb --info /tmp/snake-ventures_1.2.0_all.deb
```

### Notes
- This approach uses the native Linux filesystem (`/tmp`) to avoid Windows filesystem permission issues
- All files are properly owned by root:root as required by Debian packages
- Executable files (postinst, game binary, and main script) have 755 permissions
- Regular files have 644 permissions
- All directories have 755 permissions

### Game Features
- Animated title with figure-8 pattern
- Red glowing game over text with pulsing effects
- Mouse hover effects on menu items
- Three difficulty levels
- Improved collision detection
- Score tracking
- Pause functionality

## Running the Game
You can launch the game in three ways:
1. From the Applications menu under "Games"
2. Type `snake-ventures` in terminal
3. Click the desktop icon

## Features
- Resizable game window
- Dynamic color themes for each difficulty level
- Clean white text UI for better readability
- Pause functionality (ESC or Pause button)
- Score tracking
- Return to menu option while paused

## Files Included
- `snake-ventures/`: Debian package source
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
- Package name: snake-ventures
- Version: 1.2.0
- Architecture: all
- Dependencies: python3 (>= 3.8), python3-pygame 