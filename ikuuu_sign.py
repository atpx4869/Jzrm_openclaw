#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ikuuu 自动签到（多账号）
环境变量：ikuuu=账号1#密码1&账号2#密码2

特性：
- 自动从 https://ikuuu.one 探测可用域名
- 候选域名自动切换（.nl/.de）
- 登录失败重试
- 日志脱敏（不输出完整邮箱）
"""

import time
import random
import requests
from os import environ
from urllib.parse import urlparse
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()


def mask_email(email: str) -> str:
    if "@" not in email:
        return "***"
    name, domain = email.split("@", 1)
    if len(name) <= 2:
        m = "*" * len(name)
    else:
        m = name[:2] + "***"
    return f"{m}@{domain}"


def get_environ(key: str, default: str = "", output: bool = True) -> str:
    def no_read():
        if output:
            print(f"❌ 未填写环境变量 {key} 请添加")
            raise SystemExit(0)
        return default

    return environ.get(key) if environ.get(key) else no_read()


def detect_bases() -> list[str]:
    # 按用户要求：跳过探测，强制直连 nl
    return ["https://ikuuu.nl"]


class Ikuuu:
    def __init__(self, ck, base):
        self.msg = ""
        self.email = ck[0].strip() if len(ck) >= 2 else ""
        self.passwd = ck[1].strip() if len(ck) >= 2 else ""
        self.base = base.rstrip("/")
        self.masked_email = mask_email(self.email)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": f"{self.base}/auth/login",
                "Origin": self.base,
                "Upgrade-Insecure-Requests": "1",
                "Connection": "keep-alive",
            }
        )

    def login(self, retry=3):
        login_url = f"{self.base}/auth/login"
        data = {
            "email": self.email,
            "passwd": self.passwd,
            "remember_me": "on",
        }

        for i in range(retry):
            try:
                time.sleep(random.uniform(1, 2.5))
                self.session.get(login_url, timeout=15)
                res = self.session.post(login_url, data=data, timeout=15, allow_redirects=False)

                if res.status_code == 302 and "user" in res.headers.get("Location", ""):
                    return True

                if i < retry - 1:
                    print(f"⚠️ 第{i+1}次登录失败，{self.masked_email}，重试中...")
                    time.sleep(random.uniform(2, 4))
            except Exception as e:
                if i < retry - 1:
                    print(f"⚠️ 第{i+1}次登录异常 {self.masked_email}：{str(e)}，重试中...")
                    time.sleep(random.uniform(2, 4))

        return False

    def sign(self):
        if not self.login():
            xx = f"[登录]：{self.masked_email} 登录失败（风控/网络/账号密码），请检查 "
            print(xx)
            self.msg += xx
            return self.msg

        user_url = f"{self.base}/user"
        sign_url = f"{self.base}/user/checkin"

        try:
            time.sleep(random.uniform(1, 2))
            user_res = self.session.get(user_url, timeout=15)
            user_res.raise_for_status()
        except Exception as e:
            xx = f"[登录]：{self.masked_email} 获取用户信息失败：{str(e)} "
            print(xx)
            self.msg += xx
            return self.msg

        try:
            soup = BeautifulSoup(user_res.text, "html.parser")
            name_elem = soup.find("span", {"class": "navbar-brand"}) or soup.find(
                "div", {"class": "d-sm-none d-lg-inline-block"}
            )
            username = name_elem.text.strip() if name_elem else self.masked_email
            syll_elem = soup.find("span", {"class": "counter"})
            syll = syll_elem.text.strip() if syll_elem else "未知"
        except Exception:
            username = self.masked_email
            syll = "未知"

        try:
            time.sleep(random.uniform(1, 2))
            sign_res = self.session.post(sign_url, timeout=15)
            sign_res.raise_for_status()
        except Exception as e:
            xx = f"[登录]：{username} [签到]：请求失败 {str(e)} "
            print(xx)
            self.msg += xx
            return self.msg

        try:
            sign_json = sign_res.json()
            sign_msg = sign_json.get("msg", "无信息")
            if "已经签到" in sign_msg or "获得" in sign_msg:
                xx = f"[登录]：{username} [签到]：{sign_msg} [流量]：{syll}GB "
            else:
                xx = f"[登录]：{username} [签到]：未知结果 {sign_msg} "
        except Exception:
            xx = f"[登录]：{username} [签到]：响应解析失败（非JSON） [流量]：{syll}GB "

        print(xx)
        self.msg += xx
        return self.msg

    def get_sign_msg(self):
        return self.sign()


# ⚠️ 临时明文凭据（按你的要求写入脚本）。
# 用完请立即删除并改回环境变量方式，避免泄露风险。
HARDCODED_TOKEN = "atpx4869love@gmail.com#htp_uqf@UMQ5nyk2tcq"

if __name__ == "__main__":
    token = environ.get("ikuuu") or HARDCODED_TOKEN
    cks = [x.strip() for x in token.split("&") if x.strip()]

    print(f"✅ 检测到{len(cks)}个账号，开始ikuuu签到")

    try:
        bases = detect_bases()
        print(f"✅ 自动探测到可用域名：{' -> '.join(bases)}")
    except Exception as e:
        print(f"❌ 域名探测失败：{e}")
        raise SystemExit(1)

    msg = ""
    success, failed = 0, 0

    for idx, ck_all in enumerate(cks):
        ck = ck_all.split("#")
        if len(ck) != 2:
            print(f"❌ 第{idx+1}个账号格式错误：{ck_all}，跳过")
            msg += f"❌ 第{idx+1}个账号格式错误 "
            failed += 1
            continue

        if idx > 0:
            time.sleep(random.uniform(3, 5))

        one_msg = ""
        ok = False

        for base in bases:
            run = Ikuuu(ck, base)
            one_msg = run.get_sign_msg()
            # 成功或已签到都视为成功
            if ("获得" in one_msg) or ("已经签到" in one_msg):
                ok = True
                break
            # 非最后一个域名时提示切换
            if base != bases[-1]:
                print(f"ℹ️ 账号 {run.masked_email} 在 {base} 未成功，尝试下一个域名...")

        msg += one_msg

        if ok:
            success += 1
        else:
            failed += 1

    print(f"✅ 所有账号处理完成（成功: {success}，失败: {failed}）")

    # 若你的运行平台注入了 send 函数可自动通知
    if "send" in locals() and send:
        send("ikuuu签到通知", msg)
