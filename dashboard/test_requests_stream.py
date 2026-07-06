import requests

url = "http://192.168.137.52:81/stream"

print("before request")

response = requests.get(url, stream=True, timeout=5)

print("status:", response.status_code)
print("content-type:", response.headers.get("Content-Type"))

for chunk in response.iter_content(chunk_size=1024):
    print("chunk received:", len(chunk))
    break