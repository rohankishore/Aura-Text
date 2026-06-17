# Linter Feature for Aura Text

## Overview
The integrated linter provides real-time pylint error and warning indicators directly in the code editor for Python files.

## Features
- **Real-time Analysis**: Python code is automatically analyzed shortly after you stop typing
- **Visual Indicators**: 
  - Red circle markers for errors
  - Yellow circle markers for warnings
  - Blue triangle markers for convention, refactor, and info messages
- **Inline Annotations**: Hover or view annotations below lines with issues
- **Non-intrusive**: Runs through a Qt worker thread without blocking the editor

## Configuration
Edit the config.json file or use the menu:
- **Enable/Disable Linter**: Code menu → "Enable Linter"
- **Configuration flag**: Edit `config.json`:
   ```json
   {
       "enable_linter": "True"
   }
   ```

## Usage
1. Open or create a Python (.py) file
2. Start typing code
3. Errors and warnings will appear automatically after the debounce delay
4. Click on markers in the margin to see details
5. View inline annotations below problematic lines

## Severity Levels
- **Error** (Red): Syntax errors, undefined names, invalid code
- **Warning** (Yellow): Style violations, potential issues
- **Info** (Blue): Code conventions, suggestions

## Customization
You can customize linter behavior by creating a pylint config file:
- `.pylintrc`

## Performance
- Linting runs through a Qt worker thread
- Uses temporary files to avoid modifying your code
- Debounced to reduce CPU usage

## Troubleshooting
1. **No linting on a file**: The integrated linter only attaches to Python files
2. **Too many warnings**: Configure pylint rules in `.pylintrc`
