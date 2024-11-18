import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("_with_dist_ancien_centre_as_select_distinct_demande_id_from_gold_202410181544.csv")

rapproches = df[df['distance_itineraire_NA_B_AD'] < df['distance_itineraire_AA_B_AD']].shape[0]
eloignes = df[df['distance_itineraire_NA_B_AD'] > df['distance_itineraire_AA_B_AD']].shape[0]

moyenne_ancienne = df['distance_itineraire_AA_B_AD'].mean()
moyenne_nouvelle = df['distance_itineraire_NA_B_AD'].mean()

quantiles_ancienne = df['distance_itineraire_AA_B_AD'].quantile([0.25, 0.5, 0.75])
quantiles_nouvelle = df['distance_itineraire_NA_B_AD'].quantile([0.25, 0.5, 0.75])

mediane_nouvelle = df['distance_itineraire_NA_B_AD'].median()
mediane_ancienne = df['distance_itineraire_AA_B_AD'].median()

moyenne_temps_AA = df['temps_itineraire_AA_B_AD'].mean()
moyenne_temps_NA = df['temps_itineraire_NA_B_AD'].mean()

print(f"Moyenne de temps à l'ancienne adresse:{moyenne_temps_AA}")
print(f"Moyenne de temps à la nouvelle adresse:{moyenne_temps_NA}")

print(f"\nMédiane de la distance à la nouvelle adresse: {mediane_nouvelle:.2f} km")
print(f"Médiane de la distance à l'ancienne adresse: {mediane_ancienne:.2f} km")

print(f"\nNombre de bénéficiaires qui se sont rapprochés de la nouvelle adresse: {rapproches}")
print(f"Nombre de bénéficiaires qui se sont éloignés de la nouvelle adresse: {eloignes}")

print(f"\nMoyenne distance ancienne adresse: {moyenne_ancienne:.2f} km")
print(f"Moyenne distance nouvelle adresse: {moyenne_nouvelle:.2f} km")

print("\nQuantiles distance ancienne adresse:")
print(quantiles_ancienne)

print("\nQuantiles distance nouvelle adresse:")
print(quantiles_nouvelle)

if 'temps_itineraire_NA_B_AD' in df.columns:
    df['temps_itineraire_NA_B_AD'] = pd.to_numeric(df['temps_itineraire_NA_B_AD'], errors='coerce')
    bins = [0, 5, 10, 15, float('inf')]
    labels = ['0-5 min', '5-10 min', '10-15 min', '15 min et plus']
    df['intervalle_temps'] = pd.cut(df['temps_itineraire_NA_B_AD'], bins=bins, labels=labels, right=False)
    result = df['intervalle_temps'].value_counts().sort_index()
    print("\nNombre de personnes par intervalle de temps de trajet(Nouvelle adresse) :")
    print(result)
else:
    print("La colonne 'temps_itineraire_NA_B_AD' n'existe pas dans le fichier CSV.")


if 'temps_itineraire_AA_B_AD' in df.columns:
    df['temps_itineraire_AA_B_AD'] = pd.to_numeric(df['temps_itineraire_AA_B_AD'], errors='coerce')
    bins = [0, 5, 10, 15, float('inf')]
    labels = ['0-5 min', '5-10 min', '10-15 min', '15 min et plus']
    df['intervalle_temps'] = pd.cut(df['temps_itineraire_AA_B_AD'], bins=bins, labels=labels, right=False)
    result = df['intervalle_temps'].value_counts().sort_index()
    print("\nNombre de personnes par intervalle de temps de trajet(Ancienne adresse) :")
    print(result)
else:
    print("La colonne 'temps_itineraire_NA_B_AD' n'existe pas dans le fichier CSV.")




df['distance_itineraire_AA_B_AD'] = pd.to_numeric(df['distance_itineraire_AA_B_AD'], errors='coerce')
df['distance_itineraire_NA_B_AD'] = pd.to_numeric(df['distance_itineraire_NA_B_AD'], errors='coerce')

plt.figure(figsize=(10, 6))
plt.scatter(df['distance_itineraire_AA_B_AD'], df['distance_itineraire_NA_B_AD'], alpha=0.6)

plt.title("Distance des Anciennes et Nouvelles Familles")
plt.xlabel("Distance Ancienne Famille (km)")
plt.ylabel("Distance Nouvelle Famille (km)")

min_distance = min(df['distance_itineraire_AA_B_AD'].min(), df['distance_itineraire_NA_B_AD'].min())
max_distance = max(df['distance_itineraire_AA_B_AD'].max(), df['distance_itineraire_NA_B_AD'].max())
plt.plot([min_distance, max_distance], [min_distance, max_distance], color='red', linestyle='--')

plt.grid()
plt.show()
