import requests

def get_active_events():
    url = "https://fortniteapi.io/v1/events/list/active?showArena=false"
    headers = {
        "accept": "application/json",
        "Authorization": "16848c5d-fc8ea709-2cfe3f70-f5ad5934"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

if __name__ == '__main__':
    events = get_active_events()
    if events:
        print("Active events data:")
        print(events)
