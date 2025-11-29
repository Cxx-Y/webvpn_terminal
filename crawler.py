import requests
from bs4 import BeautifulSoup
import pandas as pd


def run_crawler(domain, username, password, output_file="webterminals.xlsx", log=None):
    """
    log: 可传一个 UI 回调函数，log("xxx") 用于界面打印信息
    """

    def log_print(msg):
        print(msg)
        if log:
            log(msg)

    BASE = f"https://{domain}"
    LOGIN_ENTRY_URL = f"{BASE}/login"
    LOGIN_POST_URL = f"{BASE}/users/sign_in"
    LIST_URL_TEMPLATE = f"{BASE}/web_terminals/all?page={{page}}"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/134.0.0.0 Safari/537.36",
    }

    def login_and_get_session():
        session = requests.Session()
        session.trust_env = False
        session.headers.update(HEADERS)

        resp = session.get(LOGIN_ENTRY_URL, allow_redirects=True)
        soup = BeautifulSoup(resp.text, "html.parser")

        token_input = soup.find("input", {"name": "authenticity_token"})
        if not token_input:
            raise Exception("❌ 获取 authenticity_token 失败")

        token = token_input.get("value")

        payload = {
            "authenticity_token": token,
            "user[login]": username,
            "user[password]": password,
            "user[dymatice_code]": "unknown",
            "user[otp_with_capcha]": "false",
            "commit": "登录 Login"
        }

        resp = session.post(LOGIN_POST_URL, data=payload, allow_redirects=True)
        if resp.status_code not in (200, 302):
            raise Exception("❌ 登录失败")

        log_print("✔ 登录成功")
        return session

    def get_total_pages(session):
        first_page = session.get(LIST_URL_TEMPLATE.format(page=1))
        soup = BeautifulSoup(first_page.text, "html.parser")

        pagination = soup.find("div", class_="pagination")
        last_page_num = 1

        if pagination:
            page_nums = [int(a.text) for a in pagination.find_all("a") if a.text.isdigit()]
            if page_nums:
                last_page_num = max(page_nums)

        log_print(f"✔ 共 {last_page_num} 页")
        return last_page_num

    def crawl_pages(session, total_pages):
        results = []
        for p in range(1, total_pages + 1):
            url = LIST_URL_TEMPLATE.format(page=p)
            log_print(f"➡ 正在爬取第 {p} 页")

            resp = session.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")

            tbody = soup.find("tbody", class_="sortable")
            if not tbody:
                continue

            for tr in tbody.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 5:
                    continue

                row = {
                    "名称": tds[0].get_text(strip=True),
                    "IP": tds[1].get_text(strip=True),
                    "协议": tds[2].get_text(strip=True),
                    "端口": tds[3].get_text(strip=True),
                    "用户名": tds[4].get_text(strip=True),
                }
                results.append(row)

        return results

    def save_to_excel(data, filename):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        log_print(f"✔ 已保存为: {filename}")

    session = login_and_get_session()
    total_pages = get_total_pages(session)
    data = crawl_pages(session, total_pages)
    save_to_excel(data, output_file)
