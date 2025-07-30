<p align="center">
  <img src="https://img.shields.io/badge/Spoonacular%20Recipe%20App-🍽️-brightgreen?style=for-the-badge" alt="Spoonacular Recipe App">
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#technologies">Technologies</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

---

## 🚀 Spoonacular Recipe App

A **Streamlit web app** (Python) that lets users **upload a food image** or **enter a search term** to instantly receive a recipe—with ingredients, instructions, nutrition details, and an option to **export as PDF**.

---

## ⭐ Badges

[![Python](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python)](#)  
[![Streamlit](https://img.shields.io/badge/streamlit‑app‑stable-orange?style=for-the-badge&logo=streamlit)](#)  
[![License: MIT](https://img.shields.io/github/license/SaqlainShahid/spoonacular-recipe?style=for-the-badge)](#)  
[![Stars on GitHub](https://img.shields.io/github/stars/SaqlainShahid/spoonacular-recipe?style=for-the-badge&logo=github)](#)

---

## 🧩 Features

- **📷 Image‑to‑Recipe Matching** — Upload a food photo to fetch relevant recipe results  
- **🔎 Keyword Search** — Discover recipes by dish names or ingredients  
- **📋 Clean Recipe View** — Includes recipe image, ingredient list, step‑by‑step instructions, and nutrition info  
- **📥 PDF Export** — Download chosen recipes as formatted printable PDFs  
- **🔐 Secure API Integration** — Store API keys in `.env` to keep credentials safe

---

## 🧱 Technologies

- **Frontend/UI**: Streamlit  
- **Backend Language**: Python  
- **Image Handling**: Pillow  
- **PDF Generation**: FPDF  
- **API Service**: Spoonacular Food & Nutrition API  
- **Secrets Management**: python‑dotenv

---

## 🧪 Installation

```bash
git clone https://github.com/SaqlainShahid/spoonacular-recipe.git
cd spoonacular-recipe
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
SPOONACULAR_API_KEY=your_api_key_here
```

Launch the app:

```bash
streamlit run app.py
```

---

## 📂 Usage

1. Open the Streamlit interface.  
2. Choose to **upload an image** or **type a keyword**.  
3. View matching recipes with images, ingredient lists, instructions, and nutrition facts.  
4. Click **Export to PDF** for a printable version.  
5. Try different images or searches anytime.

---

## 📝 Why It Stands Out

- Dual input modes: **Image** and **Text** searches  
- Powered by Spoonacular’s **extensive recipe database**  
- Simple and responsive **Streamlit layout**  
- Generates **professional-looking PDFs**

---

## ⭐ Recommended README Best Practices

- Center titles or logos for visual impact  
- Place badges at the top for a quick snapshot of your project  
- Add a **Table of Contents** for easy navigation in longer files  
- Keep it clean, concise, and friendly—use emojis for readability  

---

## 🤝 Contributing

Want to help? ✅  
1. Fork the repository  
2. Create a branch: `feature/your-feature`  
3. Make your enhancements (add caching, richer UI, new input types…)  
4. Commit changes & push: `git push origin feature/your-feature`  
5. Submit a Pull Request to `main`

Let’s build something great together!

---

## 📜 License

This project is licensed under **MIT License**.

---

Happy cooking and coding! 🍳 | Questions or feedback? Please raise an issue or DM on GitHub.
