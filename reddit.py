from playwright.sync_api import sync_playwright

def find_post(client, subreddit, time):
    """
    Find the top post from a specified subreddit within a given time range.

    Args:
        subreddit (str): The name of the subreddit to search.
        time (str): The time range to consider for the top post (e.g., 'day', 'week', 'month', 'year', 'all').

    Returns:
        tuple: A tuple containing the title, text, and URL of the top post.
    """
    subreddit = client.subreddit(subreddit)

    # Get the top post within the specified time range
    top_post = next(subreddit.top(time, limit=1))

    text = top_post.selftext
    url = top_post.url
    title = top_post.title

    return title, text, url

def extract_post_from_url(client, url):
    """
    Extract the title and text content of a Reddit post from its URL.

    Args:
        url (str): The URL of the Reddit post.

    Returns:
        tuple: A tuple containing the title and text content of the post.
    """
    submission = client.submission(url=url)

    return submission.title, submission.selftext

def capture_reddit_title_screenshot(url):
    """
    Capture a screenshot of the title element of a Reddit post using Playwright.

    Args:
        url (str): The URL of the Reddit post.
    """
    with sync_playwright() as p:
        # Create a new browser context with an arbitrary user agent
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        )
        page = context.new_page()
        
        # Head to the url of the reddit post
        page.goto(url)
        
        # Make sure the page has loaded by waiting for the title element to render
        page.wait_for_selector('h1')
        
        # Select and take a screenshot of the title element only
        title_element = page.query_selector('h1')
        if title_element:
            title_element.screenshot(path="title.png")
        else:
            print("Title element not found.")
        
        browser.close()
