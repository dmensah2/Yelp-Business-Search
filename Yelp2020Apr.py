#Author: Deidre Mensah
#Title: Yelp API
#Date Last Modified: 04/10/2020
#Purpose: Business Search using Yelp API business search endpoint

#imports all necessary modules
import requests, json, csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#creates variables for user inputs
location_search = str(raw_input("Enter the location: "))
category_criteria = str(raw_input("Enter your the business category or categories: "))
radius_search = int(raw_input("Enter the radius around your location in meters (Note: Maximum is 40,000m): "))

#authorizes api key
api_key = 'ptHy-cbk_S-NV_c1uU57IfiZGpkqrhYU50sHDPcaKD8CItrhP5tKhiJcmbYrlx03GDa_gttq9UJytu4Ux3nUMyfGBoXF5hGvQ1kXWUasvWojFm4DAwFpFXs61Dv9XXYx'
headers = {'Authorization': 'Bearer %s' % api_key}

#endpoint
url = 'https://api.yelp.com/v3/businesses/search'

#creates csv file
output = open("YelpOutput.csv", "wb")
writer = csv.DictWriter(output, fieldnames=["Name", "Address", "Category", "City", "Latitude", "Longitude"])
writer.writeheader()

#iterates through multiple pages of results and pulls 50 results for each page
for offset in range(0, 1000,50):
    params = {
        'limit': 50,
        'location': location_search,
        'categories': category_criteria,
        'radius': radius_search,
        'offset': offset
    }

    response = requests.get(url, params=params, headers=headers,verify=False)

    parsed = json.loads(response.text)

    businesses = parsed["businesses"]

    for business in businesses:
        row = ({"Name": business["name"].encode('ascii','ignore').decode('ascii'), "Address": business["location"]["address1"], "Category": business["categories"][0]["title"], "City": business["location"]["city"],"Latitude": business["coordinates"]["latitude"], "Longitude": business["coordinates"]["longitude"]})
        writer.writerow(row)
        print("Name:", business["name"])
        print("Address:", business["location"]["address1"])
        print ("Category:", business["categories"][0]["title"])
        print ("City", (business["location"]["city"]))
        print("latitude", business["coordinates"]["latitude"])
        print("longitude", business["coordinates"]["longitude"])
        print("\n")

    #output.close()

    count = len(businesses)

# returns total count of businesses
    if count == 0:
        break
    elif count != 50:
        total = count + offset
        print "Your search returned " + str(total) + " businesses."
