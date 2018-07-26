#!/usr/bin/env python3

import os
import shutil
import mistune
from string import Template

md_list = []

root = os.getcwd()  # 根目录
dist = os.path.join(root, 'dist')

template_html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>JerryZhang</title>
    <link href="https://cdn.bootcss.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="./assets/style.css" />
    <link rel="icon" href="./assets/favicon.ico">
  </head>
  <body>
    <div class="container">
      <div class="markdown-content">
        ${content}
      </div>
    </div>
  </body>
</html>
"""


def create_env():
    """创建 html 存放目录
    1. 存在则删除
    2. 创建
    """
    if os.path.isdir(dist):
        print('[{}] exist, delete it'.format(dist))
        shutil.rmtree(dist)
    os.mkdir(dist)
    os.mkdir(os.path.join(dist, 'assets'))


def copy_files():
    # index.html
    shutil.copy2(os.path.join(root, 'index.html'), dist)
    # avatar
    shutil.copy2(os.path.join(root, 'assets/avatar.png'), dist + '/assets')
    # favicon
    shutil.copy2(os.path.join(root, 'assets/favicon.ico'), dist + '/assets')
    # lessc style.less style.css
    lessc = shutil.which('lessc')
    cmd = '{0} {1} {2}'.format(
        lessc,
        os.path.join(root, 'assets/style.less'),
        os.path.join(dist, 'assets/style.css')
    )
    os.system(cmd)

    for md in md_list:
        with open(os.path.join(root, md), 'r') as fr:
            content = fr.read()
            with open(os.path.join(root, 'dist/{}.html'.format(os.path.splitext(md)[0])), 'w') as fw:
                fw.write(Template(template_html).substitute(
                    {"content": mistune.markdown(content)}
                ))


if __name__ == '__main__':
    create_env()
    copy_files()
