from conftest import SESSION
from lib.api_service_provider.api_constants import APIConstants


class APIService:
    _instance = None
    _session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._session = SESSION
            cls._instance._domain = APIConstants.DOMAIN
        return cls._instance

    @property
    def session(self):
        return self._session

    @property
    def domain(self):
        return self._domain

    def _build_url(self, endpoint):
        return f"{self.domain}/{endpoint}"

    def _default_headers(self, endpoint: str):
        """Default headers"""
        if endpoint.endswith(APIConstants.HTML_SUFFIX):
            return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
        else:
            return {
                'utcoffset': '240',
                'Content-Type': 'application/json',
                'Content-Language': 'en',
                'Accept': 'application/json',
            }

    def get(self, endpoint, params=None, headers=None, referer=None, origin=None):
        url = self._build_url(endpoint)
        headers = headers or self._default_headers(endpoint=endpoint)

        # Update headers if referer or origin are provided
        if referer:
            headers['referer'] = referer
        if origin:
            headers['origin'] = origin
        response = self.session.get(url, params=params, headers=headers)
        self._validate_response(response)
        return response

    def post(self, endpoint, data=None, json=None, headers=None, referer=None, origin=None, allow_redirects=False, params=None):
        url = self._build_url(endpoint)
        headers = headers or self._default_headers(endpoint=endpoint)

        # Update headers if referer or origin are provided
        if referer:
            headers['referer'] = referer
        if origin:
            headers['origin'] = origin
        response = self.session.post(url, data=data, json=json, headers=headers, allow_redirects=allow_redirects, params=params)
        self._validate_response(response)
        return response

    def put(self, endpoint, json=None, data=None, headers=None):
        url = self._build_url(endpoint)
        headers = headers or self._default_headers(endpoint=endpoint)
        response = self.session.put(url, json=json, headers=headers)
        self._validate_response(response)
        return response.json()

    def delete(self, endpoint, headers=None):
        url = self._build_url(endpoint)
        headers = headers or self._default_headers(endpoint=endpoint)
        response = self.session.delete(url, headers=headers)
        self._validate_response(response)
        return response

    def _validate_response(self, response):
        if response.status_code in [APIConstants.STATUS_INTERNAL_SERVER_ERROR, APIConstants.STATUS_BAD_REQUEST, APIConstants.STATUS_NOT_FOUND]:
            if APIConstants.LOGIN not in response.url:
                # Errors for Login with static old accounts are not handled (will throw Internal server error - Website Known issue)
                raise ValueError(f"Request failed with status code: {response.status_code}")

    def close_session(self):
        self.session.cookies.clear()
        self.session.close()
