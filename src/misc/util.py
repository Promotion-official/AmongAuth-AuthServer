import aiohttp


class HTMLGetter:
    def __init__(self, url):
        self.url = url

    async def get_json(self, **kwargs):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        async with aiohttp.ClientSession() as cs:
            html = await cs.post(
                self.url, headers=headers, json=kwargs
            )
            return await html.json()
