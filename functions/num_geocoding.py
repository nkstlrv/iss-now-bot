import phonenumbers
from phonenumbers import geocoder
import os
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

load_dotenv()


def geocode_num(num):
    num_data = phonenumbers.parse(num)
    loc = geocoder.description_for_number(num_data, 'en')
    cage_geo = OpenCageGeocode(os.getenv("OPENCAGE_KEY"))
    res = cage_geo.geocode(str(loc))
    coordinates = res[0]['geometry']

    return coordinates


if __name__ == "__main__":
    print(geocode_num(os.getenv("PHONENUM")))
