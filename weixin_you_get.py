import sys
import os
import you_get
import oss2
import itchat
import re
from urllib.parse import quote, unquote
import requests
from contextlib import closing


endpoint = 'http://oss-cn-beijing.aliyuncs.com'  # bucket位于北京地区
auth = oss2.Auth('xxx', 'xxx')
bucket = oss2.Bucket(auth, endpoint, 'weixin-download')


def download_upload(url):

    path = os.path.basename(url)      # 视频输出的位置
    name = unquote(path).split('.')[0]
    type = unquote(path).split('.')[-1]
    print(name, type)

    with closing(requests.get(url)) as response:
        if response.status_code == 200:
            try:
                # 下载
                sys.argv = ['you-get', '-O', name, url]
                you_get.main()
                print("download Ok")

                # 上传
                oss2.resumable_upload(bucket, path, path, multipart_threshold=100 * 1024)
                oss_path_url = "https://weixin-download.oss-cn-beijing.aliyuncs.com/" + quote(path)
                print("upload Ok", oss_path_url)

                # 删除本地文件
                os.remove(path)
                print("remove OK")

                result = "OK"

            except Exception as e:
                result = "上传错误，请稍后再试"
                oss_path_url = ""

        else:
            result = "下载错误，请检查链接"
            oss_path_url = ""

    res = '[文件名]：%s\n[状态]：%s'% (path, result)
    if oss_path_url != "":
        res += '\n[下载地址]：%s' % (oss_path_url)

    return res

def deal_wx_msg(msg):
    #text = "下载 https://pan.rogn.top/Book/Linux%20Basics%20for%20Hackers%28%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E7%A8%BF%29%E3%80%90%28%E7%BE%8E%29OccupyTheWeb%20%E8%91%97%E3%80%91.pdf"
    if "下载" in msg.text:
        url = msg.text.split(" ")[-1]
        print(url)
        return download_upload(url)


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return deal_wx_msg(msg)


# @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
# def text_reply(msg):
#     return deal_wx_msg(msg)


itchat.auto_login(hotReload=True, enableCmdQR=1)
itchat.run()

#deal_wx_msg()
