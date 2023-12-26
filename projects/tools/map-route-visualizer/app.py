import folium
import csv


csv_file = ""

# Read data from CSV file
with open(f'data/{csv_file}', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    list_of_lats = []
    list_of_lons = []
    for row in reader:
        list_of_lats.append(float(row[0]))
        list_of_lons.append(float(row[1]))

latitude = list_of_lats[0]
longitude = list_of_lons[0]

# Create a map centered at a specific location
mymap = folium.Map(location=[latitude, longitude], zoom_start=12)

# Create a list of tuples containing lat-long pairs
coordinates = list(zip(list_of_lats, list_of_lons))

# Add markers for each lat-long point
for lat, lon in coordinates:
    folium.Marker([lat, lon]).add_to(mymap)

# Add a polyline to connect the points
folium.PolyLine(locations=coordinates, color='blue').add_to(mymap)

# Save the map to an HTML file
mymap.save("route_with_lines.html")