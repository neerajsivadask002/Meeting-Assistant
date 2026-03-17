# Meeting-Assistant
To make your GitHub repository look professional, it’s best to use a combination of standard Markdown and "Copy-to-Clipboard" code blocks. 

Here is the exact code for your **README.md**. You can copy the entire block below and paste it directly into your file.

```markdown
# 📝 AI Meeting Assistant

Transform raw meeting notes into structured summaries and actionable tasks using Google's latest Gemini models.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/meeting-assistant.git](https://github.com/YOUR_USERNAME/meeting-assistant.git)
cd meeting-assistant
```

### 2. Install Dependencies
Ensure you have Python 3.9+ installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Get an API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Create a free API Key.
3. Keep this key ready to paste into the app sidebar.

### 4. Launch the App
```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack & Model Specs (2026)

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit |
| **LLM Engine** | Gemini 3.1 Flash-Lite |
| **Data Schemas** | Pydantic |
| **API Version** | v1beta |

> **Note:** This app is optimized for the **Flash-Lite** model to provide the highest possible request quota (1,000 RPD) on the Google AI Free Tier.

---

## 📂 Project Structure

* `app.py`: Core application logic and Gemini API integration.
* `requirements.txt`: Python package list (Streamlit, Pydantic, Google-GenerativeAI).
* `README.md`: Setup instructions and project overview.

---

## 🔧 Troubleshooting

**Error: 429 Quota Exceeded**
This means you've hit the per-minute limit. The app is configured to handle large notes, but if you see this, wait **20-30 seconds** and try again.

**Error: 404 Model Not Found**
Ensure you are using the correct model string in `app.py`: `gemini-3.1-flash-lite-preview`.

---
*Developed for efficient project management and automated documentation.*
```

### **One Final Step for Git Safety**
Since you are working with API keys, you should create a file named `.gitignore` in your folder so you don't accidentally upload your personal keys or environment files. 

**Create a file named `.gitignore` and paste this inside:**
```text
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/

# Streamlit
.streamlit/config.toml

# Environment/Keys
.env
.secrets
```
