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

# Configure page
st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with background image
st.markdown(f"""
<style>
   .stApp {{
        background-image: linear-gradient(rgba(71, 77, 86, 0.85), rgba(71, 77, 86, 0.85)), 
                          url("https://images.unsplash.com/photo-1490645935967-10de6ba17061?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1953&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    .main-container {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }}
    .st-emotion-cache-18ni7ap {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    .sidebar .sidebar-content {{
        background-color: rgba(255, 255, 255, 0.95);
    }}
    .stButton>button {{
        background-color: #ff6b6b;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        transition: all 0.3s;
        border: none;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: #ff5252;
        transform: scale(1.05);
        box-shadow: 0 2px 10px rgba(255,107,107,0.4);
    }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: #333;
        font-family: 'Arial Rounded MT Bold', sans-serif;
    }}
    .stMarkdown h1 {{
        text-align: center;
        color: #ff6b6b;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }}
    .recipe-card {{
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        border: 1px solid #eee;
    }}
    .recipe-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    .ingredient-item {{
        padding: 8px 0;
        border-bottom: 1px dashed #eee;
    }}
    .footer {{
        text-align: center;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        color: #666;
        font-size: 0.9em;
    }}
    .file-uploader {{
        background-color: rgba(255,255,255,0.8);
        border-radius: 10px;
        padding: 20px;
    }}
    .tab-content {{
        padding: 15px 0;
    }}
    .recipe-nav {{
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
    }}
    .recipe-nav button {{
        background-color: #ff6b6b;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-weight: bold;
        cursor: pointer;
    }}
    .recipe-nav button:hover {{
        background-color: #ff5252;
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1562923690-e274ba919781?q=80&w=1976&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)
    st.title("AI Recipe Generator")
    st.markdown("""
    *How it works:*
    1. 📸 Upload an image of ingredients
    2. 🔍 AI detects what's in your photo
    3. 👩‍🍳 Get delicious recipe suggestions!
    """)
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app uses AI to transform your ingredients into culinary masterpieces!")

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
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt=recipe["title"], ln=True, align='C')
    pdf.ln(10)
    
    # Add recipe image if available
    if recipe.get("image"):
        try:
            image_data = requests.get(recipe["image"]).content
            temp_img = io.BytesIO(image_data)
            pdf.image(temp_img, x=50, w=110)
        except:
            pass
    
    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="Ingredients:", ln=True)
    pdf.set_font("Arial", size=12)
    for ing in recipe.get("extendedIngredients", []):
        desc = ing.get('originalString') or ing.get('original') or ing.get('name') or "Ingredient details missing"
        pdf.multi_cell(0, 10, f"- {desc}")

    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="Instructions:", ln=True)
    pdf.set_font("Arial", size=12)
    if recipe.get("instructions"):
        # Clean HTML tags from instructions
        import re
        clean_instructions = re.sub('<[^<]+?>', '', recipe["instructions"])
        pdf.multi_cell(0, 10, clean_instructions)
    else:
        pdf.multi_cell(0, 10, "No instructions available.")

    # Return PDF as bytes instead of saving to file
    return pdf.output(dest='S').encode('latin-1')

def save_favorite_recipe(recipe):
    fav_path = "favorites.json"
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
    cooking_styles = ["stir-fry", "roast", "bake", "grill", "steam", "sauté"]
    adjectives = ["delicious", "mouth-watering", "nutritious", "flavorful", "quick", "easy"]
    reason = f"✨ *Why you'll love this recipe:*\n\n"
    reason += f"This {random.choice(adjectives)} {random.choice(cooking_styles)} recipe perfectly matches your ingredients: {', '.join(ingredients)}.\n\n"
    reason += f"*{title}* brings out the best in {random.choice(ingredients)} and can be prepared in under 30 minutes!"
    return reason

# Main content container
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.title("🍳 AI Recipe Generator")
    st.markdown("### Transform your ingredients into delicious meals!")
    
    # File uploader with custom styling
    uploaded_file = st.file_uploader(
        "📤 Upload an image of your ingredients", 
        type=["jpg", "jpeg", "png"],
        help="Take a photo of your fridge or pantry ingredients"
    )

    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Your Ingredients")
            image = Image.open(uploaded_file)
            st.image(image, caption="Your delicious ingredients", use_container_width=True)
            
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')

            with st.spinner("🔍 Detecting ingredients..."):
                ingredients = clarifai_predict(img_base64)

            if ingredients:
                st.success("✅ Detected ingredients!")
                st.write("")
                for ing in ingredients:
                    st.markdown(f"- 🟢 {ing}")
            else:
                st.warning("No ingredients detected. Try a clearer image of your ingredients.")

        if ingredients:
            with col2:
                st.markdown("### Recipe Suggestions")
                with st.spinner("🧑‍🍳 Finding perfect recipes for you..."):
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
                            # Initialize session state for recipe navigation
                            if 'recipe_index' not in st.session_state:
                                st.session_state.recipe_index = 0
                            
                            # Get detailed recipe information for all recipes
                            detailed_recipes = []
                            for recipe_summary in recipes:
                                recipe = get_recipe_information(recipe_summary['id'])
                                if recipe:
                                    detailed_recipes.append(recipe)
                            
                            if detailed_recipes:
                                # Recipe navigation buttons
                                st.markdown('<div class="recipe-nav">', unsafe_allow_html=True)
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    if st.button("1", key="nav_1"):
                                        st.session_state.recipe_index = 0
                                with col2:
                                    if st.button("2", key="nav_2"):
                                        st.session_state.recipe_index = 1
                                with col3:
                                    if st.button("3", key="nav_3"):
                                        st.session_state.recipe_index = 2
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Display the current recipe based on index
                                recipe = detailed_recipes[st.session_state.recipe_index]
                                with st.container():
                                    st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                                    
                                    # Recipe header with image
                                    col_img, col_title = st.columns([1, 3])
                                    with col_img:
                                        st.image(recipe['image'], width=150)
                                    with col_title:
                                        st.markdown(f"#### {recipe['title']}")
                                        st.caption(f"🕒 Ready in {recipe.get('readyInMinutes', 'N/A')} minutes | 👨‍👩‍👧‍👦 Serves {recipe.get('servings', 'N/A')}")
                                    
                                    # Why this recipe
                                    with st.expander("🤖 AI Recommendation"):
                                        st.markdown(generate_ai_reason(ingredients, recipe['title']))
                                    
                                    # Ingredients and instructions tabs
                                    tab1, tab2 = st.tabs(["🧂 Ingredients", "📝 Instructions"])
                                    
                                    with tab1:
                                        for ing in recipe.get('extendedIngredients', []):
                                            desc = ing.get('originalString') or ing.get('original') or ing.get('name') or "Unknown ingredient"
                                            st.markdown(f'<div class="ingredient-item">- {desc}</div>', unsafe_allow_html=True)
                                    
                                    with tab2:
                                        if recipe.get("instructions"):
                                            st.markdown(recipe["instructions"], unsafe_allow_html=True)
                                        else:
                                            st.warning("No instructions provided for this recipe.")
                                    
                                    # Action buttons
                                    col_dl, col_fav, _ = st.columns([2, 2, 4])
                                    with col_dl:
                                        if st.button("📄 Download PDF", key=f"pdf_{recipe['id']}"):
                                            pdf_bytes = create_recipe_pdf(recipe)
                                            st.download_button(
                                                label="⬇️ Download Now",
                                                data=pdf_bytes,
                                                file_name=f"{recipe['title']}.pdf",
                                                mime="application/pdf"
                                            )
                                    with col_fav:
                                        if st.button("⭐ Save Favorite", key=f"fav_{recipe['id']}"):
                                            if save_favorite_recipe(recipe):
                                                st.success("Saved to favorites!")
                                            else:
                                                st.info("Already in favorites")
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    st.write("")
                        else:
                            st.warning("No recipes found. Try different ingredients!")
                    else:
                        st.error(f"Error fetching recipes: {res.status_code}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">🍳 Happy cooking with AI!</div>', unsafe_allow_html=True)