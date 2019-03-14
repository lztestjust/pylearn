import threading
from time import sleep


class MyThread(threading.Thread):
    """自定义线程"""

    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        sleep(1)
        print('当前线程名称：', self.name)
        sleep(1)


if __name__ == '__main__':
    # print(help(threading.Thread))

    th1 = MyThread()
    thread_name_lst = ['线程1', '线程2', '线程3', '线程4', '线程5']
    thread_obj_lst = []
    for i in thread_name_lst:
        th = MyThread()
        th.setName(i)
        th.start()
        thread_obj_lst.append(th)
    print('主线程结束！')

    # print(thread_obj_lst)
