
from pathlib import Path
import requests

url = (
    "https://www.dahd.gov.in/static/uploads/2025/07/"
    "29e851f6c888f97635a38fd03caa4c27.pdf"
)

output = Path("dahd_publication.pdf")

response = requests.get(url, timeout=60)
response.raise_for_status()

content = response.content

if not content.startswith(b"%PDF-"):
    raise ValueError("The response is not a valid PDF file.")

output.write_bytes(content)

print("Download successful")
print("File:", output.resolve())
print("Size:", round(len(content) / (1024 * 1024), 2), "MB")
print("PDF signature verified:", content[:5])
