import os


def dir_lst(fp: str):
    root = '%s%s%s' % ('..', os.sep, fp)
    print(os.path.dirname(root))
    for director, subdirnames, filenames in os.walk(root):
        print(director)
        for i in subdirnames:
            print('dir name', i)
        for i in filenames:
            print('file name', i)


if __name__ == '__main__':
    fp = r'lzfileaction'
    dir_lst(fp)
