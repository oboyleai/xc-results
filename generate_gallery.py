import os
import re
from pathlib import Path

# Define base directories
BASE_DIR = Path('.')
MEETS_DIR = BASE_DIR / 'meets'
IMAGES_DIR = BASE_DIR / 'images' / 'meets'

# Define mapping of meet HTML files to their image directories
MEET_IMAGE_MAPPINGS = {
    "37th_Early_Bird_Open_Mens_5000_Meters_HS_Open_5K_24.html": "235827",
    "37th_Early_Bird_Open_Womens_5000_Meters_HS_Open_5K_24.html": "235827",
    "56th_Holly-Duane_Raffin_Festival_of_Races_Mens_5000_Meters_D1_Boys_24.html": "236072",
    "56th_Holly-Duane_Raffin_Festival_of_Races_Mens_5000_Meters_D1_JV_Boys_24.html": "236072",
    "56th_Holly-Duane_Raffin_Festival_of_Races_Womens_5000_Meters_D1_Girls_24.html": "236072"
}

def generate_gallery_items(image_dir_id):
    """Generate HTML for gallery items based on images in the meet directory"""
    image_dir = IMAGES_DIR / image_dir_id
    if not image_dir.exists():
        print(f"Warning: Image directory not found: {image_dir}")
        return ""
    
    image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
    gallery_items = []
    
    for pattern in image_patterns:
        for img in sorted(image_dir.glob(pattern)):
            relative_path = os.path.relpath(img, MEETS_DIR)
            item = f'<div class="gallery-item">\n  <img src="/{relative_path}" alt="Meet photo" class="gallery-image" loading="lazy">\n</div>'
            gallery_items.append(item)
    
    return "\n".join(gallery_items)

def update_meet_html(html_file):
    """Update meet HTML file with gallery section"""
    filename = os.path.basename(html_file)
    full_path = MEETS_DIR / filename
    
    if filename not in MEET_IMAGE_MAPPINGS:
        return
        
    image_dir_id = MEET_IMAGE_MAPPINGS[filename]
    
    if not full_path.exists():
        print(f"Warning: Meet file not found: {full_path}")
        return
    
    with open(full_path, 'r') as f:
        content = f.read()
    
    gallery_items = generate_gallery_items(image_dir_id)
    
    if not gallery_items:
        print(f"No images found for {filename} in directory {image_dir_id}")
        return
    
    # New gallery section with proper HTML tags
    gallery_section = f"""    <!-- Gallery Section -->
    <div class="section gallery expandable">
        <h2>Meet Gallery</h2>
        <div class="content">
            <div class="gallery-grid">
                {gallery_items}
            </div>
            
            <div id="gallery-lightbox" class="lightbox">
                <span class="close-btn">&times;</span>
                <img id="lightbox-img" src="" alt="Enlarged meet photo">
                <button class="nav-btn prev">❮</button>
                <button class="nav-btn next">❯</button>
            </div>
        </div>
    </div>

    <script src="../js/gallery.js"></script>
    """
    
    # Find the closing body tag and insert the gallery section before it
    content = content.replace('</body>', f'{gallery_section}</body>')
    
    with open(full_path, 'w') as f:
        f.write(content)
        print(f"Updated {filename} with gallery section")

def main():
    if not MEETS_DIR.exists():
        print(f"Error: Meets directory not found: {MEETS_DIR}")
        return
    
    if not IMAGES_DIR.exists():
        print(f"Error: Images directory not found: {IMAGES_DIR}")
        return
        
    for meet_file in MEET_IMAGE_MAPPINGS.keys():
        update_meet_html(meet_file)

if __name__ == "__main__":
    main()