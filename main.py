import sys
import os
import urllib.parse
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
import json


class NetworkLoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.config_path = os.path.expanduser(f'~/.bjtu_login_config.json')

        # Try to load saved credentials
        saved_credentials = self.load_credentials()

        # Attempt automatic login if credentials exist
        if saved_credentials:
            try:
                if self.perform_login(
                        saved_credentials['account'],
                        saved_credentials['password']
                ):
                    sys.exit(0)  # Exit if login successful
            except Exception:
                pass  # If auto-login fails, show GUI

        # Show GUI if no saved credentials or login fails
        self.initUI()

    def initUI(self):
        self.setWindowTitle('BJTU 网络登录')

        screen = QApplication.primaryScreen()
        screen_size = screen.size()

        # 计算窗口应放置的位置
        x = (screen_size.width() - self.width()) // 2
        y = (screen_size.height() - self.height()) // 2

        self.setGeometry(x, y, 300, 200)

        layout = QVBoxLayout()

        # 账号输入
        self.account_label = QLabel('账号:')
        self.account_input = QLineEdit()
        layout.addWidget(self.account_label)
        layout.addWidget(self.account_input)

        # 密码输入
        self.password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # 登录按钮
        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.manual_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def load_credentials(self):
        """Load saved credentials from a JSON file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def save_credentials(self, account, password):
        """Save credentials to a JSON file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump({
                    'account': account,
                    'password': password
                }, f)
            # Set file permissions to be readable/writable only by the owner
            os.chmod(self.config_path, 0o600)
        except Exception as e:
            QMessageBox.warning(self, '保存错误', f'无法保存凭据: {str(e)}')

    def manual_login(self):
        """Handle login from GUI input."""
        account = self.account_input.text()
        password = self.password_input.text()

        if self.perform_login(account, password):
            # Save credentials if login successful
            self.save_credentials(account, password)
            self.close()
        else:
            self.initUI()

    def perform_login(self, account, password):
        # URL编码密码
        encoded_password = urllib.parse.quote(password)

        # 构建登录URL
        login_url = (
            f"https://login.bjtu.edu.cn:802/eportal/portal/login?callback=dr1006&"
            f"login_method=1&user_account={account}&user_password={encoded_password}&"
            f"wlan_user_ip=10.60.41.247&wlan_user_ipv6=&wlan_user_mac=000000000000&"
            f"wlan_ac_ip=&wlan_ac_name=&jsVersion=4.2.1&terminal_type=1&"
            f"lang=zh-cn&v=8486&lang=zh"
        )

        try:
            # 发送登录请求
            response = requests.get(login_url, allow_redirects=True, timeout=100)
            # 检查登录结果
            if response.status_code == 200:
                # 解析返回的JSONP数据
                jsonp_text = response.text
                json_str = jsonp_text[jsonp_text.index('(') + 1:jsonp_text.rindex(')')]
                result = json.loads(json_str)
                msg = result['msg']

                if msg == '账号或密码错误，请检查!':
                    QMessageBox.warning(self, '登录失败', '账号或密码错误，请检查!')

                    return False
                elif msg == 'Portal协议认证成功！':
                    QMessageBox.information(self, '提示', '网络登录成功!')
                    return True
                elif '已经在线！' in msg:
                    QMessageBox.information(self, '提示',
                                            '已经登录\n提示此信息时可能使原本连接的校园网断开，倘若断开，则在运行一次程序')
                    return True
                else:
                    QMessageBox.warning(self, '登录失败', f'登录失败，原因: {msg}')
                    return False
            else:
                QMessageBox.warning(self, '登录失败', f'登录失败，状态码: {response.status_code}')
                return False

        except Exception as e:
            QMessageBox.critical(self, '错误', f'登录失败: {str(e)}')
            return False


def main():
    app = QApplication(sys.argv)
    login_window = NetworkLoginApp()
    login_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
