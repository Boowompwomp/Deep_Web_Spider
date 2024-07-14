import requests

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def test_tor_proxy():
    try:
        response = requests.get("http://check.torproject.org", proxies=proxies, timeout=10)
        if response.status_code == 200 and "Congratulations. This browser is configured to use Tor." in response.text:
            print("Successfully connected to Tor network.")
        else:
            print("Tor connection test failed. Response status code:", response.status_code)
            print("Response text:", response.text[:500])  # Print the first 500 characters for debugging
    except requests.RequestException as e:
        print("Failed to verify Tor connection. Error:", e)

test_tor_proxy()

