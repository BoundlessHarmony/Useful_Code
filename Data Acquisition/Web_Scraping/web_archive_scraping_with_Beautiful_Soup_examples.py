# ================================
# Import necessary libraries
import requests
from bs4 import BeautifulSoup

# ================================
# Define server connection parameters
WEB_SERVER = "<your_web_server_address>"  # Replace with target web server address

# ================================
# Request and parse a web page

# Simple GET request to the web server's main page
try:
    page = requests.get(f'https://{WEB_SERVER}/')
    print("Response status:", page)           # Print response status code
    print("Page text content (preview):", page.text[:500])   # Display partial text content
    print("Page byte content (preview):", page.content[:500]) # Display partial byte content

except Exception as e:
    print(f"Error retrieving main page: {e}")

# ================================
# Parse a specific page (e.g., archive) using BeautifulSoup

try:
    page = requests.get(f'http://{WEB_SERVER}/archive/')  # Access archive page
    soup = BeautifulSoup(page.content, "lxml")
    print("Archive page preview:", soup.prettify()[:800])  # Display formatted HTML preview

except Exception as e:
    print(f"Error retrieving archive page: {e}")

# ================================
# Define a function to retrieve and parse an archive page

def get_archive_page(url):
    """
    Retrieve an archive page at the specified URL.
    Returns a tuple with the URL of the next page (if it exists) and a dictionary of {"URL": "Subject"} pairs.
    """
    try:
        # Request the archive page content
        page = requests.get(f'https://{WEB_SERVER}/{url}')
        soup = BeautifulSoup(page.content, "lxml")
        
        # Parse div elements with class 'entry' for URL and subject extraction
        divs = soup.find_all("div", {"class": "entry"})
        url_subject_dict = {entry.find("a")["href"]: entry.find("div", {"class": "subject"}).text.strip() for entry in divs}

        # Identify the "next" page URL, if available
        try:
            next_page = soup.find("a", string="Next")['href']
        except:
            next_page = None  # No further pages available
        
        return next_page, url_subject_dict

    except Exception as e:
        print(f"Error retrieving archive page {url}: {e}")
        return None, {}


# Great for retrieving all the content a given website has to offer in a programmtic way #
# ================================
# Define a function to retrieve content from a specific example page

def get_example_content(url):
    """
    Retrieve content from a specific example page using the specified URL.
    Returns the text content within <pre> tags.
    """
    try:
        page = requests.get(f'https://{WEB_SERVER}/{url}')
        soup = BeautifulSoup(page.content, "lxml")
        
        # Extract content within <pre> tags
        example_content = soup.find("pre").text
        return example_content

    except Exception as e:
        print(f"Error retrieving example content from {url}: {e}")
        return ""

# ================================
# Retrieve and iterate through archive pages to collect examples

# Initialize archive traversal
next_url = "archive"  # Starting archive URL segment
archive_pages_count = 0
examples = {}  # Dictionary to store examples

# Loop through archive pages until there are no more "next" pages
while next_url:
    archive_pages_count += 1
    print(f"Processing archive page {archive_pages_count}")
    
    # Retrieve next page URL and subject-URL dictionary
    next_url, url_subject_dict = get_archive_page(next_url)
    
    # Fetch example content for each URL and store in examples dictionary
    for url, subject in url_subject_dict.items():
        examples[subject] = get_example_content(url)

# Summary of results
print(f"Total archive pages processed: {archive_pages_count}")
print(f"Total examples retrieved: {len(examples.keys())}")
