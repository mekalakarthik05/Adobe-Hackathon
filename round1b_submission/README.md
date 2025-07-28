# 📘 Round 1B – Persona-Driven Document Intelligence
**Adobe India Hackathon 2025**

## 🎯 Objective
Build an intelligent document analyzer that extracts and ranks the most relevant sections and subsections from a collection of PDFs based on:

- A persona definition
- A job-to-be-done

---

## 📁 Folder Structure

```
round1b_submission/
├── Dockerfile             
├── main.py                 
├── requirements.txt          
├── input/               
│ ├── document1.pdf      # Example input PDFs
│ ├── document2.pdf
│ └── persona_job.json   # Persona and job-to-be-done definition
├── output/              
│ └── output.json        # Generated output after processing
└── README.md 
```
---

## 📥 Input
Place the following in the `/app/input/` directory:

- PDF documents (3–10 related files)
- A file named `persona_job.json` containing:
```json
{
  "persona": "Investment Analyst",
  "job_to_be_done": "Analyze revenue trends, R&D investments, and market positioning strategies"
}
```

## 📤 Output
The system will generate a single `output.json` file in the `/app/output/` directory containing:

### 📌 Metadata
- Input filenames
- Persona
- Job-to-be-done
- Timestamp

### 📄 Extracted Sections
- Section titles
- Page numbers
- Importance ranking

### 🧠 Subsection Analysis
- Refined text summaries
- Page numbers
- Importance ranking



## ⚙️ Docker Instructions

### 🧱 Build the Image
```bash
docker build --platform linux/amd64 -t round1b-solution .
```

### ▶️ Run the Container

#### For Linux/macOS:
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none round1b-solution
```

## 🛠️ Constraints
- 🧠 CPU only (no GPU)
- 📦 Model size ≤ 1GB
- ⏱ Processing time ≤ 60 seconds for 3–5 PDFs
- 🌐 No internet/network access

📌 Notes
- Avoid hardcoded logic for specific personas or documents.
- Use semantic relevance to rank sections/subsections.
- Ensure offline execution with model size ≤ 1GB.
- All dependencies must be handled via requirements.txt.

