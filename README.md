
# Cardiovascular Disease Predictor

An interactive web-based system that uses a Bayesian Network to predict the likelihood of cardiovascular disease based on user health data.

## 🌟 Features

- 🧠 **Bayesian Inference Engine**: Performs probabilistic reasoning using a custom-built Bayesian Network (.bn file).
- 🎛️ **Interactive Frontend**: Built with **React + Vite**, allowing users to input health metrics via a responsive interface.
- 🔗 **Backend API**: Powered by **Flask**, providing prediction results via a simple POST endpoint.
- 🔍 **Explainable Output**: Displays the predicted outcome and the associated probability.

## 🏗️ Project Structure

```
cardiovascular-disease-predictor/
│
├── backend/
│   ├── app.py              # Flask backend with prediction API
│   ├── bn_engine.py        # Bayesian inference logic
│   ├── heart_disease.bn    # Network structure and CPTs
│   └── requirements.txt    # Backend dependencies
│
├── frontend/
│   └── vite-project/       # React frontend with Vite
│       ├── App.jsx
│       ├── index.jsx
│       └── vite.config.js  # Includes API proxy config
│
└── cardio_train.csv        # (Optional) Raw dataset used to build the BN
```

## 🚀 Getting Started

### 🔧 Backend Setup (Flask)


cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py


The Flask app will start at: `http://127.0.0.1:5000`

### 🧪 API Endpoint

- **POST** `/api/predict`

**Payload Example:**
```
{
  "age_group": "middle",
  "bmi_group": "normal",
  "ap_hi_group": "normal",
  "cholesterol": "1",
  "gluc": "1",
  "smoke": "0"
}
```
**Response:**

```
{
  "result": "预测结果：未患病（概率 87.35%）",
  "raw": {
    "0": 0.8735,
    "1": 0.1265
  }
}
```

---

### 💻 Frontend Setup (React + Vite)

```
cd frontend/vite-project
npm install
npm run dev
```

Accessible at: `http://localhost:3000`

---

## 🧠 Model Details

The Bayesian Network was constructed using key features such as:

- Age Group
- BMI Category
- Systolic Blood Pressure
- Cholesterol & Glucose Levels
- Smoking Status

Each variable is discretized into categories and conditional probability tables (CPTs) are learned from the dataset.

---

## 📦 Dependencies

### Backend

- Flask
- flask-cors
- numpy
- pandas

### Frontend

- React
- Vite
- axios
- Tailwind CSS (for styling)

---

## 🙌 Credits

Developed by [@FrogInDizzy](https://github.com/FrogInDizzy) as part of a medical data science initiative using Bayesian reasoning and modern web technologies.

---

## 🛡️ License

MIT License
