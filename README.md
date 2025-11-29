webvpn_crawler/
│── main.py               # 程序入口
│── crawler.py            # 爬虫代码（优化封装）
│── ui/
│     ├── window.py       # UI 主界面
│── resources/
│     ├── style.qss       # 美化样式

⭐ 如需添加图标（Windows）
pyinstaller --windowed --onefile --icon=app.ico main.py

⭐ 如需添加图标（Mac）
pyinstaller --windowed --name WebVPNCrawler --icon=resources/icon.icns main.py

#安装openpyxl  requests   bs4  pandas   PySide6 》 pip3 install 
