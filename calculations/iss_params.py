import requests

ISS_API = "https://api.wheretheiss.at/v1/satellites/25544"


def iss_data():
    req = requests.get(ISS_API).json()

    res = {
        'lat': req['latitude'],
        'lng': req['longitude'],
        'alt': round(req['altitude'], 2),
        'v_kph': int(req['velocity']),
        'v_mps': round((req['velocity'] / 3.6), 3),
        'vis': req['visibility'],
    }

    return res


if __name__ == "__main__":
    print(iss_data())
