# Linter Feature for Aura Text

## Overview
The integrated linter provides real-time error and warning indicators directly in the code editor for Python files.

## Features
- **Real-time Analysis**: Code is automatically analyzed 1.5 seconds after you stop typing
- **Multiple Linters**: Supports flake8, pylint, and pyflakes
- **Visual Indicators**: 
  - Red circle markers for errors
  - Yellow triangle markers for warnings
  - Blue circle markers for info/style suggestions
- **Inline Annotations**: Hover or view annotations below lines with issues
- **Non-intrusive**: Runs in background without blocking the editor

## Installation Requirements
Install the linters you want to use:

```bash
pip install flake8
pip install pylint
pip install pyflakes
```

## Configuration
Edit the config.json file or use the menu:

1. **Enable/Disable Linter**: Code menu → "Enable Linter"
2. **Configure Linters**: Edit `config.json`:
   ```json
   {
       "enable_linter": "True",
       "linter_types": "flake8"
   }
   ```

You can use multiple linters by separating them with commas:
```json
{
    "linter_types": "flake8,pylint"
}
```

## Usage
1. Open or create a Python (.py) file
2. Start typing code
3. Errors and warnings will appear automatically after 1.5 seconds
4. Click on markers in the margin to see details
5. View inline annotations below problematic lines

## Severity Levels
- **Error** (Red): Syntax errors, undefined names, invalid code
- **Warning** (Yellow): Style violations, potential issues
- **Info** (Blue): Code conventions, suggestions

## Supported Linters
- **flake8**: Fast, simple style checker (default)
- **pylint**: Comprehensive code analysis
- **pyflakes**: Lightweight error checker

## Customization
You can customize linter behavior by creating config files:
- `.flake8` for flake8
- `.pylintrc` for pylint

## Performance
- Linting runs in a background thread
- Has a 10-second timeout to prevent freezing
- Uses temporary files to avoid modifying your code
- Debounced to reduce CPU usage

## Troubleshooting
1. **No markers appearing**: Make sure the linter is installed (`pip install flake8`)
2. **Slow performance**: Try using only flake8 instead of multiple linters
3. **Too many warnings**: Configure linter rules in their respective config files
