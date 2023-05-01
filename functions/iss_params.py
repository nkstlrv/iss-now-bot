import requests

ISS_API = "https://api.wheretheiss.at/v1/satellites/25544"


def iss_data():
    req = requests.get(ISS_API).json()

    dt = req['visibility']

    if 'day' in dt:
        dt = 'Day ☀️'
    elif 'ecl' in dt:
        dt = 'Night 🌙'

    res = {
        'lat': req['latitude'],
        'lng': req['longitude'],
        'alt': int(req['altitude']),
        'v_kph': int(req['velocity']),
        'v_mps': round((req['velocity'] / 3.6)),
        'vis': dt,
    }

    return res


if __name__ == "__main__":
    print(iss_data())
