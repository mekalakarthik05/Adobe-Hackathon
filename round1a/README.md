# Round 1A – Adobe India Hackathon

## Objective
Extract the Title and H1, H2, H3 headings from PDFs into a structured JSON outline.

## Folder Structure
- /app/input — Mount your PDFs here  
- /app/output — Your output JSON files will be saved here

## Build and Run

### Docker Build
```bash
docker build --platform linux/amd64 -t round1a-solution .
```

### Docker Run
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none round1a-solution
```

## Output JSON Format
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```