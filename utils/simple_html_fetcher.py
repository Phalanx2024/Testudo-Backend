import argparse
from patchright.sync_api import sync_playwright
import time


def verify_success(page):
    """Verify we've successfully passed the challenge"""
    try:
        # Wait for actual site content to load - adjust selector as needed
        page.wait_for_selector('main', timeout=4000)  # Adjust selector based on the target site
        time.sleep(3)
        return True
    except Exception:
        return False

def get_html(
    url,
    output_file=None,
    preview=False,
    preview_length=10000,
    verify_ssl=False,
    honeypot_key=None,
    captcha_key=None,
):
    """
    Fetch HTML content from a URL using Playwright with 2captcha support
    """
    if not captcha_key:
        print("Warning: No 2captcha API key provided. Automated challenge solving will not work.")
        return None

    solver = TwoCaptcha(captcha_key)

    # Check IP status first if honeypot key is provided
    if honeypot_key:
        print("Checking IP status with Project Honey Pot...")
        if not check_ip(honeypot_key):
            print(
                "Warning: Your IP might be blacklisted. This could affect "
                "Cloudflare access."
            )
            response = input("Continue anyway? (y/n): ")
            if response.lower() != "y":
                return None

    print(f"Fetching URL: {url}")

    try:
        with sync_playwright() as p:
            # Launch browser with specific options for better undetectability
            browser = p.chromium.launch(
                headless=False,
                channel="chrome",
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-features=IsolateOrigins,site-per-process",
                    "--disable-web-security",
                    "--disable-site-isolation-trials",
                ]
            )

            # Modern browser context with up-to-date headers
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},  # Standard desktop resolution
                ignore_https_errors=not verify_ssl,
                locale="en-US",
                timezone_id="America/New_York",
                permissions=["geolocation"],
                extra_http_headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Upgrade-Insecure-Requests": "1",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                }
            )

            page = context.new_page()

            print("Navigating to page...")
            page.goto(url, wait_until="domcontentloaded")

            try:
                # Look for Turnstile widget
                turnstile_frame = page.frame_locator("iframe[src*='turnstile']")
                if turnstile_frame.count() > 0:
                    print("Found Turnstile challenge, solving with 2captcha...")
                    
                    # Get the sitekey from the page
                    sitekey = page.evaluate('''() => {
                        const iframe = document.querySelector('iframe[src*="turnstile"]');
                        const src = iframe.src;
                        const match = src.match(/sitekey=([^&]+)/);
                        return match ? match[1] : null;
                    }''')
                    
                    if not sitekey:
                        print("Could not find sitekey")
                        return None
                    
                    print(f"Found sitekey: {sitekey}")
                    
                    # Solve the Turnstile challenge
                    try:
                        result = solver.turnstile(
                            sitekey=sitekey,
                            url=url,
                        )
                        
                        print("Got solution from 2captcha")
                        
                        # Apply the solution
                        page.evaluate(f'''(token) => {{
                            window.turnstileCallback(token);
                        }}''', result['code'])
                        
                        print("Applied solution, waiting for page load...")
                        page.wait_for_load_state("networkidle", timeout=30000)
                        
                    except Exception as e:
                        print(f"2captcha error: {str(e)}")
                        return None

            except Exception as e:
                print(f"Error handling challenge: {str(e)}")
                return None

            # Get the page content
            html_content = page.content()
            if "jehoshaphatresearch.com needs to review" in html_content:
                print("Still on Cloudflare page - challenge not completed")
                return None

            print("Successfully retrieved content")
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"HTML saved to {output_file}")
    
            if preview:
                print("\nHTML Content Preview:")
                print(html_content[:preview_length])
                print(f"\nTotal HTML length: {len(html_content)} characters")

            browser.close()
            return html_content

    except Exception as e:
        print(f"Error fetching HTML: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Fetch HTML content from a URL"
    )
    parser.add_argument("url", help="The URL to fetch HTML from")
    parser.add_argument("-o", "--output", help="Output file to save the HTML to")
    parser.add_argument(
        "-p", "--preview", action="store_true", help="Show preview of the HTML"
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=10000,
        help="Number of characters to preview (default: 10000)",
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        help="Disable SSL certificate verification",
    )
    parser.add_argument("--honeypot-key", help="Project Honey Pot access key")
    parser.add_argument("--captcha-key", help="2captcha API key")

    args = parser.parse_args()
    get_html(
        args.url,
        args.output,
        args.preview,
        args.length,
        verify_ssl=not args.no_verify_ssl,
        honeypot_key=args.honeypot_key,
        captcha_key=args.captcha_key,
    )


if __name__ == "__main__":
    main()
