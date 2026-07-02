import os
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\Nodar\ .gemini\antigravity\brain\4b9c675d-695d-41f1-9e04-844dc09d41c6".replace(" ", "")
screenshot_path = os.path.join(artifact_dir, "map_calibration_preview.png")

print("Launching Playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    
    url = "https://green-canyon-sales-portal.netlify.app/?debug=1"
    print(f"Navigating to {url} to set token...")
    page.goto(url)
    page.evaluate("() => localStorage.setItem('gc_mapbox_token', 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNoeXphbHl5MTBwY2t5M21tZTF3eHM5YTNuIn0.hzn2CrG37vP7C79n67nN1Q')")
    print("Reloading page with saved token...")
    page.goto(url)
    
    # Wait for map to load and render
    print("Waiting for map and overlays to load...")
    page.wait_for_timeout(10000) # Give Mapbox 10 seconds to load satellite tiles and overlays
    
    # Take a screenshot
    print(f"Saving screenshot to {screenshot_path}...")
    page.screenshot(path=screenshot_path)
    print("Screenshot saved successfully!")
    
    browser.close()
