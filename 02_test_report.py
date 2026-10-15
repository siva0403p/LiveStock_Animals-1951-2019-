
import requests

pdf_url = (
    "https://www.dahd.gov.in/sites/default/files/"
    "2023-07/BAHS-2022.pdf"
)

try:
    with requests.get(
        pdf_url,
        timeout=30,
        stream=True,
    ) as response:

        print("Status:", response.status_code)
        print("Final URL:", response.url)
        print("Content-Type:",
              response.headers.get("Content-Type"))
        print("Content-Length:",
              response.headers.get("Content-Length"))

        response.raise_for_status()

        if "application/pdf" not in response.headers.get(
            "Content-Type", ""
        ).lower():
            print("Warning: Response may not be a PDF.")
        else:
            print("The server reports a PDF response.")

except requests.RequestException as error:
    print("Request failed:", error)
