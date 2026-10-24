import requests


def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "in",
    }

    headers = {
        "User-Agent": "FoodDeliveryApp/1.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=5,
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            return None, None

        latitude = float(data[0]["lat"])
        longitude = float(data[0]["lon"])

        return latitude, longitude

    except (requests.RequestException, ValueError, KeyError):
        return None, None