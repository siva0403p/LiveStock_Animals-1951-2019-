
import requests

urls = [
    "https://www.dahd.gov.in/schemes/programmes/animal-husbandry-statistics",
    "https://dahd.gov.in/schemes/programmes/animal-husbandry-statistics",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
}

for url in urls:
    print("\nTesting:", url)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30,
            allow_redirects=True,
        )

        print("Status:", response.status_code)
        print("Final URL:", response.url)
        print("Content-Type:", response.headers.get("Content-Type"))
        print("Response preview:", response.text[:250])

    except requests.RequestException as error:
        print("Request failed:", error)
