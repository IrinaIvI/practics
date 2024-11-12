import aiohttp
import asyncio
import json

urls_q = asyncio.Queue()
results_q = asyncio.Queue()

async def fetch_url(urls_q: asyncio.Queue, results_q: asyncio.Queue):
    async with aiohttp.ClientSession() as session:
            while not urls_q.empty():
                url = await urls_q.get()
                try:
                    async with session.get(url) as response:
                        result = {"url": url, "status_code": response.status}
                except Exception:
                    result = {"url": url, "status_code": 0}
                await results_q.put(result)


async def writer(results_q: asyncio.Queue, file_path: str):
    with open(file_path, 'w') as file:
        while True:
            result = await results_q.get()
            if result is not None:
                file.write(json.dumps(result) + '\n')
            else:
                break

async def fetch_urls(urls: list[str], file_path: str):
    for url in urls:
        await urls_q.put(url)

    fetch_tasks = [asyncio.create_task(fetch_url(urls_q, results_q)) for _ in range(5)]
    writer_task = asyncio.create_task(writer(results_q, file_path))
    await asyncio.gather(*fetch_tasks)

    await results_q.put(None)

    await writer_task

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]

if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))