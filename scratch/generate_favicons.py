import os
from PIL import Image

def generate_favicons(source_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load high-res source
    img = Image.open(source_path)
    
    # Ensure it's square and has alpha channel
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # 1. favicon.ico (multi-resolution: 16, 32, 48)
    # PIL can save .ico directly
    img.save(os.path.join(output_dir, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print("Generated favicon.ico")

    # 2. favicon-96x96.png
    img.resize((96, 96), Image.Resampling.LANCZOS).save(os.path.join(output_dir, 'favicon-96x96.png'))
    print("Generated favicon-96x96.png")

    # 3. apple-touch-icon.png (180x180)
    img.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(output_dir, 'apple-touch-icon.png'))
    print("Generated apple-touch-icon.png")

    # 4. web-app-manifest-192x192.png
    img.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(output_dir, 'web-app-manifest-192x192.png'))
    print("Generated web-app-manifest-192x192.png")

    # 5. web-app-manifest-512x512.png
    img.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(output_dir, 'web-app-manifest-512x512.png'))
    print("Generated web-app-manifest-512x512.png")

    # 6. site.webmanifest
    manifest_content = """{
  "name": "Alfabeto Giapponese",
  "short_name": "Kana",
  "icons": [
    {
      "src": "assets/favicons/web-app-manifest-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "assets/favicons/web-app-manifest-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}"""
    # Placing manifest in root for standard discovery
    with open(os.path.join(os.path.dirname(output_dir), '..', 'site.webmanifest'), 'w') as f:
        f.write(manifest_content)
    print("Generated site.webmanifest in root")

if __name__ == "__main__":
    # Path of the generated image from brain directory
    source = r"C:\Users\Gabriele Errico\.gemini\antigravity\brain\a95ff8fa-b6a5-4eb3-be6b-34b402457d02\favicon_base_png_1775999682272.png"
    target = r"c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese\assets\favicons"
    generate_favicons(source, target)
