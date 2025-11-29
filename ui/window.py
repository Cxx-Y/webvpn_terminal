from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QTextEdit, QVBoxLayout, QHBoxLayout
)
from crawler import run_crawler


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WebVPN 超级终端复制粘贴工具")
        self.setMinimumWidth(420)

        # ────────── 控件 ──────────
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("例如：webvpn.xxxxx.com")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("webvpn本地登录账号")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("选择 Excel 导出路径...")

        self.btn_choose = QPushButton("选择文件…")
        self.btn_choose.clicked.connect(self.choose_file)

        self.btn_run = QPushButton("Start crawling-文明")
        self.btn_run.clicked.connect(self.start_crawl)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        # ────────── 布局 ──────────
        form = QVBoxLayout()

        form.addWidget(QLabel("域名："))
        form.addWidget(self.domain_input)

        form.addWidget(QLabel("账号："))
        form.addWidget(self.username_input)

        form.addWidget(QLabel("密码："))
        form.addWidget(self.password_input)

        h = QHBoxLayout()
        h.addWidget(self.file_path_input)
        h.addWidget(self.btn_choose)
        form.addLayout(h)

        form.addWidget(self.btn_run)
        form.addWidget(QLabel("日志输出："))
        form.addWidget(self.log_box)

        self.setLayout(form)

    # ----------------------------------------------------------------------
    def choose_file(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "选择导出 Excel 文件", "webterminals.xlsx", "Excel (*.xlsx)"
        )
        if file:
            self.file_path_input.setText(file)

    # ----------------------------------------------------------------------
    def log(self, msg):
        self.log_box.append(msg)

    # ----------------------------------------------------------------------
    def start_crawl(self):
        domain = self.domain_input.text().strip()
        user = self.username_input.text().strip()
        pwd = self.password_input.text().strip()
        path = self.file_path_input.text().strip()

        if not all([domain, user, pwd, path]):
            self.log("❌ 请填写所有字段")
            return

        self.log("➡ 正在执行爬虫...")

        try:
            run_crawler(domain, user, pwd, path, log=self.log)
            self.log("🎉 任务完成！")
        except Exception as e:
            self.log(f"❌ 错误：{e}")
