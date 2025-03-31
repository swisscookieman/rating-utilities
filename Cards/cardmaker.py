from PIL import Image, ImageDraw, ImageFont
import colorsys
import csv
# Open the image
image = Image.open("Cards/input.png")

# Create a drawing context
draw = ImageDraw.Draw(image)


def color(number):
    # Clamp input between 0.60 and 1.40
    n = max(0.60, min(number, 1.40))
    
    # Define color transitions using HSV
    if n > 1.349:
        # Bright pink (magenta)
        h = 300/360  # Hue for pink
    elif n >= 1.00:
        # Yellow to green transition (1.00-1.349)
        ratio = (n - 1.00) / (1.349 - 1.00)
        h = (60 + ratio * 60) / 360  # 60° (yellow) to 120° (green)
    else:
        # Red to orange to yellow transition (0.60-1.00)
        ratio = (n - 0.60) / (1.00 - 0.60)
        h = ratio * 60 / 360  # 0° (red) to 60° (yellow)
    
    # Constant saturation and value for bright colors
    s = 1.0
    v = 1.0
    
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    # Convert to hex format
    return "#{:02x}{:02x}{:02x}".format(
        int(r * 255),
        int(g * 255),
        int(b * 255)
    )

def rating_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 74*2, 526*2
    w, h = 93*2, 30*2
    
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill="black",  # Change color as needed
        anchor="lt"
    )

def Rating(rating):
    # Rectangle parameters
    x = 58*2
    y = 562*2
    minwidth = 31
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = ((rating-0.6)*100*1.375)*2

    if addwidth > 110*2:
        addwidth = 110*2
    if addwidth <= 0:
        addwidth = 0
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=color(rating),  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    rating_text_box(image,f"{rating:.2f}")

def goals_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 247*2, 526*2
    w, h = 102*2, 30*2
    
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill="black",  # Change color as needed
        anchor="lt"
    )

def Goals(rating, value):
    # Rectangle parameters
    x = 235*2
    y = 562*2
    minwidth = 31
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = ((rating-0.6)*100*1.375)*2
    if addwidth > 110*2:
        addwidth = 110*2
    if addwidth <= 0:
        addwidth = 0
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=color(rating),  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    goals_text_box(image,f"{value:.2f}")

def assists_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 422*2, 526*2
    w, h = 107*2, 30*2
    
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill="black",  # Change color as needed
        anchor="lt"
    )

def assists(rating, value):
    # Rectangle parameters
    x = 412*2
    y = 562*2
    minwidth = 31
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = ((rating-0.6)*100*1.375)*2
    if addwidth > 110*2:
        addwidth = 110*2
    if addwidth <= 0:
        addwidth = 0
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=color(rating),  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    assists_text_box(image,f"{value:.2f}")


def saves_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 74*2, 632*2
    w, h = 93*2, 30*2
    
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill="black",  # Change color as needed
        anchor="lt"
    )

def saves(rating, value):
    # Rectangle parameters
    x = 58*2
    y = 669*2
    minwidth = 31
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = ((rating-0.6)*100*1.375)*2

    if addwidth > 110*2:
        addwidth = 110*2
    if addwidth <= 0:
        addwidth = 0
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=color(rating),  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    saves_text_box(image,f"{value:.2f}")

def shots_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 247*2, 632*2
    w, h = 102*2, 30*2
    
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill="black",  # Change color as needed
        anchor="lt"
    )

def shots(rating, value):
    # Rectangle parameters
    x = 235*2
    y = 669*2
    minwidth = 31
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = ((rating-0.6)*100*1.375)*2

    if addwidth > 110*2:
        addwidth = 110*2
    if addwidth <= 0:
        addwidth = 0
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=color(rating),  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    shots_text_box(image,f"{value:.2f}")

def shooting_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 408*2, 632*2
    w, h = 135*2, 30*2
    
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill="black",  # Change color as needed
        anchor="lt"
    )

def shooting(rating, value):
    # Rectangle parameters
    x = 412*2
    y = 669*2
    minwidth = 31
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = ((rating-0.6)*100*1.375)*2

    if addwidth > 110*2:
        addwidth = 110*2
    if addwidth <= 0:
        addwidth = 0
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=color(rating),  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    shooting_text_box(image,f"{value:.2f}")


def get_player_stats(player_name):
    # Open the CSV file and read its contents
    with open('Stats/processed-major1.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Skip the header row
        next(reader)
        
        # Search for the player
        for row in reader:
            if row[1].lower() == player_name.lower():
                # Convert all values to float and return stats (excluding team name and player name)
                return [float(value) for value in row[2:]]
        
        # Return empty list if player not found
        return []
    

def score_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 60)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 246*2, 738*2
    w, h = 107*2, 30*2
    
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill="black",  # Change color as needed
        anchor="lt"
    )

def score(rating, value):
    # Rectangle parameters
    x = 235*2
    y = 776*2
    minwidth = 31
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = ((rating-0.6)*100*1.375)*2

    if addwidth > 110*2:
        addwidth = 110*2
    if addwidth <= 0:
        addwidth = 0
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=color(rating),  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    score_text_box(image,f"{value:.2f}")

def demos_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 68*2, 738*2
    w, h = 107*2, 30*2
    
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill="black",  # Change color as needed
        anchor="lt"
    )

def demos(rating, value):
    # Rectangle parameters
    x = 58*2
    y = 776*2
    minwidth = 31
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = ((rating-0.6)*100*1.375)*2

    if addwidth > 110*2:
        addwidth = 110*2
    if addwidth <= 0:
        addwidth = 0
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=color(rating),  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    demos_text_box(image,f"{value:.2f}")
    
# Rating, r rGPG, GPG, rAss, Ass, rSaves, Saves, rShots, Shots, rShooting, Shooting% 
playerstats = get_player_stats("Vatira.")
print("INITIAL")
print(playerstats)
playerstats.pop(1)
playerstats.pop(1)
print("REMOVE WR")
print(playerstats)
score(playerstats[1], playerstats[2])
Rating(playerstats[0])
playerstats.pop(1)
playerstats.pop(1)
print("REMOVE SCORE")
print(playerstats)
Goals(playerstats[1], playerstats[2])
assists(playerstats[3], playerstats[4])
saves(playerstats[5], playerstats[6])
shots(playerstats[7], playerstats[8])
shooting(playerstats[9], playerstats[10])
demos(playerstats[11],playerstats[12])
image.save("Cards/output.png")
print("Image saved as output.png")