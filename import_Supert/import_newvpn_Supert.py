"""
 c--Y
pip install requests  pandas openpyxl
"""
import requests
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_super_ts_id(base_url, token):
    """获取 superTsId（只取第一个）"""
    url = f"{base_url}/api/admin/terminal/super-ts/list"
    headers = {"token": token}

    resp = requests.get(url, headers=headers, verify=False)
    data = resp.json()

    if data.get("code") != 0:
        raise Exception(f"获取 superTsId 失败: {resp.text}")

    super_list = data["data"]["list"]
    if not super_list:
        raise Exception("未找到可用的 superTsId")

    return super_list[0]["id"]

def import_from_excel(base_url, token, excel_path):
    # 读取 Excel
    df = pd.read_excel(excel_path,engine='openpyxl')

    # 检查必要列
    required_cols = ["name", "ip", "protocol", "port"]
    for col in required_cols:
        if col not in df.columns:
            raise Exception(f"Excel 缺少列: {col}")

    # 获取 superTsId
    super_ts_id = get_super_ts_id(base_url, token)
    print(f"[INFO] 获取到 superTsId = {super_ts_id}")

    headers = {
        "Content-Type": "application/json",
        "token": token
    }
    add_url = f"{base_url}/api/admin/terminal/add"

    for idx, row in df.iterrows():
        # 跳过空行
        if pd.isna(row["name"]) and pd.isna(row["ip"]):
            continue

        # 构造数据
        data = {
            "name": str(row["name"]) if not pd.isna(row["name"]) else "",
            "protocol": str(row["protocol"]) if not pd.isna(row["protocol"]) else "ssh",
            "superTsId": super_ts_id,
            "hostName": str(row["ip"]) if not pd.isna(row["ip"]) else "",
            "port": int(row["port"]) if not pd.isna(row["port"]) else 22
        }

        # 如果 username 不为空，则加上
        if "username" in df.columns and not pd.isna(row["username"]):
            data["username"] = str(row["username"])

        try:
            resp = requests.post(add_url, json=data, headers=headers, verify=False)
            resp.raise_for_status()
        except Exception as e:
            print(f"✗ 导入失败: {row['name']} ({row['ip']}) → {e}")
            continue

        # 根据返回内容判断是否成功
        result = resp.json()
        if result.get("code") == 0:
            print(f"✓ 导入成功: {row['name']} ({row['ip']})")
        else:
            print(f"✗ 导入失败: {row['name']} ({row['ip']}) → {result.get('message')}")

if __name__ == "__main__":
    print("=== WebVPN 自动导入工具 ===")
    base_url = input("请输入访问地址（例如 https://webvpn.richcache.com:40000 ）: ").strip()
    token = input("请输入浏览器复制的 token: ").strip()
    excel_path = input("请输入 Excel 文件路径: ").strip()

    import_from_excel(base_url, token, excel_path)
    print("=== 全部导入完成 ===")
