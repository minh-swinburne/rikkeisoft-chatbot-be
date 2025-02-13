import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_and_save_webpage(link: str, title: str = "Webpage", beautiful = False):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract page title for filename
        page_title = soup.title.string if soup.title else title
        page_title = re.sub(r"[^\w\s-]", "", page_title).strip()

        if beautiful:
            # Inline all CSS styles
            for css_link in soup.find_all("link", {"rel": "stylesheet"}):
                css_url = urljoin(link, css_link["href"])
                try:
                    css_response = requests.get(css_url)
                    css_response.raise_for_status()
                    style_tag = soup.new_tag("style")
                    style_tag.string = css_response.text
                    soup.head.append(style_tag)
                    css_link.decompose()  # Remove original <link> tag
                except requests.RequestException:
                    print(f"❌ Failed to fetch CSS: {css_url}")

            # Inline JavaScript (optional: only if critical for page display)
            for script in soup.find_all("script", {"src": True}):
                script_url = urljoin(link, script["src"])
                try:
                    script_response = requests.get(script_url)
                    script_response.raise_for_status()
                    script_tag = soup.new_tag("script")
                    script_tag.string = script_response.text
                    soup.body.append(script_tag)
                    script.decompose()  # Remove original <script> tag
                except requests.RequestException:
                    print(f"❌ Failed to fetch JS: {script_url}")

        # Save the modified HTML content
        file_name = f"{page_title}{"_beautiful" if beautiful else ""}.html"
        file_content = soup.prettify().encode("utf-8")

        return file_name, file_content  # You can upload this file to S3 or save locally

    except requests.RequestException as e:
        print(f"❌ Failed to fetch webpage: {e}")
        return None, None


if __name__ == "__main__":
    links = [
        # "https://www.example.com",
        # "https://webscraping.ai/faq/beautiful-soup/how-do-i-extract-scripts-or-stylesheets-using-beautiful-soup",
        # "https://quasar.dev/vue-components/list-and-list-items#qitem-api",
        # "https://stackoverflow.com/questions/70871059/flex-box-isnt-filling-remaining-space-when-using-flex-grow-1",
        "https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html",
        "https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset#examples",
    ]
    for link in links:
        folder = "test_links/"
        file_name, file_content = fetch_and_save_webpage(link)
        if file_name:
            with open(folder + file_name, "wb") as f:
                f.write(file_content)
            print(f"✅ Saved {file_name}")
        else:
            print("❌ Failed to save webpage")
        file_name, file_content = fetch_and_save_webpage(link, beautiful=True)
        if file_name:
            with open(folder + file_name, "wb") as f:
                f.write(file_content)
            print(f"✅ Saved {file_name}")
        else:
            print("❌ Failed to save webpage")
