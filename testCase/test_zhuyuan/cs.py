import os
import jinja2
import yaml
import random
from common.read_yaml import load
def render(tpl_path, **kwargs):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(**kwargs)

# yaml 文件调用以下函数
def rand_str():
    return load('../zy_basic.yaml')
def ran():
    return load('../extract.yaml')
if __name__ == '__main__':
    r = render("C:\\Users\zf\\PycharmProjects\\jiekou\\data\\inhos_patient\\test.yaml", **{"rand_str": rand_str,'ran':ran})
    # #
    print(yaml.safe_load(r)['dd'])