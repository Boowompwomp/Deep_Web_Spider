import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract

# Define the Tor proxy
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def verify_tor_connection():
    test_url = "http://check.torproject.org"
    try:
        response = requests.get(test_url, proxies=proxies, timeout=10)
        if response.status_code == 200 and "Congratulations. This browser is configured to use Tor." in response.text:
            print("Successfully connected to Tor network.")
        else:
            print("Tor connection test failed. Please check your Tor configuration.")
            print("Response status code:", response.status_code)
            print("Response text:", response.text[:500])  # Print the first 500 characters for debugging
            exit(1)
    except requests.RequestException as e:
        print("Failed to verify Tor connection. Error:", e)
        exit(1)

def wiki_crawl(onion_link):
     # Connect to the given Tor website and scrape outgoing URLs
    try:
        response = requests.get(f"http://{onion_link}", proxies=proxies, timeout=30)
        if response.status_code != 200:
            print(f"Failed to access {onion_link}: Status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = f"http://{onion_link}"

        # Find all links on the page
        links = soup.find_all('a', href=True)
        outgoing_urls = set()

        for link in links:
            href = link['href']
            # Ensure the URL is absolute
            absolute_url = urljoin(base_url, href)
            # Filter out internal links
            if urlparse(absolute_url).netloc != urlparse(base_url).netloc:
                outgoing_urls.add(absolute_url)

        return list(outgoing_urls)

    except requests.RequestException as e:
        print(f"Failed to connect to {onion_link}. Error: {e}")
        return []

def get_website_name(url):
    ext = tldextract.extract(url)
    ext_url =  f"{ext.domain}.{ext.suffix}"
    return ext_url[:10]

def write_outgoing_urls_to_file(onion_link, output_file):
    outgoing_urls = wiki_crawl(onion_link)
    num_written = 0
    if not outgoing_urls:
        print(f"No outgoing URLs found for {onion_link}")
        return

    with open(output_file, 'a') as file:
        file.write(f"{onion_link}\n")
        for url in outgoing_urls:
            website_name = get_website_name(url)
            print(num_written,"links scraped so far.", end="\n")
            file.write(f"\t{website_name}\n\t\t{url}\n")
            num_written += 1
    print(f"Outgoing URLs from {onion_link} written to {output_file}")

# Example usage
onion_link = "wiki47qqn6tey4id7xeqb6l7uj6jueacxlqtk3adshox3zdohvo35vad.onion"
output_file = 'outgoing_urls.txt'
write_outgoing_urls_to_file(onion_link, output_file)