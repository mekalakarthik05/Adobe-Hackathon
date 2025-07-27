import os
import json
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
from pytesseract import Output
from collections import defaultdict
import numpy as np
import re

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

def merge_lines(lines, vertical_gap=10, height_tolerance=2):
    if not lines:
        return []
    lines.sort(key=lambda x: (x['page'], x['top']))
    merged = []
    current = lines[0]
    for next_line in lines[1:]:
        same_page = next_line['page'] == current['page']
        close_vert = abs(next_line['top'] - current['bottom']) <= vertical_gap
        similar_height = abs(next_line['avg_height'] - current['avg_height']) <= height_tolerance
        if same_page and close_vert and similar_height:
            current['text'] += " " + next_line['text']
            current['bottom'] = max(current['bottom'], next_line['bottom'])
        else:
            merged.append(current)
            current = next_line
    merged.append(current)
    return merged

def extract_all_headings(pdf_path, dpi=200):
    images = convert_from_path(pdf_path, dpi=dpi)
    raw_lines = []
    title_text = ""
    title_found = False

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
            avg_width = np.mean([w['width'] for w in words])
            avg_conf = np.mean([w['conf'] for w in words])
            left = min(w['left'] for w in words)
            right = max(w['left'] + w['width'] for w in words)
            top = min(w['top'] for w in words)
            bottom = max(w['top'] + w['height'] for w in words)
            center_x = (left + right) / 2
            width_ratio = (right - left) / (avg_width * len(words) + 1e-5)

            if page_num == 1 and not title_found:
                if abs(center_x - width / 2) < width * 0.1 and avg_height > 15:
                    title_text = sentence
                    title_found = True
                    continue

            raw_lines.append({
                "text": sentence,
                "avg_height": avg_height,
                "top": top,
                "bottom": bottom,
                "page": page_num,
                "center_x": center_x,
                "avg_conf": avg_conf,
                "width_ratio": width_ratio
            })

    merged_lines = merge_lines(raw_lines)

    page_groups = defaultdict(list)
    for line in merged_lines:
        text = line['text']

        if len(text.split()) > 14 or len(text.strip()) < 3:
            continue
        if re.fullmatch(r'[\W\d\s]+', text):
            continue
        if text.islower():
            continue
        if line['avg_conf'] < 35:
            continue
        if line['width_ratio'] > 2.2:
            continue
        if line['avg_height'] < 13:
            continue
        if text.strip().endswith(('.', ',')) and len(text.split()) > 4:
            continue

        page_groups[line['page']].append(line)

    all_headings = []
    for page, lines in page_groups.items():
        heights = sorted(set([round(l['avg_height'], 1) for l in lines]), reverse=True)
        top_heights = heights[:4]
        level_map = {h: f"H{i+1}" for i, h in enumerate(top_heights)}

        for line in lines:
            closest = min(top_heights, key=lambda h: abs(h - line['avg_height']))
            level = level_map[closest]
            all_headings.append({
                "level": level,
                "text": line['text'],
                "page": line['page']
            })

    all_headings.sort(key=lambda h: (h['page'], h['level']))

    return {
        "title": title_text.strip(),
        "outline": all_headings
    }

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_files = list(input_dir.glob("*.pdf"))

    for pdf_file in pdf_files:
        result = extract_all_headings(str(pdf_file))
        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process_pdfs()