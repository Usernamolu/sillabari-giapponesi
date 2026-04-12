import os
import sys
from playwright.sync_api import sync_playwright

def test_site_integrity():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    index_path = f"file:///{os.path.join(root_dir, 'index.html')}".replace('\\', '/')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Testing Index: {index_path}")
        page.goto(index_path)
        
        # 1. Title verification
        title = page.title()
        assert "Alfabeto Giapponese" in title
        print(f"[OK] Title check passed")

        # 2. Section verification
        assert page.locator('#hiragana').is_visible()
        assert page.locator('#katakana').is_visible()
        print("[OK] Structure check passed (Hiragana/Katakana sections found)")

        # 3. Accessibility: Skip Link
        skip_link = page.locator('.skip-link')
        assert skip_link.is_visible()
        print("[OK] Accessibility: Skip link present")

        # 4. Favicon verification (Check if manifest and link tags are there)
        manifest_link = page.locator('link[rel="manifest"]')
        assert manifest_link.count() > 0
        print("[OK] Branding: site.webmanifest link found")

        # 5. Mass Link Integrity (Sample check)
        # We test if the first 5 hiragana links work
        hiragana_links = page.locator('#tabella-hiragana a').all()
        print(f"Found {len(hiragana_links)} Hiragana links. Testing first 5...")
        
        for i in range(min(5, len(hiragana_links))):
            link = hiragana_links[i]
            href = link.get_attribute('href')
            label = link.get_attribute('aria-label')
            
            # Click and verify
            link.click()
            page.wait_for_load_state('networkidle')
            
            assert page.url.endswith(href)
            assert page.locator('.main-character').is_visible() or page.locator('.main-kana').is_visible()
            print(f"  [OK] Link {label} verified: {page.url}")
            
            # Go back
            page.goto(index_path)

        print("\nSUCCESS: All core integrity tests passed.")
        browser.close()

if __name__ == "__main__":
    try:
        test_site_integrity()
    except Exception as e:
        print(f"\nFAILURE: {e}")
        sys.exit(1)
