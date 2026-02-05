from playwright.sync_api import sync_playwright # type: ignore

def post_to_linkedin(post_text="🚀 Building AI Employees that actually work."):
    """
    Post to LinkedIn using Playwright
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.linkedin.com/login")

        input("🔐 Login manually, then press ENTER...")

        page.goto("https://www.linkedin.com/feed/")
        page.click("button:has-text('Start a post')")
        page.fill("div[role='textbox']", post_text)
        page.click("button:has-text('Post')")

        print("✅ LinkedIn post published")
        browser.close()
        return {"status": "success", "message": "LinkedIn post published"}

# For backward compatibility, run the function if this file is executed directly
if __name__ == "__main__":
    post_to_linkedin()
