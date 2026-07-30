import rasterio
import os

class GeoEngine:
    def __init__(self):
        # 1. Get the directory of THIS script (level_3/)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Construct the path: look into the 'tools' folder from here
        self.substrate_path = os.path.join(script_dir, "mbagathi_clipped.tif")
        
        if not os.path.exists(self.substrate_path):
            raise FileNotFoundError(f"Critical: Substrate not found at {self.substrate_path}")

    def get_elevation(self, lat, lon):
        with rasterio.open(self.substrate_path) as src:
            # src.index converts lat/lon to pixel coordinates (row, col)
            row, col = src.index(lon, lat)
            
            # Read the elevation value (the first band)
            # We use 0,0 for the band, then row/col for the pixel
            elevation = src.read(1)[row, col]
            return elevation

# Example usage
if __name__ == "__main__":
    engine = GeoEngine()
    # Mbagathi coordinates
    lat, lon = -1.35, 36.85
    elev = engine.get_elevation(lat, lon)
    print(f"Terrain Elevation at ({lat}, {lon}): {elev} meters")