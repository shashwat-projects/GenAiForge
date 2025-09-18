# 🧠 QuizForge AI  
A smart MCQ Generator powered by **Generative AI**. Upload your PDFs or text files, and QuizForge AI will instantly create interactive multiple-choice questions, provide evaluations, and let you download the results in JSON/CSV formats — all through a sleek Streamlit UI.

---

## 🚀 Features
- 📂 Upload **PDFs** or **Text files** as input  
- 📝 Generate **MCQs with multiple options**  
- ✅ Get **AI-driven evaluations** of quizzes  
- 💾 Download results as **JSON** or **CSV**  
- 🎨 Clean, responsive **Streamlit UI**  

---

## 🛠️ Tech Stack
- **Python** + **Streamlit** → UI and app orchestration  
- **LangChain** → Sequential AI pipelines  
- **DeepSeek V3.1** via HuggingFace → Quiz generation & evaluation  
- **Pandas** → Data formatting & CSV export  
- **PyPDF2** → PDF text extraction  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/shashwat-projects/MCQGenerator.git
cd MCQGenerator
```
### 2️⃣ Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Add Your HuggingFace Token
#### Add your_huggingface_token_here in the .env file in the project root:
```bash
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```
### 5️⃣ Run the App
```bash
streamlit run QuizForgeAI.py
```

## 📚 Usage
- Upload a PDF or text file containing study material.
- Select the number of questions, subject, and difficulty level.
- Click Generate Quiz.
- View generated MCQs and evaluation.
- Download results as JSON or CSV.

## 🔒 Notes
- Never commit your .env file or API keys to GitHub.
- For best results, use well-structured educational PDFs or clean text files.

## 🏷️ Tags
#GenerativeAI #LangChain #DeepSeek #Streamlit #Python #EdTech
