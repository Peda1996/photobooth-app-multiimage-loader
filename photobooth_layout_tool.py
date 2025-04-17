#!/usr/bin/env python3
import json
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading

# Try to import psd-tools, install if not available
try:
    from psd_tools import PSDImage
except ImportError:
    import subprocess

    print("Installing required package: psd-tools...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psd-tools"])
    from psd_tools import PSDImage


class PhotoboothLayoutTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Photobooth Layout Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Status variables - define these FIRST to avoid AttributeError
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0)

        # Set default paths
        self.psd_path = tk.StringVar()
        self.config_path = tk.StringVar()
        self.output_image = tk.StringVar(value="canvas_front.png")
        self.group_name = tk.StringVar(value="photobooth_images")

        # Create the UI
        self.create_widgets()

    # We're no longer using this method since configs can be on different PCs
    # But we'll keep it for reference in case it's useful in the future
    def find_config_dir(self):
        """Try to find the default config directory"""
        home = Path.home()
        possible_paths = [
            home / "config" / "photobooth",
            home / ".config" / "photobooth",
            home / "AppData" / "Local" / "photobooth"
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)

        return str(home)

    def create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title = ttk.Label(main_frame, text="Photobooth Layout Tool", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))

        # Description
        desc = ttk.Label(main_frame, text="Extract image positions from PSD files to update your photobooth layout.",
                         wraplength=500, justify="center")
        desc.pack(pady=(0, 20))

        # Input fields frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        # File input fields
        self.create_file_input(input_frame, "PSD File:", self.psd_path, self.browse_psd, 0)
        self.create_file_input(input_frame, "Config File:", self.config_path, self.browse_config, 1)

        # Other input fields
        self.create_text_input(input_frame, "Layer Group Name:", self.group_name, 2)
        self.create_file_input(input_frame, "Output Image:", self.output_image, self.browse_output, 3, save=True)

        # Process button
        process_btn = ttk.Button(main_frame, text="Process PSD File", command=self.run_process)
        process_btn.pack(pady=20, ipadx=10, ipady=5)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate",
                                        variable=self.progress_var)
        self.progress.pack(fill=tk.X, pady=10)

        # Status label
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=10)

        # Help button
        help_btn = ttk.Button(main_frame, text="Help", command=self.show_help)
        help_btn.pack(side=tk.RIGHT, pady=10)

    def create_file_input(self, parent, label_text, var, browse_cmd, row, save=False):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)

        label = ttk.Label(frame, text=label_text, width=15)
        label.pack(side=tk.LEFT, padx=5)

        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        btn = ttk.Button(frame, text="Browse", command=browse_cmd)
        btn.pack(side=tk.RIGHT, padx=5)

    def create_text_input(self, parent, label_text, var, row):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)

        label = ttk.Label(frame, text=label_text, width=15)
        label.pack(side=tk.LEFT, padx=5)

        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def browse_psd(self):
        filename = filedialog.askopenfilename(
            title="Select PSD File",
            filetypes=[("Photoshop Files", "*.psd"), ("All Files", "*.*")]
        )
        if filename:
            self.psd_path.set(filename)

    def browse_config(self):
        filename = filedialog.askopenfilename(
            title="Select Config File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if filename:
            self.config_path.set(filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output Image As",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
            defaultextension=".png"
        )
        if filename:
            self.output_image.set(filename)

    def show_help(self):
        help_text = """
Photobooth Layout Tool Help

This tool helps you create image layouts for your photobooth by extracting
layer positions from a PSD file.

How to use:
1. Create a PSD file with a layer group named "photobooth_images" 
   (or customize the name in the tool)
2. Put rectangular layers inside this group to define where photos will appear
3. Select your PSD file and config.json in this tool
4. Click "Process PSD File"

The tool will:
- Extract image positions from your PSD
- Update your photobooth config
- Generate a background image without the placeholder frames

Need more help? Visit https://photobooth-app.org/
"""
        messagebox.showinfo("Help", help_text)

    def update_status(self, message, progress=None):
        self.status_var.set(message)
        if progress is not None:
            self.progress_var.set(progress)
        self.root.update_idletasks()

    def run_process(self):
        # Validate inputs
        if not self.psd_path.get():
            messagebox.showerror("Error", "Please select a PSD file")
            return

        if not os.path.exists(self.psd_path.get()):
            messagebox.showerror("Error", "PSD file does not exist")
            return

        # Start processing in a separate thread to keep UI responsive
        threading.Thread(target=self.process_psd, daemon=True).start()

    def process_psd(self):
        try:
            # Reset progress
            self.update_status("Starting...", 0)

            # Get values from UI
            psd_path = self.psd_path.get()
            config_path = self.config_path.get()
            output_image = self.output_image.get()
            group_name = self.group_name.get()

            # Validate PSD path
            if not psd_path:
                messagebox.showerror("Error", "Please select a PSD file")
                self.update_status("Error: No PSD file selected", 0)
                return

            # Open PSD file
            self.update_status(f"Opening PSD file: {os.path.basename(psd_path)}...", 10)
            try:
                psd = PSDImage.open(psd_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open PSD file: {str(e)}\n\nMake sure it's a valid PSD file.")
                self.update_status("Error: Could not open PSD file", 0)
                return

            # Find all groups
            self.update_status("Scanning PSD structure...", 20)
            all_groups = []
            for layer in psd.descendants():
                if hasattr(layer, 'is_group') and layer.is_group():
                    all_groups.append(layer.name)

            # Find target group
            target_group = None
            for layer in psd.descendants():
                if hasattr(layer, 'is_group') and layer.is_group() and layer.name == group_name:
                    target_group = layer
                    break

            if not target_group:
                available_groups = ", ".join(all_groups) if all_groups else "No groups found"
                messagebox.showerror("Error",
                                     f"Group '{group_name}' not found.\n\nAvailable groups: {available_groups}")
                self.update_status("Error: Group not found", 0)
                return

            # Extract positions from layers
            self.update_status(f"Found group: {group_name}. Extracting positions...", 30)
            positions = []
            for layer in target_group.descendants():
                if not hasattr(layer, 'is_group') or not layer.is_group():
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

            if not positions:
                messagebox.showwarning("Warning",
                                       f"No visible layers found in '{group_name}' group.\n\nMake sure your layers are visible and contain content.")
                self.update_status("Warning: No positions found", 40)
            else:
                self.update_status(f"Found {len(positions)} image positions", 40)

            # Save positions JSON
            output_json = os.path.join(os.path.dirname(output_image), "merge_definitions.json")
            with open(output_json, 'w') as f:
                json.dump(positions, f, indent=2)

            # Try to update config if provided
            self.update_status("Processing config...", 50)
            updated_config_message = ""

            if config_path:
                try:
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as f:
                            config = json.load(f)

                        # Find collage actions and update merge_definition
                        updated_actions = 0
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
                                    updated_actions += 1

                        # Update canvas front image path in config if it's in the same directory
                        if "actions" in config and "collage" in config["actions"]:
                            for action in config["actions"]["collage"]:
                                if "processing" in action:
                                    action["processing"]["canvas_img_front_enable"] = True
                                    # Use relative path if output image is not absolute
                                    if not os.path.isabs(output_image):
                                        action["processing"]["canvas_img_front_file"] = output_image
                                    else:
                                        action["processing"]["canvas_img_front_file"] = output_image

                        # Save updated config
                        updated_config_path = config_path + '.updated'
                        with open(updated_config_path, 'w') as f:
                            json.dump(config, f, indent=2)

                        self.update_status(f"Updated {updated_actions} collage actions in config", 60)
                        updated_config_message = f"2. Updated config saved to:\n   {updated_config_path}\n\n3. To apply changes, rename the updated file to replace your original config."
                    else:
                        self.update_status("Config file not found, skipping config update", 60)
                        updated_config_message = "2. Note: Config file not found, no config was updated."
                except Exception as e:
                    messagebox.showwarning("Warning",
                                           f"Error updating config file: {str(e)}\n\nYou can still use the extracted positions and background image.")
                    self.update_status(f"Error updating config: {str(e)}", 60)
                    updated_config_message = "2. Note: There was an error updating the config file."
            else:
                self.update_status("No config file specified, skipping config update", 60)
                updated_config_message = "2. Note: No config file was specified, so no config was updated."

            # Render background image
            self.update_status("Rendering background image...", 70)
            target_group.visible = False
            output_img = psd.composite()
            output_img.save(output_image)

            # Final success message
            self.update_status("Process completed successfully!", 100)

            # Show success message with instructions
            messagebox.showinfo("Success",
                                f"Process completed successfully!\n\n"
                                f"1. Background image saved to:\n   {output_image}\n\n"
                                f"{updated_config_message}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.update_status(f"Error: {str(e)}", 0)


if __name__ == '__main__':
    # Enable high DPI support for Windows
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    root = tk.Tk()
    app = PhotoboothLayoutTool(root)
    root.mainloop()