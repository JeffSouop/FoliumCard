import pandas as pd
import folium
import requests

df = pd.read_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv")

access_token = 'pk.eyJ1IjoiamVmZjUiLCJhIjoiY20yajF1bTN3MDB5MzJxc2J1Zjh6bXl1bCJ9.yPF_SjJe5F1K5Y8pgh6Elw'

lon_AA, lat_AA = 5.224195, 46.211818
lon2, lat2 = 5.239958, 46.204286

def get_isochrone_data(lat, lon, time_minutes, access_token):
    isochrone_url = f'https://api.mapbox.com/isochrone/v1/mapbox/walking/{lon},{lat}'
    params = {
        'contours_minutes': time_minutes,
        'polygons': 'true',
        'access_token': access_token
    }
    response = requests.get(isochrone_url, params=params)
    response.raise_for_status()
    return response.json()

carte = folium.Map(zoom_start=10)

if 'latitude_personne_adr' in df.columns and 'longitude_personne_adr' in df.columns:
    df = df.dropna(subset=['latitude_personne_adr', 'longitude_personne_adr'])

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude_personne_adr'], row['longitude_personne_adr']],
            popup=f"Coordonnées: ({row['latitude_personne_adr']}, {row['longitude_personne_adr']})",
            icon=folium.Icon(color='blue', icon='home', prefix='fa')
        ).add_to(carte)

    folium.Marker(
        location=[lat_AA, lon_AA],
        popup="Ancien Centre",
        icon=folium.Icon(color='red', icon='cloud', prefix='fa')
    ).add_to(carte)

    folium.Marker(
        location=[lat2, lon2],
        popup="Nouveau Centre",
        icon=folium.Icon(color='green', icon='cloud', prefix='fa')
    ).add_to(carte)

    red_colors = ["#ffcccc", "#ff6666", "#cc0000"]
    green_colors = ["#ccffcc", "#66ff66", "#009900"]
    blue_colors = ["#0077B3", "#0099CC", "#33B5E5"]

    for i, minutes in enumerate([5, 10, 15]):
        isochrone_data = get_isochrone_data(lat_AA, lon_AA, minutes, access_token)
        folium.GeoJson(
            isochrone_data,
            style_function=lambda feature, color=red_colors[2]: {
                'fillColor': blue_colors[0],
                'color': color,
                'weight': 2,
                'fillOpacity': 0.1
            }
        ).add_to(carte)
    for i, minutes in enumerate([5, 10, 15]):
        isochrone_data = get_isochrone_data(lat2, lon2, minutes, access_token)
        folium.GeoJson(
            isochrone_data,
            style_function=lambda feature, color=green_colors[2]: {
                'fillColor': color,
                'color': color,
                'weight': 2,
                'fillOpacity': 0.1
            }
        ).add_to(carte)

    carte.fit_bounds([[df['latitude_personne_adr'].min(), df['longitude_personne_adr'].min()],
                      [df['latitude_personne_adr'].max(), df['longitude_personne_adr'].max()]])

    carte.save('Carte_des_personnes.html')
    print("La carte a été sauvegardée sous 'Carte_des_personnes.html'")
else:
    print("Les colonnes 'latitude_personne_adr' et 'longitude_personne_adr' sont manquantes dans le fichier CSV.")
