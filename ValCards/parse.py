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
                adr = float(cells[7].find("span").get_text(strip=True))
                kpr = float(cells[8].find("span").get_text(strip=True))
                apr = float(cells[9].find("span").get_text(strip=True))
                fkpr = float(cells[10].find("span").get_text(strip=True))
                fdpr = float(cells[11].find("span").get_text(strip=True))
                clp = cells[13].find("span").get_text(strip=True)
                fkdratio = round(fkpr/fdpr,2)
            except Exception as e:
                print("Error parsing stats:", e)
                return None

            # Return the dictionary with the player's name as key and a list of stats as value.
            return [f"{rating:.2f}", f"{acs:.1f}", f"{kd:.2f}", f"{adr:.1f}", kast, f"{kpr:.2f}", f"{apr:.2f}", f"{fkdratio:.2f}", clp]

    print("Player not found.")
    return None

if __name__ == "__main__":
    url = "https://www.vlr.gg/event/stats/2380/champions-tour-2025-emea-stage-1"
    player = "xeus"
    stats = parse_player_stats(url, player)
    if stats:
        print(f"Player Stats for {player}:", stats)
