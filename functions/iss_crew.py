import requests

HUMANS_IN_SPACE_API = "http://api.open-notify.org/astros.json"


async def people_iss():
    req = [h['name'] for h in requests.get(HUMANS_IN_SPACE_API).json()['people'] if h['craft'] == 'ISS']

    res = {
        'people': req,
        'num': len(req)
    }

    return res


if __name__ == "__main__":
    print(people_iss())
