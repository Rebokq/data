from bs4 import BeautifulSoup

html = """
<div class="theme-screenshot one attachment-theme-screenshot size-theme-screenshot wp-post-image loaded" data-featured-src="https://websitedemos.net/wp-content/uploads/2019/07/outdoor-adventure-02-home.jpg" data-src="https://websitedemos.net/wp-content/uploads/2019/07/outdoor-adventure-02-home.jpg" style='background-image: url("https://websitedemos.net/wp-content/uploads/2019/07/outdoor-adventure-02-home.jpg");'></div>
"""
soup = BeautifulSoup(html, "html.parser")
url = soup.select_one(
    "div.theme-screenshot.one.attachment-theme-screenshot.size-theme-screenshot.wp-post-image.loaded"
).get("data-src")

print(url)