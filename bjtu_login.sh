# 获取无线网络接口名（假设接口名称为WLAN，你可以根据实际情况修改）
interface=$(ip -o -4 addr list | grep "10\." | awk '{print $2}')
if [ -z "$interface" ]; then
  echo "无法找到以 '10.' 开头的 IP 地址，请检查网络连接。"
  exit 1
fi

# 获取当前IP地址
wlan_user_ip=$(ip -o -4 addr list $interface | awk '{print $4}' | cut -d/ -f1)

# 获取当前MAC地址
wlan_user_mac=$(cat /sys/class/net/$interface/address | sed 's/://g')

# 其他固定参数
user_account=""     # 此处填写你的学号
user_password=""    # 此处填写你的上网密码
callback="dr1003"
login_method="1"
terminal_type="1"
lang="zh-cn"
v="1234"            # 随机数均可

# Step 1: 获取 fileVersion
versionPage=$(curl -s "https://login.bjtu.edu.cn/a79.htm")
fileVersion=$(echo "$versionPage" | grep -oP 'var fileVersion="\K\d+')

# Step 2: 使用 fileVersion 构造 URL 并获取 jsVersion （抓包得到的是4.2.1）
jsUrl="https://login.bjtu.edu.cn/a40.js?v=_$fileVersion"
jsFileContent=$(curl -s "$jsUrl")
jsVersion=$(echo "$jsFileContent" | grep -oP ";var jsVersion = '\K[0-9\.]+(?=')")

# Step 3: 构建登录URL并发送GET请求进行登录
loginUrl="https://login.bjtu.edu.cn:802/eportal/portal/login?callback=$callback&login_method=$login_method&user_account=$user_account&user_password=$user_password&wlan_user_ip=$wlan_user_ip&wlan_user_ipv6=&wlan_user_mac=$wlan_user_mac&wlan_ac_ip=&wlan_ac_name=&jsVersion=$jsVersion&terminal_type=$terminal_type&lang=$lang&v=$v&lang=zh"
curl -s "$loginUrl"
