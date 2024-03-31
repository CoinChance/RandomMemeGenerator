
# app.py
import os
import io
import aiohttp
import logging
from functools import wraps
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timedelta

from utility.meme_fetcher import get_meme, topics_accepted
from flask import Flask, request, jsonify, current_app, Response


# Load environment variables from .env file
load_dotenv()


log_file = os.path.join(os.path.dirname(__file__), 'logs', 'app.log')
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)  

 # Get the value of the RATE_LIMIT and RATE_LIMIT_DURATION environment variables
RATE_LIMIT = int(os.environ.get('RATE_LIMIT', '5'))        # default 5
RATE_LIMIT_DURATION = int(os.environ.get('RATE_LIMIT_DURATION', '15'))        # default 15

WINDOW_DURATION = timedelta(minutes=RATE_LIMIT_DURATION)
request_log = []

def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Decorator function that adds rate limiting functionality to the wrapped function.

        Parameters:
        - func: The function to be wrapped.

        Returns:
        - The wrapped function.

        Description:
        This function is a decorator that adds rate limiting functionality to the wrapped function. It checks the number of requests made within a specified time window and if the limit is exceeded, it returns an error response. Otherwise, it records the request and calls the wrapped function.
        The rate limit is defined by the global variable RATE_LIMIT, which specifies the maximum number of requests allowed within a time window defined by WINDOW_DURATION. The request log is a list that stores the timestamps of each request made.
        If the number of requests made within the time window exceeds the rate limit, the function logs an error message and returns a JSON response with an error message and a status code of 429 (Too Many Requests). Otherwise, it records the current request in the request log and calls the wrapped function.
        Note: The request log is a global variable and should be initialized before using this decorator.
        """
        global request_log
        current_time = datetime.now()

        # Remove old entries from request log
        request_log = [r for r in request_log if current_time - r <= WINDOW_DURATION]

        if len(request_log) >= RATE_LIMIT:
            logging.error({"error": "Rate limit exceeded. Please try again later."})
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

        request_log.append(current_time)
        return func(*args, **kwargs)

    return wrapper



@app.route("/meme/<topic>", methods=['GET'])
async def meme(topic: str):
    logging.info('Endpoint hit: /meme/topic')
    logging.info('Topic Requested: ')
    logging.info(topic)
    if topic not in topics_accepted:
        topic = topic + "memes"

    logging.info('Topic Selected: ')
    logging.info(topic)
    meme = await get_meme(topic, logging=logging)
    #await do_statistics("meme")
    async with aiohttp.ClientSession() as session:
        async with session.get(meme["url"]) as resp:
            if resp.status != 200:
                logging.info({"error": "Couldn't fetch the meme!"})
                return jsonify({
                    "success": 0,
                    "data": {"errormessage": "Couldn't fetch the meme!"},
                }), 500
            else:
                meme_bytes = await resp.read()
                #await do_statistics("single_meme")
                return Response(io.BytesIO(meme_bytes), mimetype="image/png")


@app.route("/meme", methods=['GET'])
async def single_meme():
    logging.info('Endpoint hit: /meme')
    meme = await get_meme("random", logging=logging)

    async with aiohttp.ClientSession() as session:
        async with session.get(meme["url"]) as resp:
            if resp.status != 200:
                logging.info({"error": "Couldn't fetch the meme!"})
                return jsonify({
                    "success": 0,
                    "data": {"errormessage": "Couldn't fetch the meme!"},
                }), 500
            else:
                meme_bytes = await resp.read()
                #await do_statistics("single_meme")
                return Response(io.BytesIO(meme_bytes), mimetype="image/png")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
