from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_featured_image(background_path, overlay_paths, text, logo_path, output_path):
    # Open the background image
    background = Image.open(background_path)
    width, height = background.size

    # Place each overlay on the background
    for overlay_path in overlay_paths:
        overlay = Image.open(overlay_path)
        background.paste(overlay, (0, 0), overlay)

    # Add the text
    draw = ImageDraw.Draw(background)
    font_path = "fonts/georgiab.ttf"  # Replace with the font you want to use
    font_size = 45  # Font size, adjust as needed
    line_spacing = 15  # Line spacing, adjust as needed
    font = ImageFont.truetype(font_path, size=font_size)

    # Split text across up to 3 lines if it's too long
    max_width = width * 0.50 # This is where the text cut off is, so increase or decrease as needed. I have text in the first 50% of the template. and thus its at 0.50. If you only want text in the first third, adjust to 0.33
    lines = textwrap.wrap(text, width=20)  # Starting width, adjust based on testing
    while len(lines) > 5: # maximum line count, will error out above this
        font_size -= 2
        font = ImageFont.truetype(font_path, size=font_size)
        lines = textwrap.wrap(text, width=18) # forgot what this did but something about text wrapping lol, goodluck.

    # Vertically center the text block in the left 40% of the image
    total_text_height = len(lines) * font_size + (len(lines) - 1) * line_spacing
    y_start = (height - total_text_height) // 2

    for line in lines:
        temp_img = Image.new('RGBA', background.size, (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((0, 0), line, font=font, fill="#FFFFFF") 
        #223484
        bbox = temp_img.getbbox()
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        draw.text(((max_width - text_width) / 2, y_start), line, font=font, fill="#000000") # Colour of your text
        y_start += text_height + line_spacing

    # Add the logo to the bottom right, uncomment below to insert a seperate logo. I have included the logo in my overlay so don't need this.
    #logo = Image.open(logo_path)
    #lw, lh = logo.size
    #logo_position = (width - lw - 10, height - lh - 10)  # 10px padding, adjust as needed
    #background.paste(logo, logo_position, logo)

    # Save the final image, adjust quality as required
    background.save(output_path, quality=98)


background_path = "background-image.jpg"
overlay_paths = ["overlay.png", "overlay.png"]
text = "Your long title goes here and gets chopped up"
logo_path = "logo.png"
output_path = "featured_image.jpg"

create_featured_image(background_path, overlay_paths, text, logo_path, output_path)
