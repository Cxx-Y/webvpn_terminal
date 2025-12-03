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

"""
  import_Supert 目录是导入会使用到的程序，跟main程序不冲突 main是旧版导出  import是新版导入 dist有mac（m1）版本的app
  导入只需下载import_Supert目录执行文件
"""
