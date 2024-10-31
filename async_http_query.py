import aiohttp
import asyncio
import json

async def fetch_urls(urls: list[str], file_path: str):
    async with asyncio.Semaphore(5):
        async with aiohttp.ClientSession() as session:
            with open(file_path, 'w') as file:
                for url in urls:
                        try:
                            async with session.get(url) as response:
                                status_code = response.status
                        except Exception as e:
                            status_code = 0
                        file.write(json.dumps({"url": url, "status_code": status_code}) + '\n')

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]

if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))