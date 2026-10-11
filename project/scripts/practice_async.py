# practice_async.py
import asyncio
import time
import aiohttp

async def fetch_example():
    """Practice async HTTP."""
    url = "https://api.github.com/repos/python/cpython"

    start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    elapsed = time.perf_counter() - start

    print(f"Fetched: {data['name']}")
    print(f"Tiempo: {elapsed:.3f} segundos")
    print(" Datos recibidos:")
    for key, value in data.items():
        print(f"  - {key}: {value}")

    return data

# Run it
asyncio.run(fetch_example())