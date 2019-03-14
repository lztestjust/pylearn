import enum
from enum import Enum
from enum import IntEnum
from enum import Flag
from enum import IntFlag


class Shake(Enum):

    JUST = '10'
    DO = 2
    IT = 3
    OK = 4


class Shake2(Enum):

    JUST = '1'
    DO = 2
    IT = 3
    OK = 4


class Shaka(IntEnum):
    JUST = '10'
    DO = 2
    IT = 3
    OK = 4


class Shaka2(IntEnum):
    JUST = '1'
    DO = 2
    IT = 3
    OK = 4


class Shakf(Flag):
    JUST = '1'
    DO = 2
    IT = 3
    OK = 4


class Shakif(IntFlag):
    JUST = 1
    DO = 2
    IT = 4
    OK = 8


def lz_enum():
    Animal = Enum('Animal', 'A B C D E')
    print(Animal)
    print(Animal.A)
    print(Animal.B)
    print(Animal.A.name)
    print(Animal.B.name)
    print(Animal.A.value)
    print(Animal.B.value)

if __name__ == '__main__':
    # print(help(enum))
    # print(help(Enum))
    # print(help(IntEnum))
    # #
    # lz_enum()
    #

    # # Shaka 与 Shake
    # print(Shake)
    # print(Shake.JUST)
    # print(Shaka == Shake)
    # print(Shaka.JUST == Shake.JUST)
    # print('名称：', Shaka.JUST.name == Shake.JUST.name)
    # print('值：', Shaka.JUST.value == Shake.JUST.value)
    # print('-----')
    # # Shaka
    # print(Shaka == Shaka2)
    # print(Shaka.JUST == Shaka2.JUST)
    # print('名称：', Shaka.JUST.name == Shaka2.JUST.name)
    # print('值：', Shaka.JUST.value == Shaka2.JUST.value)
    # print('-----')
    # # Shake
    # print(Shake == Shake2)
    # print(Shake.JUST == Shake2.JUST)
    # print('名称：', Shake.JUST.name == Shake2.JUST.name)
    # print('值：', Shake.JUST.value == Shake2.JUST.value)
    # print('------------------')
    #
    # print(Shake.JUST)
    # print(Shaka.JUST)
    # print(Shakf.JUST)
    # print('----')
    # for i in Shake:
    #     print(i.name, i.value)
    # print('-----')
    # for i in range(Shaka.JUST):
    #     print(i)
    # for i in range(Shaka.DO):
    #     print(i)
    # print('-----')
    # for i in range(Shakif.DO):
    #     print(i)
    # print('----------------')
    # m_ = {}
    # m_[Shake.JUST.name] = 'just'
    # print(m_)
    # print(not 0)

    #
    # print(Shakif.JUST & Shakif.DO)
    # print(Shakif.JUST | Shakif.DO)
    # print(Shakif.JUST ^ Shakif.DO)
    # print(~Shakif.JUST)

    ss = '123'
    ll = [1, 2]
    print(id(ss))
    print(id(ss))
    print(id(ll))
    print(id(ll.copy()))
    ll.clear()
    print(id(ll))
