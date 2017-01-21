import requests
import json
import sys
import csv
from math import *

def getrequestURL():
    url = 'https://api.airbnb.com/v2/search_results'

    #refer to http://airbnbapi.org/#listing-search

    payload = {
        'client_id':'3092nxybyb0otqw18e8nh5nty',
        'locale':'en-US',	          
        'currency':"CAD",	
        '_format':"for_search_results",
        '_limit':50,
        '_offset':50,
        'guests':1,
        'ib': "false",
        'ib_add_photo_flow':"true",
        'min_bathrooms':0,
        'min_bedrooms':	1,
        'max_bedrooms':1,
        'location': "15 Grenville St M4Y 1A1",
        'min_beds':	0,
        'price_min':40,
        'price_max':210	,
        'min_num_pic_urls':	3,
        'sort':	1,
        'suppress_facets': "true",
        'user_lat':	43.661917,
        'user_lng':	-79.384079

    }
    
    r = requests.get(url, params=payload)
    print(r.url);
    #print(r.text)
    #return r.json()

    
def getlatlong(address):
    print("locating ", address, "...")
    gmapsurl = 'https://maps.googleapis.com/maps/api/geocode/json'
    gmapspayload = {
        'address': address,
        'key': 'AIzaSyD6HHmupNncEKNVvGzYqVzmRQzbBLb55s0'
    }
    gmapsr = requests.get(gmapsurl, params=gmapspayload)
    print(gmapsr.url)
    data = gmapsr.json()
    lat = data["results"][0]["geometry"]["location"]["lat"]
    lng = data["results"][0]["geometry"]["location"]["lng"]
    print("lat, long: ", lat, lng)
    return lat, lng



def getalllistingdata(raw_data):
    entire = 0
    total = 0
    for places in data["search_results"]:
        total = total + 1
        listing = places["listing"]
        pricing = places["pricing_quote"]

        name = listing["name"]
        id = listing["id"]
        bedrooms = listing['bedrooms']
        beds = listing["beds"]
        bathrooms = listing["bathrooms"]
        room_type = listing["room_type"]
        address = listing["public_address"]
        reviews = listing["reviews_count"]
        price = pricing["localized_nightly_price"]

        if room_type == "Entire home/apt":
            entire = entire + 1
            print("name: ", name)
            print("id", id)
            print("bedrooms ", bedrooms)
            print("beds: ", beds)
            print("bathrooms: ", bathrooms)
            print("address: ", address)
            print("price: ", price)
            print("reviews: ", reviews)
            print()
    
    print("total: ", total, "entire homes:", entire)

#save data to csv
def savetocsv(data):
    with open("airbnbresults.csv", 'w') as csvfile:
        fieldnames = ["name", "id", "bedrooms", "beds", "bathrooms",  "person_capacity", "public_address", "price", "reviews_count", "star_rating","distance(km)", "lat", "long"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        processedids = []
        #loop through all listings
        for places in data["search_results"]:
            listing = places["listing"]
            id = listing["id"]
            room_type = listing["room_type"]
            listing["price"] = places["pricing_quote"]["localized_nightly_price"]
            print("processing id:", id)



            delete = []
            if room_type == "Entire home/apt":
                if id not in processedids:
                    for values in listing:
                        if values not in fieldnames:
                            #print(values)
                            delete.append(values)

                    for deletion in delete:
                        #print(deletion)
                        del(listing[deletion])


                    #use google maps api to get address latitude and longditude
                    lat, lng = getlatlong(listing["public_address"])
                    listing["lat"] = lat
                    listing["long"] = lng

                    compare_lat = 43.661776
                    compare_long = -79.384221

                    lat, lng, compare_lat, compare_long = map(radians, [lat, lng, compare_lat, compare_long])

                    dlat = lat-compare_lat
                    dlon = lng-compare_long
                    a = pow((sin(dlat/2)),2) + cos(compare_lat) * cos(lat) * pow((sin(dlon/2)),2)
                    c = 2 * atan2(sqrt(a), sqrt(1-a))
                    distance = 6368.065 * c

                    listing["distance(km)"] = distance
                    
                    
                    writer.writerow(places["listing"])
                    print("added listing id: ", id)
                    
                else:
                    print("id: ", id, "processed. Skipping.")
            else:
                print("Listing is a ", listing["room_type"], ". Skipping.")

            print("*******************************************************")



#get url for api call
getrequestURL()

#use this to get data directly
#datastring = getrequestURL()   
#data = json.load(datastring)
#print(data)

#use this to read from file
with open('alltorontodata.json', encoding='utf-8') as data_file:
   data = json.loads(data_file.read())

#prints out data file
#getalllistingdata(data)

#saves listing data to CSV file
savetocsv(data)
