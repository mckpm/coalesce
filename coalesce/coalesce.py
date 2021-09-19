from coalesce import strategies
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed, ThreadPoolExecutor
from random import choice
import requests

def get(member_id, strategy, api_urls):
    """Call some APIs and coalesce the resulting data."""
    resps = call_apis(api_urls, member_id, strategy)
    return coalesce(resps, strategy)

def call_apis(api_urls, member_id, strategy:str=None):
    """Call some APIs and return data from their responses."""
    result = []
    urls = ['{}?member_id={}'.format(api, member_id)
            for api in api_urls]
    if strategy == 'random2':
        urls = [choice(urls)]

    executor = ThreadPoolExecutor()
    with FuturesSession(executor=executor) as session:
        futures = [session.get(url) for url in urls]
        for future in as_completed(futures):
            res = future.result()
            res.raise_for_status()
            result.append(res.json())

            if strategy == 'fastest':
                executor.shutdown(wait=False)
                for f in futures:
                    if not f.done():
                        f.cancel()
                break

    return result

def coalesce(resps, strategy: str):
    """Coalesce data according to a strategy."""
    result = {}
    if len(resps) == 0:
        return result

    # Choose strategy
    if strategy == 'min':
        strat = strategies.minimum
    elif strategy == 'max':
        strat = strategies.maximum
    elif strategy == 'frequent':
        strat = strategies.frequent
    elif strategy == 'random':
        strat = strategies.random
    elif strategy == '' or strategy == 'average':
        strat = strategies.average
    elif strategy == 'random2' or strategy == 'fastest':
        return resps[0]
    else:
        raise ValueError('Unknown strategy {}'.format(strategy))

    # Apply strategy
    return strat(resps)
