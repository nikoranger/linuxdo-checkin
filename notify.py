"""
通知模块 - PushPlus
"""

import os
from loguru import logger
from curl_cffi import requests

PUSHPLUS_URL = "https://www.pushplus.plus/send"


class NotificationManager:
    """统一通知管理器"""

    def __init__(self):
        self.pushplus_token = os.environ.get("PUSHPLUS_TOKEN")

    def send_pushplus(self, title: str, message: str):
        """发送 PushPlus 通知"""
        if not self.pushplus_token:
            logger.info("未配置 PUSHPLUS_TOKEN，跳过通知发送")
            return False

        try:
            response = requests.post(
                PUSHPLUS_URL,
                json={
                    "token": self.pushplus_token,
                    "title": title,
                    "content": message,
                    "template": "txt",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("code") != 200:
                logger.error(f"PushPlus 推送失败: {data.get('msg', data)}")
                return False
            logger.success("PushPlus 推送请求成功")
            return True
        except Exception as e:
            logger.error(f"PushPlus 推送失败: {str(e)}")
            return False
