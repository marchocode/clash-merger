import yaml
from typing import Dict,Any

class ClashMerger:
    
    def __init__(self, providers: list):
        self.providers = providers
        self.config = {}
        self.proxies = []
        self.proxy_groups = []

    def merge(self) -> None:

        with open("base.yaml", 'r', encoding='utf-8') as f:
            base = yaml.safe_load(f)
            self.config = base

        for provider in self.providers:
            provider.fetch_proxies()

            li = provider.get_proxies()
            
            if len(li) == 0:
                continue

            for item in li:
                self.proxies.append(item)

            self.process_group(provider)

        self.process_auto_group()
        # main proxy group
        self.process_proxy_group()

        self.config['proxies'] = self.proxies
        self.config['proxy-groups'] = self.proxy_groups

    def process_auto_group(self) -> None:
        
        auto = {}
        auto['name'] = "AUTO"
        auto['type'] = "url-test"
        auto['proxies'] = []

        for proxies in self.proxies:
            auto['proxies'].append(proxies['name'])

        auto['url'] = "http://www.gstatic.com/generate_204"
        auto['interval'] = 300

        self.proxy_groups.append(auto)

    def process_proxy_group(self) -> None:

        proxy = {}
        proxy['name'] = "PROXY"
        proxy['type'] = "select"
        proxy['proxies'] = []

        for group in self.proxy_groups:
            proxy['proxies'].append(group['name'])

        self.proxy_groups.insert(0, proxy)

    def process_group(self, provider) -> None:
        
        group = {}
        group['name'] = provider.get_name()
        group['type'] = "select"
        group['proxies'] = []

        for item in provider.get_proxies():
            group['proxies'].append(item['name'])

        self.proxy_groups.append(group)


    def dump(self) -> str:

        return yaml.dump(
            self.config,
            allow_unicode=True,
            sort_keys=False,
            indent=2,
            default_flow_style=False,
            width=float("inf")
        )
