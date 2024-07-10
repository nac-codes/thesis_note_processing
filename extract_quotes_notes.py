import os
import json
import re

def extract_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "No title found"
    
    # Extract quotes and notes
    sections = re.split(r'```', content)[1:]  # Split by ``` and remove the first element (before first ```)
    quotes_and_notes = []
    
    for i in range(0, len(sections), 2):
        quote = sections[i].strip() if i < len(sections) else ""
        note = sections[i+1].strip() if i+1 < len(sections) else ""
        
        quotes_and_notes.append({
            'quote': quote,
            'note': note
        })
    
    return title, quotes_and_notes

def process_files(input_dir, output_file):
    results = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            title, quotes_and_notes = extract_content(file_path)
            
            for item in quotes_and_notes:
                results.append({
                    'title': title,
                    'quote': item['quote'],
                    'note': item['note']
                })
    
    # Write results to JSON
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(results, jsonfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(), 'input')
    output_file = 'extracted_quotes.json'
    
    process_files(input_directory, output_file)
    print(f"Extraction complete. Results saved to {output_file}")