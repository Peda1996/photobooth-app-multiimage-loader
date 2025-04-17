# Photobooth PSD Layer Extractor

This tool helps you create and update image position layouts for photobooth-app.org's collage feature by extracting layer positions from a Photoshop (PSD) file.

## What It Does

- Extracts image placeholder positions from layers in a PSD file
- Automatically updates your photobooth configuration file with the new positions
- Creates a clean background image without the placeholder frames
- Makes it easy to design your photobooth layout visually rather than editing JSON

## Quick Start

### Windows

1. Make sure Python is installed on your system
2. Run `install.bat` to install required packages
3. Run `start_ui.bat` to launch the graphical interface
   - Or use `start.bat` for command-line version

### Linux/Mac

1. Make sure Python is installed on your system
2. Run `./install.sh` to install required packages and make scripts executable
3. Run `./start_ui.sh` to launch the graphical interface
   - Or use `./start.sh` for command-line version

## Installation Details

### Requirements

- Python 3.6 or higher
- `psd-tools` library (for reading PSD files)

### Manual Installation

If the installation scripts don't work for you:

1. Make sure you have Python 3 installed
2. Install the required package:

```bash
pip install psd-tools
```

3. Make scripts executable (Linux/Mac only):

```bash
chmod +x *.sh *.py
```

## Using the Graphical Interface

1. Run `start_ui.bat` (Windows) or `./start_ui.sh` (Linux/Mac)
2. Click "Browse" to select your PSD file
3. Click "Browse" next to Config File to find your photobooth config.json
4. Make sure "Layer Group Name" is set to "photobooth_images" (or your custom group name)
5. Click "Process PSD File"
6. The tool will:
   - Extract image positions from your PSD
   - Update your config file (saved as config.json.updated)
   - Generate a background image with placeholders hidden

## Using the Command-Line Interface

### Basic Usage

```bash
# Windows
start.bat --psd your_design.psd --config "C:\path\to\config.json"

# Linux/Mac
./start.sh --psd your_design.psd --config ~/config/config.json
```

### All Options

```
Options:
  --psd FILE            Path to your PSD file (default: background.psd)
  --config FILE         Path to your photobooth config file (default: config.json)
  --output-image FILE   Output path for the rendered background (default: canvas_front.png)
  --group-name NAME     Name of the layer group containing image placeholders (default: photobooth_images)
  --output-json FILE    Path for the extracted positions JSON (default: merge_definitions.json)
```

### Common Examples

#### Extract from PSD and update config:
```bash
./start.sh --psd my_layout.psd --config ~/config/config.json
```

#### Use a different layer group name:
```bash
./start.sh --psd my_layout.psd --group-name "photo_frames"
```

#### Specify custom output files:
```bash
./start.sh --psd design.psd --output-image background.png --output-json positions.json
```

## Creating Your PSD File

You can create compatible PSD files using Adobe Photoshop or free alternatives like [Photopea](https://www.photopea.com/).

### Guidelines:

1. **Create a layer group** named `photobooth_images` (or your custom name)
2. Inside this group, **add a separate layer for each image placeholder**
   - Name each layer descriptively (e.g., "left", "top_right", etc.)
   - These names will appear in your configuration
3. **Design your placeholders** to show where photos will appear
   - Use rectangles, frames, or any shape that defines the photo area
   - The script will extract the exact position and dimensions
4. **Add background elements** outside of the `photobooth_images` group
   - These will remain visible in your final output

### Example Structure:
```
- Background (layer)
- Decorative elements (layers)
- photobooth_images (group)
  - left_photo (layer)
  - center_photo (layer)
  - right_photo (layer)
```

## Output Files

The script generates several files:

1. **Updated config** (`config.json.updated`)
   - A copy of your original config with the new image positions
   - Review this file and rename it to replace your original config

2. **Position JSON** (`merge_definitions.json`)
   - Just the extracted position data in JSON format
   - Useful for manual editing or backup

3. **Background image** (`canvas_front.png`)
   - Your design with the placeholder frames removed
   - Ready to use as a canvas_img_front_file in your config

## Photobooth Config Location

The photobooth config is typically located at:
- Linux: `~/.config/photobooth/config.json`
- Windows: `C:\Users\YOUR_USERNAME\config\photobooth\config.json`
- Mac: `~/config/photobooth/config.json`

The graphical interface will attempt to automatically find this directory.

## Troubleshooting

### Installation Issues
- Make sure Python 3.6+ is installed and in your PATH
- Try running the install script again
- For manual installation, run: `pip install psd-tools`

### Group Not Found
If you see `ERROR: Group 'photobooth_images' not found`, check:
- The spelling of your layer group name (case sensitive)
- Make sure it's a proper group, not just a layer
- In the GUI, check the "Layer Group Name" field is correct

### No Visible Layers
If you see `Warning: No visible layers found`, check:
- Make sure your placeholder layers are visible in the PSD
- Verify they have actual content (not empty layers)

### Image Sizes
If your extracted positions look wrong:
- Make sure PSD dimensions match your photobooth canvas dimensions
- Check your layers have clear boundaries

## Example Files

An example PSD file is included to help you get started. It demonstrates the proper structure for photobooth layouts.

## License

This script is free to use and modify for your photobooth projects.