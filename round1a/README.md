# 🔹 Round 1A – Adobe India Hackathon 2025

## 🚀 Objective
Build an intelligent outline extractor that processes PDFs and outputs structured JSON containing:
- Document Title
- Headings: H1, H2, and H3, along with their respective page numbers

## 📁 Folder Structure
```
round1a/
├── Dockerfile
├── main.py
├── requirements.txt
├── input/          # Input PDF files go here
├── output/         # Output JSON files will be saved here
└── README.md
```

## 🧱 Build Instructions
Build the Docker image compatible with AMD64 architecture:
```bash
docker build --platform linux/amd64 -t round1a-solution .
```

## ▶️ Run Instructions
Run the container to process PDFs from `/app/input` and output the corresponding JSON to `/app/output`:
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none round1a-solution
```

## 📤 Input Specification
- Place your `.pdf` files inside the `input/` directory before running the Docker container.
- Each PDF should be ≤ 50 pages in length.

## 📥 Output Format
For each input PDF (e.g., `sample.pdf`), a corresponding JSON file (`sample.json`) will be saved in the `output/` directory.

## ⚙️ Technical Constraints
- 📄 Max PDF length: 50 pages
- ⏱ Max processing time: 10 seconds per document
- 📦 Model size (if used): ≤ 200MB
- 🌐 Offline only: No internet access during execution
- 🧠 CPU-only execution (no GPU)

## 📌 Notes
- Avoid hardcoded logic for any specific document.
- Do not rely solely on font size — use multiple heuristics (font weight, position, etc.) for better accuracy.
- All dependencies are installed via `requirements.txt`.
