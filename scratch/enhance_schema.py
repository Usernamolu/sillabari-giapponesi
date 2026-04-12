import os
import re

def enhance_schema(root_dir):
    # 1. Update Index Schema
    index_path = os.path.join(root_dir, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        enhanced_index_json = """    {
      "@context": "https://schema.org",
      "@type": "LearningResource",
      "name": "Hiragana and Katakana Digital Collection",
      "description": "Una risorsa interattiva web per l'apprendimento dei sillabari Hiragana e Katakana giapponesi.",
      "author": {
        "@type": "Person",
        "name": "Gabriele Errico"
      },
      "educationalLevel": "Beginner",
      "inLanguage": ["it", "ja"],
      "learningResourceType": "Tutorial",
      "educationalAlignment": {
        "@type": "AlignmentObject",
        "alignmentType": "educationalLevel",
        "educationalFramework": "Common European Framework of Reference for Languages (CEFR)",
        "targetName": "A1",
        "targetUrl": "https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages"
      },
      "about": [
        {
          "@type": "Thing",
          "name": "Hiragana",
          "sameAs": "https://www.wikidata.org/wiki/Q48332"
        },
        {
          "@type": "Thing",
          "name": "Katakana",
          "sameAs": "https://www.wikidata.org/wiki/Q48332"
        }
      ]
    }"""
        
        # Replace the entire JSON-LD block in index
        new_content = re.sub(r'(\s*<script type="application/ld\+json">).*?(</script>)', 
                            f'\\1\n{enhanced_index_json}\n    \\2', content, flags=re.DOTALL)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated index.html schema")

    # 2. Update Character Page Schemas
    for folder in ['hiragana', 'katakana']:
        folder_path = os.path.join(root_dir, folder)
        if not os.path.exists(folder_path):
            continue
            
        for file in os.listdir(folder_path):
            if file.endswith('.html'):
                file_path = os.path.join(folder_path, file)
                char_name = file.replace('.html', '').capitalize()
                sillabario = folder.capitalize()
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Search for character in high title or main kana
                # Using file name as proxy for name
                enhanced_char_json = f"""    {{
      "@context": "https://schema.org",
      "@type": "LearningResource",
      "name": "{sillabario} {char_name}",
      "description": "Scheda didattica per il carattere {sillabario} {char_name}.",
      "learningResourceType": "Character Page",
      "educationalLevel": "Beginner",
      "inLanguage": ["it", "ja"],
      "author": {{
        "@type": "Person",
        "name": "Gabriele Errico"
      }},
      "about": {{
        "@type": "Thing",
        "name": "{char_name}",
        "description": "Caractere {char_name} del sillabario {sillabario}"
      }}
    }}"""

                new_content = re.sub(r'(\s*<script type="application/ld\+json">).*?(</script>)', 
                                    f'\\1\n{enhanced_char_json}\n    \\2', content, flags=re.DOTALL)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {folder}/{file} schema")

if __name__ == "__main__":
    enhance_schema(r"c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese")
