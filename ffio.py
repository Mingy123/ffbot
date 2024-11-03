import hmac
import hashlib
import json
import aiohttp
import asyncio
import os

api_secret = os.environ['FF_API_SECRET']
api_key = os.environ['FF_API_KEY']

async def getRate(fromCcy="XMR", toCcy="LTC"):
    json_data = {
        "fromCcy": fromCcy,
        "toCcy": toCcy,
        "amount": 1.0,
        "direction": "from",
        "type": "float"
    }

    json_data_string = json.dumps(json_data)
    signature = hmac.new(api_secret.encode(), json_data_string.encode(), hashlib.sha256).hexdigest()

    headers = {
        "Accept": "application/json",
        "X-API-KEY": api_key,
        "X-API-SIGN": signature,
        "Content-Type": "application/json; charset=UTF-8"
    }

    url = "https://ff.io/api/v2/price"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json_data_string) as response:
            assert response.status == 200
            result = await response.json()
            assert result['code'] == 0
            rate_from = result['data']['from']['rate']
            rate_to = result['data']['to']['rate']
            return rate_from, rate_to

# Example of how to run the async function
async def main():
    rate_from, rate_to = await getRate()
    print(f"Rate from: {rate_from}, Rate to: {rate_to}")

if __name__ == '__main__':
    asyncio.run(main())
