
# 📘 README.md
# Round 1B – Persona-Driven Document Intelligence

## 🔍 Input
- PDF files in `/app/input/`
- `persona_job.json` file:
```json
{
  "persona": "Investment Analyst",
  "job_to_be_done": "Analyze revenue trends, R&D investments, and market positioning strategies"
}
```

## ✅ Output
Generates `output.json` in `/app/output/` with:
- Metadata
- Extracted relevant sections
- Subsection analysis

## 🚀 Docker Build
```bash
docker build --platform linux/amd64 -t round1b-solution .
```

## 🏃 Run
```bash
docker run --rm \
  -v %cd%/input:/app/input \
  -v %cd%/output:/app/output \
  --network none round1b-solution
```

---
