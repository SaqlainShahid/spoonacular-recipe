import streamlit as st
import requests
from PIL import Image
import io
import os
import json
from dotenv import load_dotenv
from fpdf import FPDF
import base64
import random

# Load API keys
load_dotenv()
CLARIFAI_API_KEY = os.getenv("CLARIFAI_API_KEY")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

st.set_page_config(page_title="AI Recipe Generator", layout="centered")
st.title("🍲 Ingredient Image to Recipe Generator")

uploaded_file = st.file_uploader("Upload an ingredient image", type=["jpg", "jpeg", "png"])

def clarifai_predict(image_base64):
    url = "https://api.clarifai.com/v2/models/food-item-recognition/outputs"
    headers = {
        "Authorization": f"Key {CLARIFAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": [
            {
                "data": {
                    "image": {
                        "base64": image_base64
                    }
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        st.error(f"Clarifai API error: {response.status_code} {response.text}")
        return []
    outputs = response.json()["outputs"][0]["data"].get("concepts", [])
    return [concept['name'] for concept in outputs if concept['value'] > 0.85]

def get_recipe_information(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": SPOONACULAR_API_KEY
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json()
    return None

def create_recipe_pdf(recipe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=recipe["title"], ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Ingredients:", ln=True)
    pdf.set_font("Arial", size=12)
    for ing in recipe.get("extendedIngredients", []):
        desc = ing.get('originalString') or ing.get('original') or ing.get('name') or "Ingredient details missing"
        pdf.multi_cell(0, 10, f"- {desc}")

    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Instructions:", ln=True)
    pdf.set_font("Arial", size=12)
    if recipe.get("instructions"):
        pdf.multi_cell(0, 10, recipe["instructions"])
    else:
        pdf.multi_cell(0, 10, "No instructions available.")

    pdf_path = "/mnt/data/recipe.pdf"
    pdf.output(pdf_path)
    return pdf_path

def save_favorite_recipe(recipe):
    fav_path = "/mnt/data/favorites.json"
    if os.path.exists(fav_path):
        with open(fav_path, "r") as f:
            favorites = json.load(f)
    else:
        favorites = []

    if recipe["id"] not in [r["id"] for r in favorites]:
        favorites.append(recipe)
        with open(fav_path, "w") as f:
            json.dump(favorites, f, indent=2)
        return True
    return False

def generate_ai_reason(ingredients, title):
    reason = f"This recipe is a great match for your ingredients: {', '.join(ingredients)}.\n"
    reason += f"'{title}' brings out the flavor of {random.choice(ingredients)} perfectly and is easy to cook with everyday items!"
    return reason

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    with st.spinner("🔍 Detecting ingredients using Clarifai..."):
        ingredients = clarifai_predict(img_base64)

    if ingredients:
        st.success("✅ Ingredients detected!")
        st.write(", ".join(ingredients))

        with st.spinner("📡 Fetching recipes..."):
            params = {
                "apiKey": SPOONACULAR_API_KEY,
                "ingredients": ",".join(ingredients),
                "number": 3,
                "ranking": 1
            }
            res = requests.get("https://api.spoonacular.com/recipes/findByIngredients", params=params)

            if res.status_code == 200:
                recipes = res.json()
                if recipes:
                    for recipe_summary in recipes:
                        recipe = get_recipe_information(recipe_summary['id'])
                        if recipe:
                            st.markdown("---")
                            st.subheader(f"🍽️ {recipe['title']}")
                            st.image(recipe['image'], use_container_width=True)

                            st.markdown("### 🧂 Ingredients:")
                            for ing in recipe.get('extendedIngredients', []):
                                desc = ing.get('originalString') or ing.get('original') or ing.get('name') or "Unknown ingredient"
                                st.write(f"- {desc}")

                            st.markdown("### 📝 Instructions:")
                            if recipe.get("instructions"):
                                st.markdown(recipe["instructions"], unsafe_allow_html=True)
                            else:
                                st.write("No instructions provided.")

                            with st.expander("💡 Why this recipe?"):
                                st.write(generate_ai_reason(ingredients, recipe['title']))

                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(f"📄 Download PDF - {recipe['id']}", key=f"pdf_{recipe['id']}"):
                                    pdf_path = create_recipe_pdf(recipe)
                                    with open(pdf_path, "rb") as f:
                                        st.download_button(
                                            label="Download PDF",
                                            data=f,
                                            file_name="recipe.pdf",
                                            mime="application/pdf"
                                        )
                            with col2:
                                if st.button(f"⭐ Save Favorite - {recipe['id']}", key=f"fav_{recipe['id']}"):
                                    if save_favorite_recipe(recipe):
                                        st.success("Saved to favorites!")
                                    else:
                                        st.info("Already in favorites.")
                else:
                    st.warning("No recipes found.")
            else:
                st.error(f"Spoonacular error: {res.status_code}")
    else:
        st.warning("No ingredients detected.")

