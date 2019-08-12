import os

# 生成当前文件上一级的绝对路径==>../../../project
BASE_DIRS = os.path.dirname(__file__)
# 参数
options = {
    'port': 8080,

}
# 数据库配置
mysql = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '123456',
    'dbName': 'tornado'
}
# 配置
settings = {
    'static_path': os.path.join(BASE_DIRS, 'static'),
    'template_path': os.path.join(BASE_DIRS, 'templates'),
    'debug': True,  # 修改代码，自动重启服务
}
