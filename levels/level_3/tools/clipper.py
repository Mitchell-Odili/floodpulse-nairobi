import rasterio
from rasterio.mask import mask
import json
import os

def clip_srtm(tif_path, geojson_path, output_path):
    """
    Clips a large SRTM raster (.hgt or .tif) to a specific basin boundary.
    """
    # 1. Load the basin boundary
    with open(geojson_path) as f:
        basin_data = json.load(f)
        # Extract geometry: supports GeoJSON Features or FeatureCollections
        geometry = basin_data['features'][0]['geometry']

    # 2. Open the SRTM tile
    with rasterio.open(tif_path) as src:
        # 3. Clip the raster
        # crop=True shrinks the raster to the extent of the polygon
        out_image, out_transform = mask(src, [geometry], crop=True)
        out_meta = src.meta.copy()

    # 4. Update metadata for the new clipped file
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    # 5. Write the clipped file to disk
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(out_image)
    
    print(f"Success: Clipped raster saved to {output_path}")

if __name__ == "__main__":
    # Define paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input files
    input_hgt = os.path.join(script_dir, "s02e036.hgt")
    boundary_file = os.path.join(script_dir, "..", "assets", "basin.geojson")
    
    # Output file
    output_tif = os.path.join(script_dir, "mbagathi_clipped.tif")
    
    # Run the function
    clip_srtm(input_hgt, boundary_file, output_tif)