import os
import json
import pyproj
from shapely.ops import transform
from shapely.geometry import shape


def get_basin_area(geojson_path):
    # 1. Load the boundary data
    with open(geojson_path) as f:
        data = json.load(f)
    
    # 2. Extract geometry
    poly = shape(data['features'][0]['geometry'])
    
    # 3. Define Projector: WGS84 (lat/lon) -> UTM Zone 37S (Meters)
    # Kenya is in EPSG:32737
    project = pyproj.Transformer.from_crs(
        "EPSG:4326", 
        "EPSG:32737", 
        always_xy=True
    ).transform
    
    # 4. Project and calculate area
    poly_meters = transform(project, poly)
    area_sq_km = poly_meters.area / 1_000_000
    
    print(f"Verified Basin Area: {area_sq_km:.2f} km²")

if __name__ == "__main__":
    # Robust Pathing: Find this script's directory, then point to assets/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(script_dir, "basin.geojson")
    
    # Run the area check
    if os.path.exists(geojson_path):
        get_basin_area(geojson_path)
    else:
        print(f"Error: File not found at {geojson_path}")

# square degrees

# def get_basin_area(geojson_path):
#     with open(geojson_path) as f:
#         data = json.load(f)
    
#     # Convert the GeoJSON geometry to a Shapely polygon
#     poly = shape(data['features'][0]['geometry'])
    
#     # Note: For accurate square meters, you must project to a 
#     # local coordinate system (e.g., UTM), but for a rough 
#     # estimate in degrees, you can see the complexity.
#     print(f"Polygon Area (in coordinate units): {poly.area}")

# # Get the directory where this script resides (level_3/assets/)
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Construct the full path to your geojson file
# geojson_path = os.path.join(script_dir, "basin.geojson")

# # Run the function with the absolute path
# get_basin_area(geojson_path)
