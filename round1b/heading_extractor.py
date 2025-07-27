
import pytesseract
from pdf2image import convert_from_path
from pytesseract import Output
from pathlib import Path
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Medha Trust\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_headings_from_pdf(pdf_path: Path, dpi: int = 200, max_clusters: int = 4):
    images = convert_from_path(str(pdf_path), dpi=dpi)
    title = ""
    all_lines = []

    for page_num, img in enumerate(images, start=1):
        width, height = img.size
        ocr_data = pytesseract.image_to_data(img, output_type=Output.DICT)

        lines = defaultdict(list)
        n = len(ocr_data['text'])
        for i in range(n):
            word = ocr_data['text'][i].strip()
            if not word:
                continue
            key = (ocr_data['block_num'][i], ocr_data['par_num'][i], ocr_data['line_num'][i])
            conf = int(ocr_data['conf'][i]) if isinstance(ocr_data['conf'][i], str) and ocr_data['conf'][i].isdigit() else 0
            lines[key].append({
                'text': word,
                'left': ocr_data['left'][i],
                'top': ocr_data['top'][i],
                'width': ocr_data['width'][i],
                'height': ocr_data['height'][i],
                'conf': conf
            })

        line_entries = []
        for word_list in lines.values():
            if len(word_list) < 1:
                continue
            avg_height = np.mean([w['height'] for w in word_list])
            max_conf = np.max([w['conf'] for w in word_list])
            left = min(w['left'] for w in word_list)
            right = max(w['left'] + w['width'] for w in word_list)
            center_x = (left + right) / 2
            sentence = " ".join(w['text'] for w in word_list)

            line_entries.append({
                'text': sentence.strip(),
                'avg_height': avg_height,
                'center_x': center_x,
                'page': page_num,
                'left': left,
                'top': min(w['top'] for w in word_list),
                'right': right,
                'width': right - left,
                'max_conf': max_conf
            })

        if page_num == 1 and not title:
            center_threshold = width * 0.1
            candidates = [l for l in line_entries if abs(l['center_x'] - width/2) < center_threshold]
            if candidates:
                title = sorted(candidates, key=lambda x: -x['avg_height'])[0]['text']

        all_lines.extend(line_entries)

    if len(all_lines) == 0:
        return {"title": title, "outline": []}

    # Cluster heights to assign heading levels
    heights = np.array([[line['avg_height']] for line in all_lines])
    k = min(max_clusters, len(heights))
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=0).fit(heights)
    cluster_labels = kmeans.labels_

    cluster_avg = {label: np.mean(heights[cluster_labels == label]) for label in set(cluster_labels)}
    sorted_clusters = sorted(cluster_avg.items(), key=lambda x: -x[1])
    cluster_to_level = {label: f"H{i+1}" for i, (label, _) in enumerate(sorted_clusters)}

    outline = []
    for i, line in enumerate(all_lines):
        label = cluster_labels[i]
        level = cluster_to_level[label]

        if line['avg_height'] < 0.6 * max(cluster_avg.values()):
            continue
        if len(line['text'].strip()) < 5:
            continue
        if "RFP" in line['text'] and line['avg_height'] < 0.9 * max(cluster_avg.values()):
            continue

        outline.append({
            "level": level,
            "text": line['text'],
            "page": line['page']
        })

    outline = sorted(outline, key=lambda x: (x['page'], x['level']))

    return {
        "title": title,
        "outline": outline
    }
