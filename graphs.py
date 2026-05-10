import pandas as pd 
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("Animal_Dataset.csv") #loads in csv file into dataframe 

#################################################
################ EXTRACTING DATA ################
#################################################

##### HEIGHT #####

def extract_numeric_heights(df, column_name):
    heights = []
    bad_count = 0
    for value in df[column_name].dropna():
        val = str(value).strip()

        # Skip "Varies"
        if val.lower() == "varies":
            bad_count +=1
            continue

        # Extract all numbers (handles decimals too)
        numbers = re.findall(r"\d+\.?\d*", val)

        if not numbers:
            bad_count +=1
            continue  # skip anything weird

        numbers = [float(n) for n in numbers]

        # Case 1: range (A-B)
        if "-" in val and len(numbers) >= 2:
            avg = sum(numbers[:2]) / 2
            heights.append(avg)

        # Case 2: "Up to X"
        elif "up to" in val.lower():
            heights.append(numbers[0])
            
        # Case 3: single number
        else:
            heights.append(numbers[0])


    return heights

height_list = extract_numeric_heights(df, "Height (cm)")

def bin_heights(height_list):
    # Create bins
    bins = [(i, i+20) for i in range(0, 200, 20)]
    
    # Initialize counts
    bin_counts = {f"{low}-{high}": 0 for low, high in bins}
    bin_counts["200+"] = 0

    # Assign values to bins
    for h in height_list:
        placed = False

        for low, high in bins:
            if low <= h < high:
                bin_counts[f"{low}-{high}"] += 1
                placed = True
                break

        # If not placed, goes to 200+
        if not placed:
            bin_counts["200+"] += 1

    return bin_counts

height_bin = bin_heights(height_list)

##### WEIGHT #####

def extract_numeric_weights(df, column_name):
    weights = []
    bad_count = 0

    for value in df[column_name].dropna():
        val = str(value).strip()

        # Skip "Varies"
        if val.lower() == "varies":
            bad_count += 1
            continue

        # Remove commas (e.g., "1,400" → "1400")
        val = val.replace(",", "")

        # Extract all numbers (handles decimals)
        numbers = re.findall(r"\d+\.?\d*", val)

        if not numbers:
            bad_count += 1
            continue

        numbers = [float(n) for n in numbers]

        # Case 1: range (A-B)
        if "-" in val and len(numbers) >= 2:
            avg = (numbers[0] + numbers[1]) / 2
            weights.append(avg)

        # Case 2: "Up to X"
        elif "up to" in val.lower():
            weights.append(numbers[0])

        # Case 3: single number
        elif len(numbers) == 1:
            weights.append(numbers[0])

        else:
            bad_count += 1

    return weights, bad_count

weight_list, bad_count_weight = extract_numeric_weights(df, "Weight (kg)")

def weight_bins(weight_list):
    # Create bins: 0–20, 20–40, ..., 180–200
    bins = [(i, i+20) for i in range(0, 200, 20)]
    
    # Initialize counts
    bin_counts = {f"{low}-{high}": 0 for low, high in bins}
    bin_counts["200+"] = 0

    # Assign weights to bins
    for w in weight_list:
        placed = False

        for low, high in bins:
            if low <= w < high:
                bin_counts[f"{low}-{high}"] += 1
                placed = True
                break

        # If not placed → 200+
        if not placed:
            bin_counts["200+"] += 1

    return bin_counts

weight_bins = weight_bins(weight_list)


##### LIFESPAN (YEARS) #####

def extract_lifespan_values(df, column_name):
    lifespans = []
    bad_count = 0

    for value in df[column_name].dropna():
        val = str(value).strip().lower()

        # Skip "Varies"
        if val == "varies":
            bad_count += 1
            continue

        # Handle "60+" → treat as 60
        if "+" in val:
            numbers = re.findall(r"\d+\.?\d*", val)
            if numbers:
                lifespans.append(float(numbers[0]))
            else:
                bad_count += 1
            continue

        # Remove words like "days", "years"
        val = re.sub(r"[a-zA-Z]+", "", val).strip()

        # Extract numbers
        numbers = re.findall(r"\d+\.?\d*", val)

        if not numbers:
            bad_count += 1
            continue

        numbers = [float(n) for n in numbers]

        # Case 1: range (A-B)
        if "-" in val and len(numbers) >= 2:
            avg = (numbers[0] + numbers[1]) / 2
            lifespans.append(avg)

        # Case 2: "Up to X"
        elif "up to" in value.lower():
            lifespans.append(numbers[0])

        # Case 3: single number
        elif len(numbers) == 1:
            lifespans.append(numbers[0])

        else:
            bad_count += 1

    return lifespans, bad_count

lifespan_list, bad_count_lifespan = extract_lifespan_values(df, "Lifespan (years)")

def lifespan_bins(lifespan_list):
    # Create bins: 0–10, 10–20, ..., 90–100
    bins = [(i, i+10) for i in range(0, 100, 10)]
    
    # Initialize counts
    bin_counts = {f"{low}-{high}": 0 for low, high in bins}
    bin_counts["100+"] = 0

    # Assign values to bins
    for l in lifespan_list:
        placed = False

        for low, high in bins:
            if low <= l < high:
                bin_counts[f"{low}-{high}"] += 1
                placed = True
                break

        # If not placed → 100+
        if not placed:
            bin_counts["100+"] += 1

    return bin_counts

lifespan_bins = lifespan_bins(lifespan_list)


##### AVERAGE SPEED (KM/H) #####

def extract_avg_speeds(df, column_name):
    speeds = []
    bad_count = 0

    for value in df[column_name].dropna():
        val = str(value).strip().lower()

        # Skip invalid categories
        if val in ["varies", "not applicable"]:
            bad_count += 1
            continue

        # Extract numbers
        numbers = re.findall(r"\d+\.?\d*", val)

        if not numbers:
            bad_count += 1
            continue

        numbers = [float(n) for n in numbers]

        # Case 1: range (A-B)
        if "-" in val and len(numbers) >= 2:
            avg = (numbers[0] + numbers[1]) / 2
            speeds.append(avg)

        # Case 2: single number
        elif len(numbers) == 1:
            speeds.append(numbers[0])

        else:
            bad_count += 1

    return speeds, bad_count

AvgSpeed_list, bad_count_avg_speed = extract_avg_speeds(df, "Average Speed (km/h)")

def AvgSpeed_bins(speed_list):
    # Create bins: 0–10, 10–20, ..., 90–100
    bins = [(i, i+10) for i in range(0, 100, 10)]
    
    # Initialize counts
    bin_counts = {f"{low}-{high}": 0 for low, high in bins}
    bin_counts["100+"] = 0

    # Assign speeds to bins
    for s in speed_list:
        placed = False

        for low, high in bins:
            if low <= s < high:
                bin_counts[f"{low}-{high}"] += 1
                placed = True
                break

        # If not placed → 100+
        if not placed:
            bin_counts["100+"] += 1

    return bin_counts

AvgSpeed_bins = AvgSpeed_bins(AvgSpeed_list)

##### TOP SPEED (KM/H) #####

def extract_top_speeds(df, column_name):
    speeds = []
    bad_count = 0

    for value in df[column_name].dropna():
        val = str(value).strip().lower()

        # Skip invalid entries
        if val in ["varies", "not applicable"]:
            bad_count += 1
            continue

        # Extract numbers
        numbers = re.findall(r"\d+\.?\d*", val)

        if not numbers:
            bad_count += 1
            continue

        numbers = [float(n) for n in numbers]

        # Case 1: range (A-B)
        if "-" in val and len(numbers) >= 2:
            avg = (numbers[0] + numbers[1]) / 2
            speeds.append(avg)

        # Case 2: single number
        elif len(numbers) == 1:
            speeds.append(numbers[0])

        else:
            bad_count += 1

    return speeds, bad_count

topspeed_list, bad_count_top_speed = extract_top_speeds(df, "Top Speed (km/h)")

def topspeed_bins(top_speed_list):
    # Create bins: 0–10, 10–20, ..., 90–100
    bins = [(i, i+10) for i in range(0, 100, 10)]
    
    # Initialize counts
    bin_counts = {f"{low}-{high}": 0 for low, high in bins}
    bin_counts["100+"] = 0

    # Assign speeds to bins
    for s in top_speed_list:
        placed = False

        for low, high in bins:
            if low <= s < high:
                bin_counts[f"{low}-{high}"] += 1
                placed = True
                break

        # If not placed → 100+
        if not placed:
            bin_counts["100+"] += 1

    return bin_counts

topspeed_bins = topspeed_bins(topspeed_list)


##### GESTATION PERIOD (DAYS) #####

def extract_gestation_days(df, column_name):
    gestation_days = []
    bad_count = 0

    for value in df[column_name].dropna():
        val = str(value).strip().lower()

        # Skip invalid entries
        if val in ["varies", "not applicable"]:
            bad_count += 1
            continue

        # Extract numbers
        numbers = re.findall(r"\d+\.?\d*", val)

        if not numbers:
            bad_count += 1
            continue

        numbers = [float(n) for n in numbers]

        # Case 1: range (A-B)
        if "-" in val and len(numbers) >= 2:
            avg = (numbers[0] + numbers[1]) / 2
            gestation_days.append(avg)

        # Case 2: single number
        elif len(numbers) == 1:
            gestation_days.append(numbers[0])

        else:
            bad_count += 1

    return gestation_days, bad_count

gestation_day_list, bad_count_gestation_days = extract_gestation_days(df, "Gestation Period (days)")

def gestation_day_bins(gestation_list):
    # Create bin of 50
    bins = [(i, i+50) for i in range(0, 300, 50)]
    
    # Initialize counts
    bin_counts = {f"{low}-{high}": 0 for low, high in bins}
    bin_counts["300+"] = 0

    # Assign values to bins
    for g in gestation_list:
        placed = False

        for low, high in bins:
            if low <= g < high:
                bin_counts[f"{low}-{high}"] += 1
                placed = True
                break

        # If not placed → 300+
        if not placed:
            bin_counts["300+"] += 1

    return bin_counts

gestation_day_bins = gestation_day_bins(gestation_day_list)


##### OFFSPRING PER BIRTH #####

def extract_offspring_per_birth(df, column_name):
    offspring_list = []
    bad_count = 0

    for value in df[column_name].dropna():
        val = str(value).strip().lower()

        # Skip invalid entries
        if val in ["varies", "not applicable"]:
            bad_count += 1
            continue

        # Remove commas (e.g., "200,000" → "200000")
        val = val.replace(",", "")

        # Extract numbers
        numbers = re.findall(r"\d+\.?\d*", val)

        if not numbers:
            bad_count += 1
            continue

        numbers = [float(n) for n in numbers]

        # Case 1: range (A-B)
        if "-" in val and len(numbers) >= 2:
            avg = (numbers[0] + numbers[1]) / 2
            offspring_list.append(avg)

        # Case 2: "Up to X"
        elif "up to" in val:
            offspring_list.append(numbers[0])

        # Case 3: single number
        elif len(numbers) == 1:
            offspring_list.append(numbers[0])

        else:
            bad_count += 1

    return offspring_list, bad_count

offspring_per_birth_list, bad_count_offspring_per_birth = extract_offspring_per_birth(df, "Offspring per Birth")

def offspring_per_birth_bins(offspring_list):
    # Initialize bins
    bin_counts = {
        "1": 0,
        "2-10": 0,
        "11-100": 0,
        "101-1000": 0,
        "1001-10000": 0,
        "10000+": 0
    }

    for o in offspring_list:
        if o == 1:
            bin_counts["1"] += 1
        elif 2 <= o <= 10:
            bin_counts["2-10"] += 1
        elif 11 <= o <= 100:
            bin_counts["11-100"] += 1
        elif 101 <= o <= 1000:
            bin_counts["101-1000"] += 1
        elif 1001 <= o <= 10000:
            bin_counts["1001-10000"] += 1
        else:
            bin_counts["10000+"] += 1

    return bin_counts

offspring_per_birth_bins = offspring_per_birth_bins(offspring_per_birth_list)

##### DIET #####

def count_diets(df, column_name):
    diet_counter = Counter()

    for value in df[column_name].dropna():
        diets = [d.strip() for d in str(value).split(",")]

        for diet in diets:
            if diet and diet != "Varies":
                diet_counter[diet] += 1

    return diet_counter

diet_bins = count_diets(df, "Diet")

##### CONSERVATION STATUS #####

conservation_status_bins = df["Conservation Status"].value_counts().to_dict()

##### SOCIAL STRUCTURE #####
social_structure_bins = df["Social Structure"].value_counts().to_dict()


###########################################
################ PLOTTING #################
###########################################


##### BAR CHART PLOTTING #####
def plot_bar(data_dict, title, xlabel, ylabel):
    keys = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure()
    plt.bar(keys, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    filepath = "static/images/temp_graph.png"
    plt.savefig(filepath)
    plt.close()
    return filepath
    
#Ex: plot_bar(height_bin, "Animal Height Distribution", "Height Range", "Count")

##### PIE CHART PLOTTING #####
def plot_pie(data_dict, title):
    
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())

    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    
    filepath = "static/images/temp_graph1.png"
    plt.savefig(filepath)
    plt.close()
    return filepath
    
#Ex: plot_pie(diet_bins, "Diet Distribution")



##### SCATTER PLOT PLOTING #####

#Ordering the non-numerical bins

diet_categories = ["Herbivore","Omnivore","Carnivore","Insectivore","Piscivore",
                    "Scavenger","Filter Feeder", "Nectar"]

conservation_status_categories = ["Least Concern","Near Threatened", "Vulnerable",
    "Endangered", "Critically Endangered", "Extinct"
    "Near Threatened", "Not Applicable", "Varies" ]

social_structure_categories = ["Solitary", "Group-based", "Social groups"]


def plot_mixed_scatter(df, col1, col2,
                        diet_categories,
                        conservation_status_categories,
                        social_structure_categories,
                        title=""):

    # ---------- helper: clean numeric ----------
    def clean_value(val):
        if isinstance(val, str):
            val_lower = val.lower()
            if "varies" in val_lower or "not applicable" in val_lower:
                return None
            
            # up to X
            match_up_to = re.match(r"up to (\d+\.?\d*)", val_lower)
            if match_up_to:
                return float(match_up_to.group(1)) / 2
            
            # range X-Y
            match_range = re.match(r"(\d+\.?\d*)\s*-\s*(\d+\.?\d*)", val_lower)
            if match_range:
                return (float(match_range.group(1)) + float(match_range.group(2))) / 2
            
            # single number
            try:
                return float(val)
            except:
                return None
        
        elif isinstance(val, (int, float)):
            return float(val)
        
        return None

    # ---------- define categorical columns ----------
    category_maps = {
        "Diet": diet_categories,
        "Conservation Status": conservation_status_categories,
        "Social Structure": social_structure_categories
    }

    is_cat1 = col1 in category_maps
    is_cat2 = col2 in category_maps

    # ---------- create mappings if categorical ----------
    if is_cat1:
        x_map = {cat: i for i, cat in enumerate(category_maps[col1])}
    if is_cat2:
        y_map = {cat: i for i, cat in enumerate(category_maps[col2])}

    x_vals = []
    y_vals = []

    # ---------- extract + clean ----------
    for v1, v2 in zip(df[col1], df[col2]):

        # handle categorical
        if is_cat1:
            if v1 not in x_map:
                continue
            x_val = x_map[v1]
        else:
            x_val = clean_value(v1)

        if is_cat2:
            if v2 not in y_map:
                continue
            y_val = y_map[v2]
        else:
            y_val = clean_value(v2)

        if x_val is not None and y_val is not None:
            x_vals.append(x_val)
            y_vals.append(y_val)

    # ---------- plotting ----------
    plt.figure(figsize=(8,6))
    plt.scatter(x_vals, y_vals, alpha=0.6)

    # ---------- apply categorical labels ----------
    if is_cat1:
        plt.xticks(range(len(category_maps[col1])), category_maps[col1], rotation=45)
    if is_cat2:
        plt.yticks(range(len(category_maps[col2])), category_maps[col2])

    # ---------- log scale variables ----------
    log_vars = [
        "Weight (kg)",
        "Gestation Period (days)",
        "Height (cm)",
        "Lifespan (years)",
        "Offspring per Birth"
    ]

    if not is_cat1 and col1 in log_vars:
        plt.xscale("log")
    if not is_cat2 and col2 in log_vars:
        plt.yscale("log")

    # ---------- labels ----------
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.title(title)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    
    filepath = "static/images/temp_graph2.png"
    plt.savefig(filepath)
    plt.close()
    return filepath


# var1 = "Lifespan (years)"
# var2 = "Offspring per Birth"
# Ex: plot_mixed_scatter(df, var1, var2, diet_categories, conservation_status_categories, social_structure_categories, title="Weight vs Speed")


##### HEAT MAP PLOTTING #####


# PREDEFINED BINS
numerical_bins = {
    "height (cm)": height_bin,
    "weight (kg)": weight_bins,
    "lifespan (years)": lifespan_bins,
    "average speed (km/h)": AvgSpeed_bins,
    "top speed (km/h)": topspeed_bins,
    "gestation period (days)": gestation_day_bins,
    "offspring per birth": offspring_per_birth_bins
}

categorical_bins = {
    "diet": diet_categories,
    "conservation status": conservation_status_categories,
    "social structure": social_structure_categories
}

# CLEAN NUMERICAL VALUES
def clean_value(val):
    if isinstance(val, str):
        val_lower = val.lower()
        if "varies" in val_lower or "not applicable" in val_lower:
            return None
        
        match_up_to = re.match(r"up to (\d+\.?\d*)", val_lower)
        if match_up_to:
            return float(match_up_to.group(1)) / 2
        
        match_range = re.match(r"(\d+\.?\d*)\s*-\s*(\d+\.?\d*)", val_lower)
        if match_range:
            return (float(match_range.group(1)) + float(match_range.group(2))) / 2
        
        try:
            return float(val)
        except:
            return None

    elif isinstance(val, (int, float)):
        return float(val)

    return None


# BIN DICT → EDGES
def get_bin_edges(bin_dict):
    edges = []

    for key in bin_dict.keys():
        key = key.strip()

        # Case 1: "X-Y"
        if "-" in key:
            try:
                low, high = key.split("-")
                edges.append(float(low))
                edges.append(float(high))
            except:
                continue

        # Case 2: "X+"
        elif "+" in key:
            try:
                edges.append(float(key.replace("+", "")))
            except:
                continue

        # Case 3: single number "X"
        else:
            try:
                val = float(key)
                edges.append(val)
                edges.append(val + 1)  # small range so it forms a bin
            except:
                continue

    edges = sorted(list(set(edges)))

    return edges


# HEATMAP FUNCTION
def plot_heatmap2(df, var1, var2, title="Heatmap", cmap="RdYlGn_r", type = ""):

    v1_key = var1.lower()
    v2_key = var2.lower()

    x_bin_dict = numerical_bins.get(v1_key)
    y_bin_dict = numerical_bins.get(v2_key)

    x_is_num = x_bin_dict is not None
    y_is_num = y_bin_dict is not None

    clean_x = []
    clean_y = []

    # =========================
    # CLEAN DATA
    # =========================
    for v1, v2 in zip(df[var1], df[var2]):
        cx = clean_value(v1) if x_is_num else v1
        cy = clean_value(v2) if y_is_num else v2

        if cx is not None and cy is not None:
            clean_x.append(cx)
            clean_y.append(cy)

    # =========================
    # CASE 1: NUM + NUM
    # =========================
    if x_is_num and y_is_num:

        x_edges = get_bin_edges(x_bin_dict)
        y_edges = get_bin_edges(y_bin_dict)

        heatmap, _, _ = np.histogram2d(clean_x, clean_y, bins=[x_edges, y_edges])

        x_labels = list(x_bin_dict.keys())
        y_labels = list(y_bin_dict.keys())

    # =========================
    # CASE 2: CAT + NUM
    # =========================
    elif not x_is_num and y_is_num:

        y_edges = get_bin_edges(y_bin_dict)
        y_labels = list(y_bin_dict.keys())[:len(y_edges)-1]

        x_categories = categorical_bins.get(v1_key, [])

        heatmap = np.zeros((len(y_edges) - 1, len(x_categories)))

        for x, y in zip(clean_x, clean_y):

            # find y bin
            for i in range(len(y_edges) - 1):
                if y_edges[i] <= y < y_edges[i + 1]:
                    row = i
                    break
            else:
                continue

            # split multi-category
            x_parts = [i.strip() for i in str(x).split(",")]

            for xp in x_parts:
                if xp in x_categories:
                    col = x_categories.index(xp)
                    heatmap[row][col] += 1

        x_labels = x_categories

    # =========================
    # CASE 3: NUM + CAT
    # =========================
    elif x_is_num and not y_is_num:

        x_edges = get_bin_edges(x_bin_dict)
        x_labels = list(x_bin_dict.keys())

        y_categories = categorical_bins.get(v2_key, [])

        heatmap = np.zeros((len(y_categories), len(x_edges) - 1))

        for x, y in zip(clean_x, clean_y):

            # find x bin
            for i in range(len(x_edges) - 1):
                if x_edges[i] <= x < x_edges[i + 1]:
                    col = i
                    break
            else:
                continue

            # split multi-category
            y_parts = [i.strip() for i in str(y).split(",")]

            for yp in y_parts:
                if yp in y_categories:
                    row = y_categories.index(yp)
                    heatmap[row][col] += 1

        y_labels = y_categories

    # =========================
    # CASE 4: CAT + CAT
    # =========================
    else:

        x_categories = categorical_bins.get(v1_key, [])
        y_categories = categorical_bins.get(v2_key, [])

        heatmap = np.zeros((len(y_categories), len(x_categories)))

        for x, y in zip(clean_x, clean_y):

            x_parts = [i.strip() for i in str(x).split(",")]
            y_parts = [i.strip() for i in str(y).split(",")]

            for xp in x_parts:
                for yp in y_parts:
                    if xp in x_categories and yp in y_categories:
                        row = y_categories.index(yp)
                        col = x_categories.index(xp)
                        heatmap[row][col] += 1

        x_labels = x_categories
        y_labels = y_categories

    # =========================
    # PLOT
    # =========================
    plt.figure(figsize=(9,6))
    plt.imshow(
            heatmap,
            origin='lower',
            aspect='auto',
            cmap=cmap,
            interpolation= type   
        )
    plt.colorbar(label="Count")

    plt.xticks(np.arange(len(x_labels)), x_labels, rotation=45)
    plt.yticks(np.arange(len(y_labels)), y_labels)

    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.title(title)

    plt.tight_layout()
    
    filepath = "static/images/temp_graph3.png"
    plt.savefig(filepath)
    plt.close()
    return filepath


#v1 = "Diet"
#v2 = "Lifespan (years)"
#plot_heatmap2(df, v1, v2, title="", type = "bilinear")    
        #type should either be bilinear or nearest or gaussian
        
