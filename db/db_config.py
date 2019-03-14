import configparser
import os

# 当前文件夹路径
cur_dir = os.path.split(os.path.realpath(__file__))[0]

# 配置文件
file_name = 'db_config.ini'
file_path = os.path.join(cur_dir, file_name)
cfg_parser = configparser.ConfigParser()
cfg_parser.read(file_path)


class MySQLConfig:

    @staticmethod
    def get_host():
        return cfg_parser.get('mysql', 'host')
    @staticmethod
    def get_user():
        return cfg_parser.get('mysql', 'user')
    @staticmethod
    def get_password():
        return cfg_parser.get('mysql', 'password')
    @staticmethod
    def get_database():
        return cfg_parser.get('mysql', 'database')
    @staticmethod
    def get_port():
        return cfg_parser.get('mysql', 'port')

    @staticmethod
    def get_option(option: str):
        return cfg_parser.get('mysql', option)


if __name__ == '__main__':
    # res_ = cfg_parser.get('mysql', 'host')
    res_ = MySQLConfig.get_host()
    print(res_)
    res_ = MySQLConfig.get_user()
    print(res_)
    res_ = MySQLConfig.get_password()
    print(res_)
    res_ = MySQLConfig.get_database()
    print(res_)
    res_ = MySQLConfig.get_port()
    print(res_)
    res_ = MySQLConfig.get_option('host')
    print(res_)
