# weixin-download
使用Python实现抖音无水印视频自动下载微信机器人，

附带一个我模仿的you_get自动下载。

## 一、准备工作

由于是将抖音视频上传到本地，在上传到阿里云OSS，获得OSS中的链接，所以阿里云OSS是必需的。（当然你也可以用其他云存储）
### 开通OSS服务并创建bucket

![](https://cdn.jsdelivr.net/gh/growvv/img/images/20200212112038.png)

注意读写权限设为“公共读写”。

推荐两个使用教程：
- [PyPi-oss2 文档](https://pypi.org/project/oss2/2.3.2/)，对于任何一个py库，当你找不到文档的时候都可以来pypi看看
- [aliyun-oss-python-sdk exampples](https://github.com/aliyun/aliyun-oss-python-sdk/blob/master/examples/object_basic.py)，有许多示例

## 二、下载抖音无水印视频

详细原理及实现见[【使用Python快速实现抖音无水印视频自动下载微信机器人】](https://www.92ez.com/?action=show&id=23506)

![效果图](https://cdn.jsdelivr.net/gh/growvv/img/images/20200212112727.png)

考虑到你可能跟我一样求人才得到一个抖音链接，这里我把测试链接分享出来。

>#在抖音，记录美好生活#自动调整列宽～#wps #wps表格 #wps表格技巧 @山竹Excel表格教学 https://v.douyin.com/pTVEfY/ 复制此链接，打开【抖音短视频】，直接观看视频！

## 三、you_get下载视频

这是我模仿上面写的一个下载助手（漏洞百出，以至于不想补）。

![效果图](https://cdn.jsdelivr.net/gh/growvv/img/images/20200212113250.png)

以下是我的几点探索：
1. you_get的用法：参考[you-get官方文档](https://github.com/soimort/you-get)，添加输出重命名。
2. with的使用：参考[Python 中 with用法及原理](https://blog.csdn.net/u012609509/article/details/72911564)，实现出错也能返回提示信息。
3. os.remove()：增加删除本地文件，因为最后程序会挂到VPS上，上传到OSS上后VPS上的文件就没必要保留了。

## 四、部署到vps
就一个python程序，部署起来还是很简单的，最主要的是我们要让我一直保持运行，这里采用<code>nohup</code>。

```bash
nohup python3 douyin.py > dy.log &
```

如果要关掉某个nohup呢？

采用kill进程的方式，使用<code>ps -ef</code>查看当前所有进程，在用<code>kill -9 PID</code>杀死对应进程

![](https://cdn.jsdelivr.net/gh/growvv/img/images/20200212125650.png)


## 五、有待改进
1. 如果多人同时发送下载链接呢？
2. 出错处理有待完善
3. 找一个挂py代码的平台？
