import os
import json
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
from pytesseract import Output
from collections import defaultdict
import numpy as np
import re
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  # For Linux Docker. For Windows local, change as needed.

def extract_headings_with_text(pdf_path, dpi=200):
    images = convert_from_path(pdf_path, dpi=dpi)
    doc_results = []

    for page_num, img in enumerate(images, start=1):
        width, _ = img.size
        data = pytesseract.image_to_data(img, output_type=Output.DICT)
        lines = defaultdict(list)

        for i in range(len(data['text'])):
            word = data['text'][i].strip()
            if word:
                key = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
                lines[key].append({
                    'text': word,
                    'left': data['left'][i],
                    'top': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i],
                    'conf': int(data['conf'][i]) if str(data['conf'][i]).isdigit() else 0
                })

        for words in lines.values():
            sentence = " ".join(w['text'] for w in words).strip()
            if not sentence:
                continue
            avg_height = np.mean([w['height'] for w in words])
            left = min(w['left'] for w in words)
            right = max(w['left'] + w['width'] for w in words)
            top = min(w['top'] for w in words)
            bottom = max(w['top'] + w['height'] for w in words)
            center_x = (left + right) / 2
            width_ratio = (right - left) / (np.mean([w['width'] for w in words]) * len(words) + 1e-5)

            doc_results.append({
                "text": sentence,
                "avg_height": avg_height,
                "top": top,
                "bottom": bottom,
                "page": page_num,
                "center_x": center_x,
                "avg_conf": np.mean([w['conf'] for w in words]),
                "width_ratio": width_ratio
            })

    return doc_results

def compute_relevance_score(text, persona, job):
    # Flatten persona/job if they're dicts
    persona_text = json.dumps(persona) if isinstance(persona, dict) else str(persona)
    job_text = json.dumps(job) if isinstance(job, dict) else str(job)

    combined = (persona_text + " " + job_text).lower()
    keywords = re.findall(r'\w+', combined)
    score = sum(text.lower().count(k) for k in keywords)
    return score

def process_documents(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(input_dir / "persona_job.json", "r", encoding="utf-8") as f:
        task_info = json.load(f)
    #print("Loaded persona_job.json:", json.dumps(task_info, indent=2))

    persona = task_info["persona"]
    job = task_info["job_to_be_done"]

    metadata = {
        "input_documents": [],
        "persona": persona,
        "job_to_be_done": job,
        "timestamp": datetime.utcnow().isoformat()
    }

    extracted_sections = []
    subsection_analysis = []

    for pdf_file in input_dir.glob("*.pdf"):
        if pdf_file.name == "persona_job.json":
            continue

        metadata["input_documents"].append(pdf_file.name)
        lines = extract_headings_with_text(str(pdf_file))
        ranked = []

        for line in lines:
            if line['avg_conf'] < 40 or len(line['text'].split()) > 20:
                continue
            score = compute_relevance_score(line['text'], persona, job)
            if score > 0:
                ranked.append((score, line))

        ranked.sort(reverse=True, key=lambda x: x[0])

        for rank, (score, line) in enumerate(ranked[:5], start=1):
            extracted_sections.append({
                "document": pdf_file.name,
                "page": line["page"],
                "section_title": line["text"],
                "importance_rank": rank
            })
            subsection_analysis.append({
                "document": pdf_file.name,
                "page": line["page"],
                "section_title": line["text"],
                "refined_text": line["text"]
            })

    output_data = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_dir / "output.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process_documents("/app/input", "/app/output")
