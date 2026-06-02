from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from bs4 import BeautifulSoup
import requests
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
async def outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Failed to fetch Wikipedia page: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")

    headings = []

    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        text = tag.get_text(" ", strip=True)

        if text:
            level = int(tag.name[1])
            headings.append("#" * level + " " + text)

    return "\n".join(headings)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )