import requests
import yaml
import logging

class ProxyProvider:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.proxies = []

    def fetch_proxies(self) -> None:
        """获取订阅内容"""
        try:
            headers = {
                'User-Agent': 'clash-verge/v2.2.3'
            }

            logging.info(f"Fetching subscription from {self.url}")

            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            config = yaml.safe_load(response.text)
            self.proxies = config.get('proxies', [])

        except requests.RequestException as e:
            logging.error(f"Failed to fetch subscription: {e}")

    def get_proxies(self) -> list:
        return self.proxies
    
    def get_name(self) -> str:
        return self.name