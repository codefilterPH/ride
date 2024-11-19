from geopy.distance import geodesic

def get_distance(x, y):
    distance = geodesic(point1, point2).kilometers
    print(f"The distance is {distance:.2f} kilometers.")
    return

if __name__=="__main__":
    # Coordinates of two locations (latitude, longitude)
    point1 = (40.748817, -73.985428)  # Example: New York
    point2 = (34.052235, -118.243683)  # Example: Los Angeles

    get_distance(point1, point2)
