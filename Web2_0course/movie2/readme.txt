1. 开发环境：ubuntu 12.04 + python 2.7.3 + tornado 3.1.1 + firefox for ubuntu 18.0.2
2. 建议运行环境：任意较新的linux发行版 + python 2.6/2.7 + tornado 3 + 任意较新的firefox
3. 为了方便，原网页通用的素材不再链接到原网址，而是保存在static/img下直接加载
4. python代码已经尽量按照pylint的建议修改，剩下不通过的主要是本身的设计和使用框架的原因。css代码和生成的html已经过W3C检测
5. 默认端口设置为8888, e.g. http://localhost:8888/?film=tmnt
6. linux下压缩中文名文件/文件夹易出现乱码，所以没有多加一层文件夹直接压缩
