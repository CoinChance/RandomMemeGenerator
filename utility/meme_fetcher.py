import aiohttp
import asyncio
import random

topics_accepted = {
    "random": ["memes", "meme", "solana",
        "ethereum",
        "crytpocurrencies",
        "bitcoin",
        "dogecoin",
        "shiba",
        "doge",
        "shibainu"
    ],
    "memes": ["memes"],
    "coding": [
        "programmerhumor",
        "programmingmemes",
        "programminghumor",
        "codingmemes",
        "pythonmemes",
        "javascriptmemes",        
    ],
    "crypto":["crypto",
        "solana",
        "ethereum",
        "crytpocurrencies",
        "bitcoin",
        "dogecoin",
        "shiba",
        "doge",
        "shibainu",
        "czbinance",
    ]
}

# Define function to check if a post is an image
async def is_image_post(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            content_type = response.headers.get("Content-Type", "")
            return content_type.startswith("image/")

SUBREDDITS = ["CryptoCurrencyMemes", "CryptoMemes"]

async def get_meme(subreddit, logging):
    """Gets a meme from reddit from the subreddit provided"""
    meme_not_found, max_tries = True, 10
    async with aiohttp.ClientSession() as session:
        logging.info('subreddit requested: ')
        logging.info(subreddit)
        if subreddit in topics_accepted:
            subreddit = random.choice(topics_accepted[subreddit])

        logging.info('subreddit selected: ')
        logging.info(subreddit)
        while meme_not_found and max_tries > 0:
            # top_or_other = random.randint(0, 1)
            # if top_or_other == 0:
            #     async with session.get(
            #         f"https://www.reddit.com/r/{subreddit}/{random.choice(['hot', 'new'])}.json"
            #     ) as response:
            #         data = await response.json()
            # else:
            #     async with session.get(
            #         f"https://www.reddit.com/r/{subreddit}/top.json?t={random.choice(['hour','day', 'week', 'month', 'year'])}"
            #     ) as response:
            #         data = await response.json()

            subreddit = random.choice(SUBREDDITS)
            sort_type = random.choice(["hot", "new", "top"])

            # Use Reddit's filter for listing only images
            async with session.get(
                f"https://www.reddit.com/r/{subreddit}/{sort_type}.json?sort=rising&restrict_sr=on&img=on"
            ) as response:
                data = await response.json()

            

            try:                
                # meme = random.choice(data["data"]["children"])
                # reply= meme["data"]
                # url= meme["data"]["url"]
                # if not any([
                #     url.endswith("png"),
                #     url.endswith("jpg"),
                #     url.endswith("jpeg"),
                #     url.endswith("gif"),
                #     ]):
                #     continue

                for post in data.get("data", {}).get("children", []):
                    url = post.get("data", {}).get("url")
                    meme= random.choice(data["data"]["children"])
                    reply= meme["data"]
                   
                logging.info(reply)
                return reply
            except KeyError:
                max_tries -= 1
                continue
            except TypeError:
                max_tries -= 1
                continue




async def main():
    meme = await get_meme("random")
    print(meme)

if __name__ == '__main__':
    asyncio.run(main())

