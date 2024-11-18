from math import radians, sin, cos, sqrt, atan2
import requests
import pandas as pd
from geopy.distance import geodesic

def calculer_distance_geo(lat1, lon1, lat2, lon2):
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    
    distance_km = geodesic(point1, point2).kilometers
    
    return distance_km

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculer_distances_B_NA_csv(lat2, lon2):
    df = pd.read_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv", dtype={"personne_r1_adr_cp": str, "personne_r1_adr_cp_admin":str})

    df['distance_B_NA_AD'] = None

    for index, row in df.iterrows():
        lat1 = row['latitude_personne_adr']
        lon1 = row['longitude_personne_adr']
        
        if pd.notna(lat1) and pd.notna(lon1):
            # distance = haversine(lat1, lon1, lat2, lon2)
            distance = calculer_distance_geo(lat1, lon1, lat2, lon2)
            
            df.at[index, 'distance_B_NA_AD'] = distance
    
    df.to_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv", index=False)
    print(f"Distances calculées et ajoutées dans la colonne 'distance_B_NA_AD' du fichier.")



def calculer_distances_B_AA_csv(lat2, lon2):
    df = pd.read_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv", dtype={"personne_r1_adr_cp": str, "personne_r1_adr_cp_admin":str})

    df['distance_B_AA_AD'] = None

    for index, row in df.iterrows():
        lat1 = row['latitude_personne_adr']
        lon1 = row['longitude_personne_adr']
        
        if pd.notna(lat1) and pd.notna(lon1):
            # distance = haversine(lat1, lon1, lat2, lon2)
            distance = calculer_distance_geo(lat1, lon1, lat2, lon2)
            
            df.at[index, 'distance_B_AA_AD'] = distance
    
    df.to_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv", index=False)
    print(f"Distances calculées et ajoutées dans la colonne 'distance_B_AA_AD' du fichier.")




def geocode_single_address(adresse, code_postal, ville):
    url = f"https://api-adresse.data.gouv.fr/search/?q={adresse}&postcode={code_postal}&city={ville}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if len(data["features"]) > 0:
            coordinates = data["features"][0]["geometry"]["coordinates"]
            latitude = coordinates[1]
            longitude = coordinates[0]

            result_json = {
                "latitude": latitude,
                "longitude": longitude,
            }
            return result_json
        else:
            print("L'adresse ne correspond pas")
    else:
        print("Échec de la requête")

def Calcul_Lat_Long_B():
    df = pd.read_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv", dtype={"personne_r1_adr_cp": str, "personne_r1_adr_cp_admin":str})
    df["latitude_personne_adr"] = None
    df["longitude_personne_adr"] = None

    for index, row in df.iterrows():
        adresse = row["personne_r1_adr"]
        code_postal = row["personne_r1_adr_cp"]
        ville = row["personne_r1_adr_ville"]
        result = geocode_single_address(adresse, code_postal, ville)
        print(adresse, code_postal, ville)

        if result:
            df.at[index, "latitude_personne_adr"] = result["latitude"]
            df.at[index, "longitude_personne_adr"] = result["longitude"]
            print(result["latitude"], result["longitude"])

    df.to_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv", index=False)


    print("Terminé. Les résultats ont été enregistrés dans le fichier CSV d'origine.")


def calculate_route_distance(origin_address, destination_address, access_token):

    def get_coordinates(address, access_token):
        geocode_url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json'
        params = {
            'access_token': access_token
        }
        response = requests.get(geocode_url, params=params)
        data = response.json()
        coordinates = data['features'][0]['geometry']['coordinates']
        return coordinates

    origine_coords = get_coordinates(origin_address, access_token)
    destination_coords = get_coordinates(destination_address, access_token)

    directions_url = f'https://api.mapbox.com/directions/v5/mapbox/driving/{origine_coords[0]},{origine_coords[1]};{destination_coords[0]},{destination_coords[1]}.json'
    params = {
        'access_token': access_token,
        'geometries': 'geojson'
    }
    response = requests.get(directions_url, params=params)
    directions_data = response.json()

    distance = directions_data['routes'][0]['distance'] / 1000

    return distance


def calculate_route_time(origin_address, destination_address, access_token):
    def get_coordinates(address, access_token):
        geocode_url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json'
        params = {
            'access_token': access_token
        }
        response = requests.get(geocode_url, params=params)
        data = response.json()
        coordinates = data['features'][0]['geometry']['coordinates']
        return coordinates

    origine_coords = get_coordinates(origin_address, access_token)
    destination_coords = get_coordinates(destination_address, access_token)

    directions_url = f'https://api.mapbox.com/directions/v5/mapbox/walking/{origine_coords[0]},{origine_coords[1]};{destination_coords[0]},{destination_coords[1]}.json'
    params = {
        'access_token': access_token,
        'geometries': 'geojson'
    }
    response = requests.get(directions_url, params=params)
    directions_data = response.json()

    duration_seconds = directions_data['routes'][0]['duration']

    minutes = (duration_seconds) // 60

    return minutes

if __name__ == "__main__":
    lon2 = 5.239958
    lat2 = 46.204286

    lon_AA = 5.224195
    lat_AA = 46.211818

    Calcul_Lat_Long_B()

    calculer_distances_B_NA_csv(lat2, lon2)

    calculer_distances_B_AA_csv(lat_AA, lon_AA)

    access_token = 'pk.eyJ1IjoiamVmZjUiLCJhIjoiY20yajF1bTN3MDB5MzJxc2J1Zjh6bXl1bCJ9.yPF_SjJe5F1K5Y8pgh6Elw'

    destination_address_NA = '44 avenue Amédée Mercier 01000 BOURG EN BRESSE'
    destination_address_AA = '10 rue des Blanchisseries 01000 BOURG EN BRESSE'

    df = pd.read_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv", dtype={"personne_r1_adr_cp": str, "personne_r1_adr_cp_admin":str})

    df['distance_itineraire_NA_B_AD'] = None

    for index, row in df.iterrows():
        adresse = row["personne_r1_adr"]
        code_postal = row["personne_r1_adr_cp"]
        ville = row["personne_r1_adr_ville"]
        
        if pd.isna(adresse) or pd.isna(code_postal) or pd.isna(ville) or not adresse.strip() or not code_postal.strip() or not ville.strip():
            print(f"Adresse, code postal ou ville manquant pour l'index {index}. Enregistrement ignoré.")
            df.at[index, 'distance_itineraire_NA_B_AD'] = None 
            continue   

        origin_address = f'{adresse}, {code_postal} {ville}, France'

        try:
            distance = calculate_route_distance(origin_address, destination_address_NA, access_token)
            df.at[index, 'distance_itineraire_NA_B_AD'] = distance
        except Exception as e:
            print(f"Erreur lors du calcul pour {origin_address}: {e}")
            df.at[index, 'distance_itineraire_NA_B_AD'] = None   



    df['distance_itineraire_AA_B_AD'] = None

    for index, row in df.iterrows():
        adresse = row["personne_r1_adr"]
        code_postal = row["personne_r1_adr_cp"]
        ville = row["personne_r1_adr_ville"]
        
        if pd.isna(adresse) or pd.isna(code_postal) or pd.isna(ville) or not adresse.strip() or not code_postal.strip() or not ville.strip():
            print(f"Adresse, code postal ou ville manquant pour l'index {index}. Enregistrement ignoré.")
            df.at[index, 'distance_itineraire_AA_B_AD'] = None 
            continue 

        origin_address = f'{adresse}, {code_postal} {ville}, France'

        try:
            distance = calculate_route_distance(origin_address, destination_address_AA, access_token)
            df.at[index, 'distance_itineraire_AA_B_AD'] = distance
        except Exception as e:
            print(f"Erreur lors du calcul pour {origin_address}: {e}")
            df.at[index, 'distance_itineraire_AA_B_AD'] = None

    

    df['temps_itineraire_AA_B_AD'] = None

    for index, row in df.iterrows():
        adresse = row["personne_r1_adr"]
        code_postal = row["personne_r1_adr_cp"]
        ville = row["personne_r1_adr_ville"]
        
        if pd.isna(adresse) or pd.isna(code_postal) or pd.isna(ville) or not adresse.strip() or not code_postal.strip() or not ville.strip():
            print(f"Adresse, code postal ou ville manquant pour l'index {index}. Enregistrement ignoré.")
            df.at[index, 'temps_itineraire_AA_B_AD'] = None 
            continue 

        origin_address = f'{adresse}, {code_postal} {ville}, France'

        try:
            minutes = calculate_route_time(origin_address, destination_address_AA, access_token)
            df.at[index, 'temps_itineraire_AA_B_AD'] = minutes
        except Exception as e:
            print(f"Erreur lors du calcul pour {origin_address}: {e}")
            df.at[index, 'temps_itineraire_AA_B_AD'] = None


    
    df['temps_itineraire_NA_B_AD'] = None

    for index, row in df.iterrows():
        adresse = row["personne_r1_adr"]
        code_postal = row["personne_r1_adr_cp"]
        ville = row["personne_r1_adr_ville"]
        
        if pd.isna(adresse) or pd.isna(code_postal) or pd.isna(ville) or not adresse.strip() or not code_postal.strip() or not ville.strip():
            print(f"Adresse, code postal ou ville manquant pour l'index {index}. Enregistrement ignoré.")
            df.at[index, 'temps_itineraire_NA_B_AD'] = None 
            continue 

        origin_address = f'{adresse}, {code_postal} {ville}, France'

        try:
            minutes = calculate_route_time(origin_address, destination_address_NA, access_token)
            df.at[index, 'temps_itineraire_NA_B_AD'] = minutes
        except Exception as e:
            print(f"Erreur lors du calcul pour {origin_address}: {e}")
            df.at[index, 'temps_itineraire_NA_B_AD'] = None


    df.to_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv", index=False)
    print("Calcul des temps et distances terminé. Fichier mis à jour")