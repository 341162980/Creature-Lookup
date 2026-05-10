#Contains python for map generation
import matplotlib
matplotlib.use("Agg")

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box
import os
import re

WORLD_URL = ("https://naturalearth.s3.amazonaws.com/"
            "110m_cultural/ne_110m_admin_0_countries.zip")

OCEAN_URL = ("https://naturalearth.s3.amazonaws.com/"
            "50m_physical/ne_50m_geography_marine_polys.zip")

# --- Custom Region Groups ---
REGION_ALIASES = {
    "americas": ["North America", "South America"],
    "amazon rainforest": ["Brazil", "Peru", "Bolivia", "Ecuador", 
                        "Colombia", "Venezuela", "French Guiana", "Guyana", "Suriname"],
    "central america": ["Mexico", "Guatemala", "Belize", "Honduras",
                        "El Salvador", "Nicaragua", "Costa Rica", "Panama"],
    "middle east": ["Saudi Arabia", "Iran", "Iraq", "Israel", "Jordan",
                    "United Arab Emirates", "Qatar", "Kuwait",
                    "Oman", "Yemen", "Syria", "Lebanon"],
    "indian subcontinent": ["India", "Pakistan", "Bangladesh", "Nepal",
                            "Bhutan", "Sri Lanka"],
    "north africa": ["Africa"],
    "indonesia": ["Indonesia"],
    "borneo": ["Indonesia", "Malaysia", "Brunei"],
    "sumatra": ["Indonesia"],
    "southeast asia": ["Asia"],
    "south asia": ["Asia"],
    "tasmania": ["Australia"],
    "galápagos islands": ["Ecuador"],
    "new guinea": ["Papua New Guinea", "Indonesia"],
    "sub-saharan africa": ["Africa"],  # simplified
    "indo-pacific region": ["Indian Ocean", "Pacific Ocean"],
    "all oceans": ["Pacific Ocean", "Atlantic Ocean",
                "Indian Ocean", "Arctic Ocean", "Southern Ocean"],
    "oceans worldwide": ["Pacific Ocean", "Atlantic Ocean",
                        "Indian Ocean", "Arctic Ocean", "Southern Ocean"],
    "worldwide": ["Africa", "Asia", "Europe",
                "North America", "South America", "Oceania", "Antarctica"],
    "northern hemisphere": ["North America", "Europe", "Asia"],
}

# Words to remove (ignore cardinal directions)
REMOVE_WORDS = ["western", "eastern", "northern", "southern",
    "central", "tropical"]


def clean_region_name(name):
    name = name.lower()

    # remove direction words
    for word in REMOVE_WORDS:
        name = re.sub(rf"\b{word}\b", "", name)

    name = name.replace("(", "").replace(")", "")
    name = name.strip()

    return name


def highlight_region(input_string, show_map=True):

    world = gpd.read_file(WORLD_URL)
    world.columns = world.columns.str.lower()
    oceans = gpd.read_file(OCEAN_URL)
    oceans.columns = oceans.columns.str.lower()

    regions = [r.strip() for r in input_string.split(",")]

    matches = []

    for region_raw in regions:

        region = clean_region_name(region_raw)

        # --- Alias group ---
        if region in REGION_ALIASES:
            for subregion in REGION_ALIASES[region]:

                # Ocean inside alias
                ocean_match = oceans[oceans["name_en"].str.lower() == subregion.lower()]
                
                if not ocean_match.empty:
                    matches.append(ocean_match)
                    continue

                # Continent inside alias
                continent_match = world[world["continent"].str.lower() == subregion.lower()]
                
                if not continent_match.empty:
                    matches.append(continent_match)
                    continue

                # Country inside alias
                country_match = world[world["admin"].str.lower() == subregion.lower()]
                
                if not country_match.empty:
                    matches.append(country_match)
            continue

        # --- Continent ---
        continent_match = world[world["continent"].str.lower() == region]
        
        if not continent_match.empty:
            matches.append(continent_match)
            continue

        # --- Country ---
        country_match = world[world["admin"].str.lower() == region]
        
        if not country_match.empty:
            matches.append(country_match)
            continue

        # --- Ocean ---
        ocean_match = oceans[oceans["name_en"].str.lower() == region]
        
        if not ocean_match.empty:
            matches.append(ocean_match)
            continue

        # --- Arctic ---
        if region == "arctic":
            arctic_box = box(-180, 66.5, 180, 90)
            arctic_gdf = gpd.GeoDataFrame(geometry=[arctic_box], crs=world.crs)
            matches.append(arctic_gdf)
            continue

        if not matches:
            return -1

    if show_map:
        fig, ax = plt.subplots(figsize=(12, 6))

        world.plot(ax=ax, color="lightgray", edgecolor="white")
        oceans.plot(ax=ax, color="lightblue", edgecolor="lightblue")

        for match in matches:
            match.plot(ax=ax, color="green", alpha=0.7)

        # Force full world extent (lon/lat)
        ax.set_xlim(-200, 200)
        ax.set_ylim(-100, 100)

        ax.set_aspect("equal", adjustable="box")
        
        ax.axis("off")
        
        # Save map to static folder
        os.makedirs("static/maps", exist_ok=True)
        map_path = "static/maps/generated_map.png"

        plt.savefig(map_path, bbox_inches="tight",pad_inches=0,dpi=150)
        plt.close(fig)

        return map_path
