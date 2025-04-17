#!/usr/bin/env python3
import json
import os
import argparse
from psd_tools import PSDImage


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract image positions from PSD and update photobooth config')
    parser.add_argument('--psd', default='background.psd', help='Path to the PSD file')
    parser.add_argument('--config', default='config.json', help='Path to the photobooth config file')
    parser.add_argument('--output-image', default='canvas_front.png', help='Output path for rendered background')
    parser.add_argument('--group-name', default='photobooth_images',
                        help='Name of the group containing image placeholders')
    parser.add_argument('--output-json', default='merge_definitions.json', help='Path for extracted positions JSON')
    args = parser.parse_args()

    # Open PSD file
    print(f"Opening PSD file: {args.psd}")
    try:
        psd = PSDImage.open(args.psd)
    except Exception as e:
        print(f"Error opening PSD file: {e}")
        return

    # Find all groups to help with debugging
    all_groups = []
    for layer in psd.descendants():
        if hasattr(layer, 'is_group') and layer.is_group():
            print(f"Found group: {layer.name}")
            all_groups.append(layer.name)

    # Find the target group
    target_group = None
    for layer in psd.descendants():
        if hasattr(layer, 'is_group') and layer.is_group() and layer.name == args.group_name:
            target_group = layer
            break

    if not target_group:
        print(f"ERROR: Group '{args.group_name}' not found. Available groups: {', '.join(all_groups)}")
        return

    print(f"Found target group: {target_group.name}")

    # Extract image positions from visible layers
    positions = []
    for layer in target_group.descendants():
        if not hasattr(layer, 'is_group') or not layer.is_group():  # Only process non-group layers
            if layer.is_visible() and hasattr(layer, 'bbox') and layer.bbox:
                x1, y1, x2, y2 = layer.bbox
                width = x2 - x1
                height = y2 - y1

                positions.append({
                    "description": layer.name,
                    "pos_x": x1,
                    "pos_y": y1,
                    "width": width,
                    "height": height,
                    "rotate": 0,
                    "predefined_image": None,
                    "image_filter": "original"
                })
                print(f"Found position: {layer.name} ({x1}, {y1}, {width}x{height})")

    if not positions:
        print(f"Warning: No visible layers found in '{args.group_name}' group")

    # Save extracted positions to JSON
    with open(args.output_json, 'w') as f:
        json.dump(positions, f, indent=2)
    print(f"Saved positions to {args.output_json}")

    # Try to update config file if it exists
    if os.path.exists(args.config):
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)

            # Find collage actions and update merge_definition
            if "actions" in config and "collage" in config["actions"]:
                for i, action in enumerate(config["actions"]["collage"]):
                    if "processing" in action and "merge_definition" in action["processing"]:
                        # Keep image filters from existing config if available
                        if len(action["processing"]["merge_definition"]) == len(positions):
                            for j, pos in enumerate(positions):
                                existing = action["processing"]["merge_definition"][j]
                                pos["image_filter"] = existing.get("image_filter", "original")
                                pos["predefined_image"] = existing.get("predefined_image", None)

                        action["processing"]["merge_definition"] = positions
                        print(f"Updated merge_definition in collage action {i}")

            # Save updated config
            updated_config_path = args.config + '.updated'
            with open(updated_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"Saved updated config to {updated_config_path}")
        except Exception as e:
            print(f"Error updating config file: {e}")

    # Hide the layer group and render background
    target_group.visible = False
    output_img = psd.composite()
    output_img.save(args.output_image)
    print(f"Rendered background image (without {args.group_name}) to {args.output_image}")

    # Print snippet for manual config update
    print("\n/// Paste this into your config under collage → merge_definition:")
    print(json.dumps(positions, indent=2))


if __name__ == '__main__':
    main()