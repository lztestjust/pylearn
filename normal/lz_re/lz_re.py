import re
import os


def go():
    file_dir = r'C:\Users\lztes\Desktop\dazon'
    file_css_name = 'svg_css.css'
    file_name = 'svg.html'
    file_name2 = 'svg2.html'
    file_name3 = 'svg3.html'
    file_name4 = 'svg4.html'

    file_css_path = os.path.join(file_dir, file_css_name)
    file_path = os.path.join(file_dir, file_name)
    file_path2 = os.path.join(file_dir, file_name2)
    file_path3 = os.path.join(file_dir, file_name3)
    file_path4 = os.path.join(file_dir, file_name4)
    with open(file_css_path, 'r', encoding='utf-8') as f_css, \
            open(file_path, 'r', encoding='utf-8') as f, \
            open(file_path2, 'r', encoding='utf-8') as f2, \
            open(file_path3, 'r', encoding='utf-8') as f3, \
            open(file_path4, 'r', encoding='utf-8') as f4:
        data_css_txt = f_css.read()
        data_txt = f.read()
        data_txt2 = f2.read()
        data_txt3 = f3.read()
        data_txt4 = f4.read()

    # width
    width_pattern_str = '<style>.*font-size:(.*?)px;'
    width_pattern_txt = re.findall(width_pattern_str, data_css_txt)
    print(width_pattern_txt[0])

    # svg_para_lst
    svg_pattern_str = '<path id="(.*?)" d="(.*?) (.*?) (.*?)"/>'
    svg_pattern_txt = re.findall(svg_pattern_str, data_txt)
    data_svg_index_m = {}
    for i in svg_pattern_txt:
        # print(i)
        data_svg_index_m.setdefault(i[0], int(i[2]))
    print(data_svg_index_m)
    # svg 中文
    svg_txt_pattern_str = '<textPath xlink:href="#(\d*?)" textLength="(.*?)">(.*?)</textPath>'
    svg_txt_pattern_txt = re.findall(svg_txt_pattern_str, data_txt)
    data_svg_txt_m = {}
    for i in svg_txt_pattern_txt:
        # print(i)
        data_svg_txt_m.setdefault(i[0], [int(i[1]), i[2]])
    print(data_svg_txt_m)
    # svg_css 背景图 标签
    svg_css_pattern_str = '\.(\w*?){background:(.*?)px (.*?)px;}'
    svg_css_pattern_txt = re.findall(svg_css_pattern_str, data_txt2)
    data_svg_css_m = {}
    # print(len(svg_css_pattern_txt))
    for i in svg_css_pattern_txt:
        # print(i)
        try:
            data_svg_css_m.setdefault(i[0], {'x': int(float(i[1].lstrip('-'))), 'y': int(float(i[2].lstrip('-')))})
        except:
            print(i)
    print(data_svg_css_m)

    # #
    # svg_css_key_str = 'span\[class\^="(.*?)"]'
    # svg_css_key_txt = re.findall(svg_css_key_str, data_txt2)
    # for i in svg_css_key_txt:
    #     print(i)

    data_m = {}
    key_value = len(data_svg_index_m)
    for i in data_svg_css_m:
        print(data_svg_css_m[i])
        for j in data_svg_index_m:
            # y 坐标大于
            if data_svg_css_m[i]['y'] <= data_svg_index_m[j]:
                key_value = j
                break
        # print(key_value)
        # value = data_svg_css_m[i]['x']
        value = int(data_svg_css_m[i]['x'] / int(width_pattern_txt[0]))
        print(value)
        print(data_svg_txt_m[str(key_value)][1])
        print(data_svg_txt_m[str(key_value)][1][value])
        # data_m.setdefault(i, data_svg_txt_m[key_value][1][value])


def svg_css_to_dict(txt: str, slice_str: str = None, slice_start_str: str = None, slice_pattern_str: str = None,
                    coordinate_pattern_str: str = None):
    """svg css 文件背景图坐标字典化

    1、将 css 文件切片，（css 文件中存在多个 svg 文件链接，切片后各自的坐标域）
    2、按照规则提取坐标生成字典

    :parameter:
        txt: svg css 文件字符串文本
        slice_str: 切片规则字符串，txt 的切片规则
        slice_start_str: 切片起始字符串，切片后的列表中个字符串的起始标志（用于识别全局和局部变量）
        slice_pattern_str: 从切片中获取局部属性标志的正则表达式规则
        coordinate_pattern_str: 从切片中获取坐标属性标志的正则表达式规则
    """
    # 返回值的字典
    data_svg_css_temp_m = {}

    # 切片规则
    if slice_str is None:
        slice_str = 'span'
    if slice_start_str is None:
        slice_start_str = '[class'
    # 正则表达式规则
    if slice_pattern_str is None:
        slice_pattern_str = '\[class.*?="(.*?)"'
    if coordinate_pattern_str is None:
        coordinate_pattern_str = '\.(\w*?){background:(.*?)px (.*?)px;}'
    # 全部属性
    global_area = 'global'
    # 开始切片
    svg_css_slice = txt.split(slice_str)
    # 遍历所有切片
    for i in svg_css_slice:
        # 开始字符串符合的为局部属性
        if i.startswith(slice_start_str):
            slice_pattern = re.findall(slice_pattern_str, i)
            global_area = slice_pattern[0]
        # 背景图 标签
        coordinate_pattern = re.findall(coordinate_pattern_str, i)
        data_svg_css_m = {}
        for j in coordinate_pattern:
            # print(i)
            try:
                data_svg_css_m.setdefault(j[0],
                                          {'x': int(float(j[1].lstrip('-'))), 'y': int(float(j[2].lstrip('-')))})
            except:
                print(i)
        data_svg_css_temp_m.setdefault(global_area, data_svg_css_m)
    # for i in data_svg_css_temp_m:
    #     print(i, data_svg_css_temp_m[i])
    return data_svg_css_temp_m


def svg_css_to_dict_global(txt: str, coordinate_pattern_str: str=None):
    """svg css 文件背景图坐标字典化"""
    data_m = {}

    # 背景图正则表达式
    if coordinate_pattern_str is None:
        coordinate_pattern_str = '\.(\w*?){background:(.*?)px (.*?)px;}'
    # 背景图列表
    coordinate_pattern = re.findall(coordinate_pattern_str, txt)
    for j in coordinate_pattern:
        try:
            if j[0][:3] not in data_m:
                data_m.setdefault(j[0][:3], {})
            data_m.get(j[0][:3]).setdefault(j[0], {'x': int(float(j[1].lstrip('-'))), 'y': int(float(j[2].lstrip('-')))})
        except:
            print('背景图字典化存在错误！txt_code=%s' % j)

    return data_m


def svg_url_from_css(txt: str, flag_pattern_str: str=None, url_pattern_str: str=None):
    """
    从 svg css 文件中获取 svg 文件链接及标签
    :param txt:
    :param url_pattern_str:
    :return:
    """

    if flag_pattern_str is None:
        flag_pattern_str = 'span.*?url(.*?)'
    if url_pattern_str is None:
        url_pattern_str = '\[class.*?="(.*?)"'





def svg_file_to_dict(txt: str, font_size: int = None, font_pattern_str: str = None,
                     x_pattern_str: str = None, y_pattern_str: str = None):
    """svg 文件字典化

    使用 正则表达式规则直接获取文件中各项 x 和 y 轴坐标，并字典化返回

    :parameter
        txt: svg 文件文本
        font_size: svg 文件的背景图宽度
        font_pattern_str: 获取 svg 文件背景图宽度正则表达式
        x_pattern_str:  获取 x 坐标正则表达式
        y_pattern_str:  获取 y 坐标正则表达式

    """
    # 返回的字典
    data_m = {}

    # 正则表达式规则
    if font_pattern_str is None:
        font_pattern_str = '<style>.*font-size:(.*?)px;'
    if x_pattern_str is None:
        x_pattern_str = '<path id="(.*?)" d="(.*?) (.*?) (.*?)"/>'
    if y_pattern_str is None:
        y_pattern_str = '<textPath xlink:href="#(\d*?)" textLength="(.*?)">(.*?)</textPath>'
    # 字体大小
    if font_size is None:
        width_pattern_txt = re.findall(font_pattern_str, txt)
        font_size = int(width_pattern_txt[0])
    # print(font_size)
    # x 轴坐标
    svg_pattern_txt = re.findall(x_pattern_str, txt)
    data_svg_index_m = {}
    for i in svg_pattern_txt:
        data_svg_index_m.setdefault(i[0], int(i[2]))
    # print(data_svg_index_m)
    # y 轴坐标
    svg_txt_pattern_txt = re.findall(y_pattern_str, txt)
    data_svg_txt_m = {}
    for i in svg_txt_pattern_txt:
        data_svg_txt_m.setdefault(i[0], [int(i[1]), i[2]])
    # print(data_svg_txt_m)
    # 数据字典化
    for i in data_svg_index_m:
        data_m.setdefault(data_svg_index_m.get(i), data_svg_txt_m.get(i)[1])
    # print(data_m)

    return {'font_size': font_size, 'data': data_m}


def svg_file_to_dict_without_x_axis(txt: str, font_size: int=None, font_pattern_str: str=None, y_pattern_str: str=None):
    """svg 文件字典化

    使用正则表达式规则直接获取文件中各项 y 轴坐标，并字典化返回

    :param txt: svg文件文本
    :param font_size: 文件背景图宽度
    :param font_pattern_str: 获取 svg 文件背景图宽度正则表达式
    :param y_pattern_str: 获取 y 坐标正则表达式
    :return:
    """
    # 返回的字典
    data_m = {}

    # 正则表达式规则
    if font_pattern_str is None:
        font_pattern_str = '<style>.*font-size:(.*?)px;'
    if y_pattern_str is None:
        y_pattern_str = '<text.*y="(\w*?)".*?>(.*?)</text>'
    # 字体大小
    if font_size is None:
        width_pattern_txt = re.findall(font_pattern_str, txt)
        font_size = int(width_pattern_txt[0])
    # print(font_size)
    # y 轴坐标
    svg_txt_pattern_txt = re.findall(y_pattern_str, txt)
    data_svg_txt_m = {}
    for i in svg_txt_pattern_txt:
        data_svg_txt_m.setdefault(int(i[0]), i[1])
    # print(data_svg_txt_m)
    # 数据字典化
    data_m.update({'font_size': font_size, 'data': data_svg_txt_m})

    return data_m


def svg_file_bind_dict(txt: str, txt_name: str, font_size: int = None, font_pattern_str: str = None,
                       x_pattern_str: str = None, y_pattern_str: str = None):
    """svg 文件字典化

    使用正则表达式规则直接获取文件中各项 x 和 y 轴坐标，并字典化返回

    :parameter
        txt: svg 文件文本
        txt_name: svg 文件标志名称
        font_size: svg 文件的背景图宽度
        font_pattern_str: 背景图宽度正则表达式
        x_pattern_str:  获取的 x 坐标正则表达式
        y_pattern_str:  获取的 y 坐标正则表达式

    """
    # 包含 x,y 轴形式的svg文件处理方式
    data_ = svg_file_to_dict(txt, font_size, font_pattern_str, x_pattern_str, y_pattern_str)
    # 仅包含 y 轴形式的处理方式
    if not data_['data']:
        data_ = svg_file_to_dict_without_x_axis(txt, font_size, font_pattern_str, y_pattern_str)
    # 字典化
    data_m = {txt_name: data_}

    return data_m


def svg_img_trans_txt(svg_css_dict: dict, svg_file_dict: dict):
    """svg 背景图转文本"""

    data_m = {}

    for i in svg_css_dict:
        if i in svg_file_dict:
            for j in svg_css_dict[i]:
                # print(j)
                txt_code = j
                txt_x_y = svg_css_dict[i][j]
                font_szie = svg_file_dict[i]['font_size']
                y_ = 0
                for k in svg_file_dict[i]['data']:
                    if k >= txt_x_y['y']:
                        y_ = k
                        break
                try:
                    # print(txt_code)
                    # print(svg_file_dict[i]['data'][y_][int(txt_x_y['x'] / font_szie)])
                    data_m.setdefault(txt_code, svg_file_dict[i]['data'][y_][int(txt_x_y['x'] / font_szie)])
                except:
                    print(txt_code)
                    # print(svg_file_dict[i]['data'][y_])
                    data_m.setdefault(txt_code, None)
    return data_m


if __name__ == '__main__':
    #
    file_dir = r'C:\Users\lztes\Desktop\dazon\20190226'
    file_css_name = 'svg_css.css'
    file_name = 'svg.html'
    file_name2 = 'svg2.html'
    file_name3 = 'svg3.html'
    file_name4 = 'svg4.html'

    file_css_path = os.path.join(file_dir, file_css_name)
    file_path = os.path.join(file_dir, file_name)
    file_path2 = os.path.join(file_dir, file_name2)
    file_path3 = os.path.join(file_dir, file_name3)
    file_path4 = os.path.join(file_dir, file_name4)
    with open(file_css_path, 'r', encoding='utf-8') as f_css, \
            open(file_path, 'r', encoding='utf-8') as f, \
            open(file_path2, 'r', encoding='utf-8') as f2, \
            open(file_path3, 'r', encoding='utf-8') as f3, \
            open(file_path4, 'r', encoding='utf-8') as f4:
        data_css_txt = f_css.read()
        data_txt = f.read()
        data_txt2 = f2.read()
        data_txt3 = f3.read()
        data_txt4 = f4.read()

    # css
    res_css_ = svg_css_to_dict(data_css_txt)
    for i in res_css_.items():
        print(i)
    print('------')
    res_css_ = svg_css_to_dict_global(data_css_txt)
    for i in res_css_.items():
        print(i)

    # svg 文本
    res_ = svg_file_to_dict_without_x_axis(data_txt)
    print(res_)
    res_ = svg_file_to_dict_without_x_axis(data_txt2)
    print(res_)
    res_ = svg_file_to_dict(data_txt3)
    print(res_)
    res_ = svg_file_to_dict(data_txt4)
    print(res_)
    data_m_ = {}
    for i in ['jwx', 'gfi']:
        res2_ = svg_file_bind_dict(data_txt2, i)
        data_m_.update(res2_)
    print(data_m_)
    data_m_ = {}
    res_ = svg_file_bind_dict(data_txt, 'sdf')
    print(res_)
    data_m_.update(res_)
    res_ = svg_file_bind_dict(data_txt2, 'uwq')
    print(res_)
    data_m_.update(res_)
    res_ = svg_file_bind_dict(data_txt3, 'syq')
    print(res_)
    data_m_.update(res_)
    res_ = svg_file_bind_dict(data_txt4, 'vxf')
    print(res_)
    data_m_.update(res_)
    # 编码转文本
    res_ = svg_img_trans_txt(res_css_, data_m_)
    # print(len(res_))
    # print(res_)
    temp_ = 0
    temp2_ = 0
    for i in res_:
        if res_[i]:
            temp_ += 1
            print(i, res_[i])
        else:
            temp2_ += 1
    print(temp_)
    print(temp2_)