
# 📧 Email Phishing Detector

A full-stack phishing email detection system built with **Python (backend)** and **React (frontend)**. It uses the Gmail API to read emails, analyze their content, and detect phishing patterns using regex, keyword analysis, and basic NLP.

---

## 🧠 Features

- ✅ Gmail OAuth 2.0 Integration
- ✅ Analyzes subject & body for phishing
- ✅ Regex-based suspicious URL detection
- ✅ Keyword analysis using dataset
- ✅ React-based UI for scanning and viewing results
- ✅ `.gitignore` and credentials protection
- ✅ Modular backend (`utils/`, `dataset/`, etc.)

---

## 📁 Project Structure

```

email-phishing-detector/
├── backend/                     # Python logic & Gmail API
│   └── credentials/            # Gmail API credentials.json (ignored)
├── phishing-detector-frontend/ # React frontend
├── dataset/                    # CSVs or keyword data
├── utils/                      # Helper Python files
├── .gitignore
├── README.md
└── LICENSE

````

---

## 🚀 How to Run the Project

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/Batman7byte/email-phishing-detector.git
cd email-phishing-detector
````

---

### 🐍 2. Backend Setup (Python)

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

---

### 🔐 3. Add Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Gmail API**
4. Configure **OAuth consent screen**:

   * Select **External**
   * Add app info
   * Add scope: `../auth/gmail.readonly`
   * Add your Gmail as test user
5. Create **OAuth Client ID**:

   * App type: **Desktop**
   * Download JSON
   * Rename to: `credentials.json`
6. Place it here:

```
backend/credentials/credentials.json
```

Make sure this folder exists.

**Python code should use:**

```python
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials/credentials.json',
    scopes=SCOPES
)
```

✅ Already ignored in `.gitignore`

---

### ▶️ 4. Run the Backend

```bash
python main.py
```

---

### 🌐 5. Frontend Setup (React)

```bash
cd phishing-detector-frontend
npm install
npm start
```

The app will run at:
`http://localhost:3000`

---

## 🔒 Security

* ✅ `credentials.json` and `token.json` are **not pushed to GitHub**
* ✅ Only `gmail.readonly` access is requested
* ✅ Use `.env` for future token handling (optional)

---

## ✨ Future Improvements

* 🤖 ML-based phishing detection (TF-IDF, Naive Bayes)
* ☁️ Cloud deployment (Render, Vercel)
* 🗂 Email quarantine or deletion support
* 📬 Notifications / Alerts UI
* 📊 Visualization of phishing stats

---

## 🙌 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss it.

---

## 📄 License

This project is licensed under the **MIT License**.
See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

* [Google Gmail API](https://developers.google.com/gmail/api)
* [React](https://react.dev/)
* [Python](https://www.python.org/)
* [NLTK](https://www.nltk.org/)

````

---

## ✅ What to Do Now

1. Create or replace your `README.md` file  
2. Paste the full content above  
3. Commit and push:

```bash
git add README.md
git commit -m "Add final full README with setup and credential guide"
git push
````
Important!!
In style.css in button section add Margin: 50x; and padding: 20px;

