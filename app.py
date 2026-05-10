from flask import Flask, render_template, request, session
from image_utils import get_animal_image
from map_gen import highlight_region
from graphs import plot_bar, plot_pie, plot_mixed_scatter, plot_heatmap2, diet_categories, conservation_status_categories, social_structure_categories, diet_bins, numerical_bins, conservation_status_bins, social_structure_bins
import pandas as pd
import math

app = Flask(__name__)       #create web app project
app.secret_key = "mcqueen"  # for graph generation

df = pd.read_csv("Animal_Dataset.csv")     #read in data

def search_animal(animal):
    
    result = df[df["Animal"].str.lower() == animal.lower()]     #search for animal
    if result.empty:
        return None
    
    return result.iloc[0].to_dict()     #return result as dictionary


def list_all_columns(num_cols=6):       #returns list of animals in 5 columns
    animals = sorted(df["Animal"].dropna().tolist())        #sort lit of animals
    total = len(animals)
    rows_per_col = math.ceil(total / num_cols)      #find # of rows per col

    columns = []        
    for i in range(num_cols):       #fill cols that will be returned
        start = i * rows_per_col
        end = start + rows_per_col
        columns.append(animals[start:end])

    return columns

def search_suggest(user_input, max_results=7):    #returns search suggestions based on user input
    if not user_input:      #no input
        return []

    user_input = user_input.lower().strip()
    animal_names = df["Animal"].str.lower()
    
    #animals that START with the input string
    starts_with = df[animal_names.str.startswith(user_input, na=False)]

    #animals that don't start with input string but contain it
    contains = df[animal_names.str.contains(user_input, na=False) &
            ~animal_names.str.startswith(user_input, na=False)]

    # results prioritize starts_with
    results = pd.concat([starts_with, contains])

    # Return up to max results animal names
    return results["Animal"].head(max_results).tolist()


def create_foodchain():     #create food chain
    food_chains = {}

    for _, row in df.iterrows():
        animal = row["Animal"].strip().lower()

        # Process food column
        foods = row["Food"]
        if isinstance(foods, str):
            foods = foods.strip("()")
            foods = [f.strip().lower() for f in foods.split(",") if f.strip()]
        else:
            foods = []

        # Process predators column
        predators = row["Predators"]
        if isinstance(predators, str):
            if predators.strip().lower() == "not applicable":
                predators = []
            else:
                predators = [p.strip().lower()
                    for p in predators.split(",")
                    if p.strip() and p.strip().lower() != "not applicable"]
        else:
            predators = []

        food_chains[animal] = {
            "food": foods,
            "predators": predators
        }
    
    return food_chains

food_chains = create_foodchain()     #create food chain data structure when app 1st runs
    
#FLASK ROUTES:

@app.route("/", methods=["GET", "POST"])        #Home route, accepts "GET" & "POST" requests
def index():
    animal_data = None
    searched = False
    image_url = None
    map_url = None

    if request.method == "POST":        #POST: requests for search function
        searched = True
        animal_name = request.form["animal"]        #gets input for search
        animal_data = search_animal(animal_name)    #searches for animal input
        image_url = get_animal_image(animal_data["Animal"])
        map_url = highlight_region(animal_data["Countries Found"])

    return render_template( "index.html", animal=animal_data, searched=searched,
                        image_url=image_url, map_url=map_url )   #sends data to index.html



@app.route("/about")        #route to About.html (another page)
def about():
    return render_template("about.html")     


@app.route("/List-of-Animals")      #route to List-of-Animals.html
def list_of_animals():
    animal_columns = list_all_columns()
    return render_template("List-of-Animals.html", animal_columns=animal_columns)


@app.route("/food-chains", methods=["GET", "POST"])     #route to food-chains.html
def Food_Chains():

    result = None
    searched = False

    if request.method == "POST":
        searched = True
        animal_name = request.form["animal"].strip().lower()

        if animal_name in food_chains:

            foods = food_chains[animal_name]["food"]
            predators = food_chains[animal_name]["predators"]

            # create food image cards
            food_cards = []
            for food in foods:
                food_cards.append({"name": food,
                                    "image": get_animal_image(food)})

            # create predator image cards
            predator_cards = []
            for predator in predators:
                predator_cards.append({"name": predator,
                        "image": get_animal_image(predator)})

            result = {"animal": animal_name, "animal_image": get_animal_image(animal_name),
                "foods": food_cards, "predators": predator_cards }

    return render_template("food-chains.html", result=result, searched=searched)


@app.route("/graphs", methods=["GET", "POST"])  #route to graphs.html
def graphs():

    graph_type = None

    if request.method == "POST":
        graph_type = request.form.get("graph_type")
        var1 = request.form.get("var1")
        var2 = request.form.get("var2")
        map_type = request.form.get("map_type")

        if graph_type == "bar":
            session["bar_var1"] = var1
            categorical_counts = {
                "diet": diet_bins,
                "conservation status": conservation_status_bins,
                "social structure": social_structure_bins
            }
            data = numerical_bins.get(var1.lower()) or categorical_counts.get(var1.lower())
            if data:
                session["bar_url"] = plot_bar(data, f"{var1} Distribution", var1, "Count")

        elif graph_type == "pie":
            session["pie_var1"] = var1
            categorical_counts = {
                "diet": diet_bins,
                "conservation status": conservation_status_bins,
                "social structure": social_structure_bins
            }
            data = numerical_bins.get(var1.lower()) or categorical_counts.get(var1.lower())
            if data:
                session["pie_url"] = plot_pie(data, f"{var1} Distribution")

        elif graph_type == "scatter":
            session["scatter_var1"] = var1
            session["scatter_var2"] = var2
            session["scatter_url"] = plot_mixed_scatter(df, var1, var2,
                diet_categories, conservation_status_categories,
                social_structure_categories, title=f"{var1} vs {var2}")

        elif graph_type == "heatmap":
            session["heatmap_var1"] = var1
            session["heatmap_var2"] = var2
            session["heatmap_map_type"] = map_type
            session["heatmap_url"] = plot_heatmap2(df, var1, var2,
                title=f"{var1} vs {var2}", type=map_type)

    return render_template("graphs.html",
        bar_url=session.get("bar_url"),
        bar_var1=session.get("bar_var1"),

        pie_url=session.get("pie_url"),
        pie_var1=session.get("pie_var1"),

        scatter_url=session.get("scatter_url"),
        scatter_var1=session.get("scatter_var1"),
        scatter_var2=session.get("scatter_var2"),

        heatmap_url=session.get("heatmap_url"),
        heatmap_var1=session.get("heatmap_var1"),
        heatmap_var2=session.get("heatmap_var2"),
        heatmap_map_type=session.get("heatmap_type")
    )


@app.route("/contribute")       #route to contribute.html
def contribute():
    return render_template("contribute.html")   

from flask import jsonify, request      

@app.route("/suggest")      #Route for search_suggest (for javascript)
def suggest():
    query = request.args.get("q", "")       #read string input
    suggestions = search_suggest(query)     #put input into search_suggest

    return jsonify(suggestions)         #returns search_suggest output for javascript to use

if __name__ == "__main__":
    app.run(debug=True)