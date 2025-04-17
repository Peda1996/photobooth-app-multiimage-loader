# Photobooth PSD Layer Extractor

This tool helps you create and update image position layouts for photobooth-app.org's collage feature by extracting layer positions from a Photoshop (PSD) file.

## What It Does

- Extracts image placeholder positions from layers in a PSD file
- Automatically updates your photobooth configuration file with the new positions
- Creates a clean background image without the placeholder frames
- Makes it easy to design your photobooth layout visually rather than editing JSON

## Requirements

- Python 3.6 or higher
- `psd-tools` library (for reading PSD files)

## Installation

1. Make sure you have Python 3 installed
2. Install the required package:

```bash
pip install psd-tools
```

3. Download the script to your computer
4. Make it executable (Linux/Mac only):

```bash
chmod +x photobooth_psd_extractor.py
```

## Usage

### Basic Usage

```bash
python photobooth_psd_extractor.py --psd your_design.psd --config ~/config/config.json
```

### All Options

```
python photobooth_psd_extractor.py [options]

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
python photobooth_psd_extractor.py --psd my_layout.psd --config ~/config/config.json
```

#### Use a different layer group name:
```bash
python photobooth_psd_extractor.py --psd my_layout.psd --group-name "photo_frames"
```

#### Specify custom output files:
```bash
python photobooth_psd_extractor.py --psd design.psd --output-image background.png --output-json positions.json
```

## Creating Your PSD File

You can create compatible PSD files using Adobe Photoshop or free alternatives like [Photopea](https://www.photopea.com/).

### Guidelines:

1. **Create a layer group** named `photobooth_images` (or your custom name specified with `--group-name`)
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

## Troubleshooting

### Group Not Found
If you see `ERROR: Group 'photobooth_images' not found`, check:
- The spelling of your layer group name (case sensitive)
- Make sure it's a proper group, not just a layer
- Try using the `--group-name` option with the exact name shown in the error message

### No Visible Layers
If you see `Warning: No visible layers found`, check:
- Make sure your placeholder layers are visible in the PSD
- Verify they have actual content (not empty layers)

### Image Sizes
If your extracted positions look wrong:
- Make sure your PSD dimensions match your photobooth canvas dimensions
- Check your layers have clear boundaries

## Example Files

An example PSD file is included to help you get started. It demonstrates the proper structure for photobooth layouts.

## License

This script is free to use and modify for your photobooth projects.