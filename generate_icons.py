import os
from cairosvg import svg2png

def create_theme_index(theme_dir):
    """Create the index.theme file for the icon theme."""
    content = """[Icon Theme]
Name=Hicolor
Comment=Hicolor icon theme
Directories=16x16/apps,32x32/apps,48x48/apps,64x64/apps,128x128/apps,256x256/apps

[16x16/apps]
Size=16
Context=Applications
Type=Fixed

[32x32/apps]
Size=32
Context=Applications
Type=Fixed

[48x48/apps]
Size=48
Context=Applications
Type=Fixed

[64x64/apps]
Size=64
Context=Applications
Type=Fixed

[128x128/apps]
Size=128
Context=Applications
Type=Fixed

[256x256/apps]
Size=256
Context=Applications
Type=Fixed"""

    with open(os.path.join(theme_dir, "index.theme"), "w") as f:
        f.write(content)

def generate_icons(svg_path, output_dir):
    """Generate PNG icons of different sizes from SVG."""
    sizes = [16, 32, 48, 64, 128, 256]
    
    for size in sizes:
        output_path = os.path.join(output_dir, f'advertpreneur-{size}x{size}.png')
        svg2png(url=svg_path,
                write_to=output_path,
                output_width=size,
                output_height=size)
        print(f"Generated {size}x{size} icon")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(base_dir, "images", "advertpreneur-icon.svg")
    icons_dir = os.path.join(base_dir, "icons")
    
    # Create icons directory if it doesn't exist
    os.makedirs(icons_dir, exist_ok=True)
    
    # Generate icons
    generate_icons(svg_path, icons_dir)
    
    # Set up the icon theme structure
    home = os.path.expanduser("~")
    local_icons = os.path.join(home, ".local", "share", "icons", "hicolor")
    
    # Create theme index file
    os.makedirs(local_icons, exist_ok=True)
    create_theme_index(local_icons)
    
    for size in [16, 32, 48, 64, 128, 256]:
        # Create size directory
        size_dir = os.path.join(local_icons, f"{size}x{size}", "apps")
        os.makedirs(size_dir, exist_ok=True)
        
        # Source and target paths
        source = os.path.abspath(os.path.join(base_dir, "icons", f"advertpreneur-{size}x{size}.png"))
        target = os.path.join(size_dir, "advertpreneur-converter.png")
        
        # Copy file instead of symlink
        from shutil import copy2
        if os.path.exists(target):
            os.remove(target)
        copy2(source, target)
        print(f"Copied {size}x{size} icon to theme directory")
