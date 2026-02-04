from playwright.sync_api import sync_playwright # type: ignore

POST_TEXT = "🚀 Building AI Employees that actually work."

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.linkedin.com/login")

    input("🔐 Login manually, then press ENTER...")

    page.goto("https://www.linkedin.com/feed/")
    page.click("button:has-text('Start a post')")
    page.fill("div[role='textbox']", POST_TEXT)
    page.click("button:has-text('Post')")

    print("✅ LinkedIn post published")
    browser.close()
