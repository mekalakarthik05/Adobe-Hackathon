# 🧠 Adobe India Hackathon 2025 – “Connecting the Dots”

Welcome to our official submission for the Adobe India Hackathon. This project showcases our solutions to two document intelligence challenges designed to improve how machines interpret and extract meaning from PDFs.

---

## 📌 Challenges Covered

- ✅ **Round 1A** – Extract a structured outline (Title + H1, H2, H3 headings) from a scanned or image-based PDF
- ✅ **Round 1B** – Given a persona and job-to-be-done, analyze multiple PDFs and extract the most relevant sections and sub-sections

---

## 🧭 Project Structure

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

