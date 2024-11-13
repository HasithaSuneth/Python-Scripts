import os
from PIL import Image, ImageDraw, ImageFont

# Configuration
input_directory = "images"  # Directory containing images
output_directory = "output"  # Directory to save edited images
font_path = "fonts/arial.ttf"      # Path to a .ttf font file (you can download a .ttf file and specify the path)
font_size = 22              # Font size for text
# text_color = (255, 255, 255) # White text color
text_color = (0, 0, 0) # Black text color
offset_x, offset_y = 30, 30  # Offset for text placement from the bottom-right corner

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to add text to an image
def add_text_to_image(image_path):
    # Open image
    with Image.open(image_path) as img:
        # Initialize drawing context
        draw = ImageDraw.Draw(img)
        
        # Get image filename without extension
        filename = os.path.splitext(os.path.basename(image_path))[0].upper()
        # Load font
        font = ImageFont.truetype(font_path, font_size)
        
        # Calculate text size and position
        text_width, text_height = draw.textsize(filename, font=font)
        x = img.width - text_width - offset_x
        y = img.height - text_height - offset_y
        
        # Draw text on image
        draw.text((x, y), filename, font=font, fill=text_color)
        
        # Save the image with text in the output directory
        output_path = os.path.join(output_directory, os.path.basename(image_path))
        img.save(output_path)
        print(f"Saved: {output_path}")

# Process all images in the input directory
for filename in os.listdir(input_directory):
    file_path = os.path.join(input_directory, filename)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        add_text_to_image(file_path)
