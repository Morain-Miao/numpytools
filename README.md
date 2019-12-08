# NumpyTools

## 前言：

大家好，我是咕泡的苗同学。

因为numpy索引、切片很复杂。需要多多的练习，所以需要很多的练习题。但自己想的话，又很苦恼。

所以我用了4个小时开发了一个练习的小工具。

源码开放在这里，希望大家有好的建议或者发现BUG能来提交合并。



## 主要功能：

- 索引、切片、索引+切片三种训练模式
- 根据代码给数组或者看数组给代码两种模式
- 如果做不出来，可以显示当前数组的shape作为提示



## python如何打包为exe程序

- pip install  PyInstall    如果需要配置代理的话   --proxy = 代理地址       
- pyinstaller --clean --win-private-assemblies -F -w XXXX.py 
- w是小黑窗  F是打包为单独的一个exe文件