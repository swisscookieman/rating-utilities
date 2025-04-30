from PIL import Image, ImageDraw, ImageFont
import colorsys
import csv

import requests
from bs4 import BeautifulSoup

def parse_player_stats(url, target_player):
    # Fetch the webpage
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Unable to retrieve the webpage.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the stats table (adjust the class name if needed)
    table = soup.find("table", class_="wf-table mod-stats mod-scroll")
    if not table:
        print("Error: Stats table not found.")
        return None

    tbody = table.find("tbody")
    if not tbody:
        print("Error: Table body not found.")
        return None

    # Iterate over each row in the table body
    for row in tbody.find_all("tr"):
        # The player name is in the first cell with class "mod-player"
        player_cell = row.find("td", class_="mod-player")
        if not player_cell:
            continue
        name_div = player_cell.find("div", class_="text-of")
        if not name_div:
            continue

        name = name_div.get_text(strip=True)
        # Check if this row corresponds to the target player (case-insensitive)
        if name.lower() == target_player.lower():
            # Get all the cells in the row
            cells = row.find_all("td")
            try:
                rating = float(cells[3].find("span").get_text(strip=True))
                acs = float(cells[4].find("span").get_text(strip=True))
                kd = float(cells[5].find("span").get_text(strip=True))
                kast = cells[6].find("span").get_text(strip=True)
                if kast != "":
                    kast = float(kast.strip().rstrip("%")) / 100
                adr = float(cells[7].find("span").get_text(strip=True))
                kpr = float(cells[8].find("span").get_text(strip=True))
                apr = float(cells[9].find("span").get_text(strip=True))
                fkpr = float(cells[10].find("span").get_text(strip=True))
                fdpr = float(cells[11].find("span").get_text(strip=True))
                clp = cells[13].find("span").get_text(strip=True)
                if clp != "":
                    clp = float(clp.strip().rstrip("%")) / 100
                else:
                    clp = 0
                fkdratio = round(fkpr/fdpr,2)
            except Exception as e:
                print("Error parsing stats:", e)
                return None
            cardrating = round((rating/1.35)*50+50)
            if cardrating >= 100:
                cardrating = 99
            # Return the dictionary with the player's name as key and a list of stats as value.
            return [cardrating, rating, acs, acs/195.41, kd, kd/1, adr, adr/128.1, kast, kast/0.71, kpr, kpr/0.69, apr, apr/0.27, fkdratio, fkdratio/1.08,clp, clp/0.15]
    #averages: [1.0, 195.41, 1.01, 128.3, 0.71, 0.69, 0.27, 1.08, 0.15]
    print("Player not found.")
    return None

# Open the image
image = Image.open("ValCards/card.png")

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
    goals_text_box(image,f"{round(value)}")

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
    saves_text_box(image,f"{round(value)}")

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
    with open('Cards/major1.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Skip the header row
        next(reader)
        
        # Search for the player
        for row in reader:
            if row[1].lower() == player_name.lower():
                print(row)
                # Convert all values to float and return stats (excluding team name and player name)
                return [float(value) for value in row[2:]]
        
        # Return empty list if player not found
        return []
    

def score_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
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
    
def card_rating(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 160)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 42*2, 29*2
    w, h = 132*2, 76*2
    text = text[:2]
    draw = ImageDraw.Draw(image)
    
    # Calculate text position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center coordinates
    x_centered = x + (w - text_width) / 2
    y_centered = y + (h - text_height) / 2 - text_bbox[1]  # Adjust for font ascent
    

    if int(text) > 92: 
        colorfill = "#FF3DF9"
    elif int(text) > 87:
        colorfill = "#20BE45"
    elif int(text) > 83: 
        colorfill = "#EEFE14"
    else:
        colorfill = "#EA3030"
    
    # Draw centered text (white color by default)
    draw.text(
        (x_centered, y_centered),
        text,
        font=font,
        fill=colorfill,  # Change color as needed
        anchor="lt"
    )

def wor_text_box(image, text):
    # Load custom font
    try:
        font = ImageFont.truetype("Designer.otf", 80)
    except IOError:
        raise Exception("Font file 'Designer.otf' not found in directory")

    # Text box parameters
    x, y = 421*2, 738*2
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


def wor(value):
    # Rectangle parameters
    x = 412*2
    y = 776*2
    minwidth = 140
    height = 14.5*2
    radius = 15  # Corner radius
    addwidth = (value*18)

    if addwidth > 56*2:
        addwidth = 56*2
    if addwidth <= -109:
        addwidth = -109
    # Calculate the bounding box coordinates
    left = x
    top = y
    right = x + minwidth + addwidth
    bottom = y + height

    if value > 3: 
        colorfill = "#FF3DF9"
    elif value > 0:
        colorfill = "#20BE45"
    elif value > -2: 
        colorfill = "#EEFE14"
    else:
        colorfill = "#EA3030"
    # Draw the rounded rectangle (modify fill color as needed)
    draw.rounded_rectangle(
        xy=[(left, top), (right, bottom)],
        radius=radius,
        fill=colorfill,  # Change color here if needed
        outline=None  # Add outline color if desired
    )
    wor_text_box(image,f"{value:.2f}")
# Rating, r rGPG, GPG, rAss, Ass, rSaves, Saves, rShots, Shots, rShooting, Shooting% 


url = "https://www.vlr.gg/event/stats/2380/champions-tour-2025-emea-stage-1"
player = "MiniBoo"
playerstats = parse_player_stats(url,player)
print("INITIAL")

print(playerstats)
card_rating(image,str(playerstats[0]))
Rating(playerstats[1])
Goals(playerstats[3], playerstats[2])
assists(playerstats[5], playerstats[4])
saves(playerstats[7], playerstats[6])
shots(playerstats[9], playerstats[8])
shooting(playerstats[11], playerstats[10])
demos(playerstats[13],playerstats[12])
score(playerstats[15], playerstats[14])
wor(playerstats[16])
image.save("ValCards/output.png")
print("Image saved as output.png")