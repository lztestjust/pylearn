import pprint


if __name__ == '__main__':
    ll = ['div', 'h', 'b', 'br', 'a', 'div', 'h', 'b']
    ll.insert(0, ll[:])
    pprint.pprint(ll, indent=4)
    url = 'https://tieba.baidu.com/f?kw=%s&pn=%s'
    menu = 'meinv'
    offset = 50
    print(url % (menu, offset))