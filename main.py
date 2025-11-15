import requests
import yaml
import os
from typing import Dict, Any
from flask import Flask, send_file
import tempfile

app = Flask(__name__)

class ClashConverter:
    def __init__(self, subscription_url: str):
        self.subscription_url = subscription_url
        self.config: Dict[str, Any] = {}

    def fetch_subscription(self) -> None:
        """获取订阅内容"""
        try:
            headers = {
                'User-Agent': 'clash/v1.7.5'
            }
            response = requests.get(self.subscription_url, headers=headers)
            response.raise_for_status()
            self.config = yaml.safe_load(response.text)
            # 删除原始配置中的 rules
            if 'rules' in self.config:
                del self.config['rules']
            
            # 修改 proxy-groups，只保留第一个元素
            if 'proxy-groups' in self.config and len(self.config['proxy-groups']) > 0:
                first_group = self.config['proxy-groups'][0]
                first_group['name'] = 'PROXY'
                self.config['proxy-groups'] = [first_group]
        except requests.RequestException as e:
            print(f"获取订阅失败: {e}")
            raise

    def merge_custom_config(self, custom_config_path: str) -> None:
        """合并自定义配置"""
        try:
            with open(custom_config_path, 'r', encoding='utf-8') as f:
                custom_config = yaml.safe_load(f)
            
            # 合并配置
            for key, value in custom_config.items():
                if key in self.config and isinstance(value, list) and isinstance(self.config[key], list):
                    # 如果是列表类型，则合并列表
                    self.config[key].extend(value)
                else:
                    # 其他情况直接覆盖
                    self.config[key] = value
        except IOError as e:
            print(f"读取自定义配置失败: {e}")
            raise
        except yaml.YAMLError as e:
            print(f"解析自定义配置失败: {e}")
            raise

    def save_config(self, output_path: str) -> None:
        """保存配置到文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    self.config,
                    f,
                    allow_unicode=True,
                    sort_keys=False,
                    indent=2,
                    default_flow_style=False,
                    width=float("inf")
                )
        except IOError as e:
            print(f"保存配置失败: {e}")
            raise


@app.route('/sub/<token>')
def convert_subscription(token):
    try:

        # check token if corcurrent.
        sys_token = os.getenv('TOKEN')

        if sys_token != token:
            return f"get out!", 401

        # 从环境变量获取订阅链接
        subscription_url = os.getenv('SUBSCRIPTION_URL')
        if not subscription_url:
            return "环境变量 SUBSCRIPTION_URL 未设置", 500

        # 创建临时文件用于保存配置
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_path = temp_file.name

        # 执行转换
        converter = ClashConverter(subscription_url)
        converter.fetch_subscription()
        converter.merge_custom_config('custom.yaml')  # 确保custom.yaml文件存在
        converter.save_config(temp_path)

        # 发送文件
        return send_file(
            temp_path,
            mimetype='application/x-yaml',
            as_attachment=True,
            download_name='config.yaml'
        )

    except Exception as e:
        return f"处理失败: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)