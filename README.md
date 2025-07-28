# 🧠 Adobe India Hackathon 2025 – “Connecting the Dots”

Welcome to our official submission for the Adobe India Hackathon. This project addresses two core document intelligence challenges, aiming to enhance machine understanding and semantic extraction from complex PDFs.

---

## 📌 Challenges Covered

- ✅ **Round 1A – Document Outline Extraction**  
  Extract a structured outline (Title, H1, H2, H3) from scanned/image-based PDFs.

- ✅ **Round 1B – Persona-Based Relevance Ranking**  
  Given a persona and a job-to-be-done, analyze multiple PDFs to extract and rank the most relevant sections and sub-sections.

---

## 🧭 Project Structure

\`\`\`
Adobe-Hackathon/
├── round1a/                  # Round 1A: Outline Extraction
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   ├── input/                # Place input PDFs here
│   └── output/               # Output JSONs go here
│
├── round1b/                  # Round 1B: Persona Relevance Ranking
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   ├── input/                # Place PDFs + persona_job.json here
│   └── output/               # Output JSON file will be saved here
│
└── README.md                # Root-level summary (this file)
\`\`\`

---

## ⚙️ Technologies Used

- **Language:** Python 3.10  
- **OCR Engine:** Tesseract OCR  
- **PDF Rendering:** \`pdf2image\`, \`poppler-utils\`  
- **Containerization:** Docker (CPU-only, \`linux/amd64\`)  
- **Offline-First:** No internet access or external API calls required

---

## 🧩 Round 1A – Understand Your Document

### 📝 Objective  
Extract a structured, hierarchical outline from scanned/image-based PDFs. This includes:

- **Title**
- **H1** (Main Headings)
- **H2** (Subheadings)
- **H3** (Nested Subheadings)

### 📥 Input Format  
Place one or more \`.pdf\` files in:  
\`round1a/input/\`

### 📤 Output Format  
Each PDF results in a structured \`.json\` file saved in:  
\`round1a/output/\`

---

## 🧠 Round 1B – Persona-Driven Document Intelligence

### 📝 Objective  
Given:

- A set of **3–10 related PDFs**
- A **persona** (user role)
- A **job_to_be_done** (specific goal/task)

→ The system semantically analyzes the documents and extracts the **most relevant sections and sub-sections**, ranked by alignment with the user's goal.

### 📥 Input Format  
- PDFs and a \`persona_job.json\` placed in:  
  \`round1b/input/\`

### 📤 Output Format  
- A single \`output.json\` file containing the ranked relevant sections, saved in:  
  \`round1b/output/\`
