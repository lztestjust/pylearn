import copy


if __name__ == '__main__':
    ii = 123
    ss = 123
    ll = [1, 2, 3]
    mm = {1: 123}

    print(id(ii))
    print(id(ss))
    print(id(ll))
    print(id(ll.copy()))
    print(id(mm))
    print(id(mm.copy()))
    ii = 124
    print('-----')
    print(id(ii))
    print(ll)
    print(mm)
    ll.clear()
    mm.clear()
    print(id(ll))
    print(id(mm))
    ll.append(12)
    print(id(ll))
    print(ll)
    print(mm)