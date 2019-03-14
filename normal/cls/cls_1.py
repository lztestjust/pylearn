from selenium.webdriver.common.by import By


class MyClass:
    """

    """

    LZ = 'lz'
    JUST = 'just'
    DO = 'do'
    IT = 'it'
    @staticmethod
    def get_by_attr(by):
        return getattr(By, by)

    @staticmethod
    def prase_dict(locator, params=None):
        """解析字典"""
        return locator.format(params or {})


__all__ = ['MyClass']

if __name__ == '__main__':
    res_ = MyClass.get_by_attr('ID')
    print(res_)
    print(getattr(MyClass, 'DO'))

    locator = '//div{}'
    params = 0
    res_ = MyClass.prase_dict(locator)
    print(res_)
