from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data/netflix_data.csv")
df = df[df["Category"] != "Romance"]

user_activity = {"Language": [], "Category": []}

@app.route("/", methods=["GET", "POST"])
def index():
    categories = df["Category"].unique()
    languages = df["Language"].unique()
    top_movies = []

    if request.method == "POST":
        category = request.form.get("category")
        language = request.form.get("language")
        filtered = df[(df["Category"] == category) & (df["Language"] == language)]
        top_movies = filtered.head(5).to_dict(orient="records")
        if top_movies:
            user_activity["Language"].extend([m['Language'] for m in top_movies])
            user_activity["Category"].extend([m['Category'] for m in top_movies])

    # Always include all categories for chart
    all_categories = df['Category'].unique()
    cat_counts = {cat: user_activity["Category"].count(cat) for cat in all_categories}
    lang_counts = {lang: user_activity["Language"].count(lang) for lang in df['Language'].unique()}

    return render_template(
        "index.html",
        categories=categories,
        languages=languages,
        top_movies=top_movies,
        lang_counts=lang_counts,
        cat_counts=cat_counts
    )

if __name__ == "__main__":
    app.run(debug=True)
