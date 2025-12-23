import os
import time

import requests
from requests.exceptions import HTTPError


class BetaSeriesAPI:
    BASE_URL = "https://api.betaseries.com"
    API_VERSION = "3.0"
    USER_AGENT = "movie_recommender_system/1.0"

    def __init__(self, api_key, access_token=None):
        self.api_key = api_key
        self.access_token = access_token
        self.common_headers = {
            "X-BetaSeries-Version": self.API_VERSION,
            "User-Agent": self.USER_AGENT,
            "X-BetaSeries-Key": self.api_key,
        }
        if self.access_token:
            self.common_headers["Authorization"] = f"Bearer {self.access_token}"

    def _get_headers(self):
        return self.common_headers

    def _make_get_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        retries = 0
        backoff_factor = 0.5

        while retries < 3:
            try:
                response = requests.get(url, headers=headers, params=params)
                # Retry on server errors
                if 500 <= response.status_code < 600:
                    raise HTTPError(response=response)

                response.raise_for_status()
                return response
            except HTTPError as http_err:
                if 500 <= http_err.response.status_code < 600:
                    retries += 1
                    sleep_time = backoff_factor * (2**retries)
                    time.sleep(sleep_time)
                    continue
                raise
            except requests.RequestException:
                # Retry on connection errors
                retries += 1
                sleep_time = backoff_factor * (2**retries)
                time.sleep(sleep_time)
                continue

        msg = f"Max retries exceeded with url: {url}"
        raise HTTPError(msg)

    def get_shows_list(self, fields=None, limit=100, order=None, page=1):
        endpoint = "/shows/list"
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        if limit:
            params["limit"] = limit
        if order:
            params["order"] = order
        if page:
            params["page"] = page

        response = self._make_get_request(endpoint, params)
        return response.json()

    def get_movies_list(self, limit=100, order=None, page=1):
        endpoint = "/movies/list"
        params = {}
        if limit:
            params["limit"] = limit
        if order:
            params["order"] = order
        if page:
            params["page"] = page

        response = self._make_get_request(endpoint, params)
        return response.json()

    def get_movie_details(self, movie_id):
        endpoint = "/movies/movie"
        params = {"id": movie_id}

        response = self._make_get_request(endpoint, params)
        return response.json()
