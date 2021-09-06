"""
Created on Thu Apr 15 09:32:05 2021
Imports Flamingo scooters status from JSON and maps using geopandas
@author: Ryan
"""

import geopandas as gpd
import pandas as pd
import json
import urllib
import matplotlib.pyplot as plt
import datetime as dt

def import_json(city):
        """Imports a JSON file from the URL, saves as local json file"""     
        url = (f"https://api.flamingoscooters.com/gbfs/{city}/free_bike_status.json")
        flamingos = (json.load(urllib.request.urlopen(url))) #converts json to dict
        data = flamingos['data']
        bikes = data['bikes']
                          
        return (bikes)


def print_import_summary(bikes):
        """Prints max/min latitude and longitudes and number of assets imported"""
        num_assets = len(bikes)
        max_lon, min_lon = 0, 0
        max_lat, min_lat = 0, 0 

        #checks latitude and longitude of bike dicts in bikes list to find max, mins         
        for bike in bikes:
            if bike['lon'] > max_lon:
                max_lon = bike['lon']                
            else:
                 bike['lon'] < min_lon
                 min_lon = bike['lon']
                 
            #latitude if statement is reversed because we are in southern
            #hemisphere, latitudes are negative values               
            if bike['lat'] < max_lat:
                 max_lat = bike['lat']                
            else:
                 bike['lat'] > min_lat
                 min_lat = bike['lat']
     
        print(f"{num_assets} currently stationary flamingo assets imported.")
        print(f"Max longitude: {max_lon}")
        print(f"Min longitude: {min_lon}")
        print(f"Max latitude: {max_lat}")
        print(f"Min latitude: {min_lat}")
        

def save_csv(data, filename, city):
        """Saves data to a csv file"""
        try:
            data.to_csv(f"{filename}_{city}.csv", index=False)
            print(f"{filename}_{city}.csv file saved.")
        except PermissionError:
            print("Cannot save new flamingoLocations file, make sure .csv file is closed")
            

def get_city():
    """user input for city"""
    city_exists = False
    city_list = ['christchurch', 'wellington']
    print("Pick a city to map e-scooter locations: \n")
    while not city_exists:
        for city in city_list:            
            print(str(city).capitalize())
        city = str(input("City: ").lower())
        if city in city_list:
            city_exists = True
        else:
            print("Please choose from the available options")
            
    return city, city_list
    


def convert_to_df(data):
        """Takes a dict file, converts to dataframe"""
        df = pd.DataFrame(data) 
        return df
    
                   
def get_shp(city, city_list):
        """Plots base map with given SHP file"""
        if city == city_list[0]:
            shp = 'nz-roads-chc.shp'
        elif city == city_list[1]:
            shp = 'nz-roads-wlg.shp'            
        shape_file = gpd.read_file(shp)        
        
        return shape_file

  
def plot_map(shp,size, geo_df, city):
        """Plots base map with given SHP file"""
        now = dt.datetime.now()
        hour = now.strftime("%H:%M:%S")
        date = now.strftime("%d/%m/%Y")
        city = city.capitalize()
        fig, ax = plt.subplots(figsize = (size, size/1.5))
        shp.plot(ax = ax, color='gray')
        geo_df.plot(ax=ax, color='purple', label="Flamingo E-Scooter")
        ax.set_xlabel("Latitude")
        ax.set_ylabel("Longitude")
        plt.rc('font', size=20)
        plt.rc('axes', titlesize=30)
        plt.title(label=(f"Flamingo E-Scooter locations in {city} at {hour} on {date}"))
        plt.legend(prop={'size' : 15}) 
                   
        return
    
    
def save_map():
    """Asks for filename, saves the plot as png"""
    filename = input("Filename? ")
    plt.savefig(f"{filename}.png")
    print(f"Map saved as \"{filename}.png\"")
    
    
def ask_yes_no(question):
        """Asks given Q, return true or false """
        answer = ""    
        while answer != 'Y' and answer != 'N': 
            answer = (input(f"{question} Y/N ")).upper()
        if answer == 'Y':
            return True
        else:
            return False  


def create_geodataframe(df):
        """Plots coordinates in a given dataframe"""
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
        
        return (gdf)
    
    
def main():
    """Runs the show"""    
    city, city_list = get_city()
    bikes = import_json(city)
    print_import_summary(bikes)
    df = convert_to_df(bikes)
    shp = get_shp(city, city_list)
    geo_df = create_geodataframe(df)
    save_csv(df, 'flamingoLocations', city)
    plot_map(shp, 50, geo_df, city)
    if ask_yes_no("Save map?") == True:
        save_map()    

main()



