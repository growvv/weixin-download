from ipaddress import ip_address
from contextlib import closing
import requests
import itchat
import random
import oss2
import time
import sys
import re
import json


# 生成x位随机字符串
def create_random_string(x):
    chars = "abcdefghijklmnABCDEFGHIJKLMNXYZopqrstuvwxyz"
    random_string = random.sample(chars, x)
    return "".join(random_string)


def create_headers():
    rip = ip_address('0.0.0.0')
    while rip.is_private:
        rip = ip_address('.'.join(map(str, (random.randint(0, 255) for _ in range(4)))))
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'X-Real-IP': str(rip),
        'X-Forwarded-For': str(rip),
    }
    return headers


def do_download(video_url, v_info):
    size = 0
    headers = create_headers()
    with closing(requests.get(video_url, headers=headers, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            local_file = "%s/Download/%s.mp4" % (sys.path[0], v_info.get("video_author") + '-[' + v_info.get("video_name") +']')
            print("local_file", local_file)
            with open(local_file, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    file.flush()

            reset_name = str(time.strftime('%Y%m%d%H%M%S')) + create_random_string(5) + ".mp4"
            remote_path = "auto-upload" + time.strftime('/%Y-%m-%d/') + reset_name
            print(remote_path)
            try:
                auth = oss2.Auth("access_key_id", "access_key_secret")
                endpoint = 'http://oss-cn-beijing.aliyuncs.com'
                bucket = oss2.Bucket(auth, endpoint, 'weixin-download')
                bucket.put_object_from_file(remote_path, local_file)
                oss_path_url = "https://weixin-download.oss-cn-beijing.aliyuncs.com/" + remote_path
                result = "成功"
            except Exception as e:
                result = "视频上传云端失败，请微信联系开发者"
                oss_path_url = "无"
        else:
            result = "下载视频失败，请微信联系开发者"
            oss_path_url = "无"
    return '[作者]：%s\n[描述]：%s\n[大小]：%0.2f MB\n[状态]：%s\n[下载地址]：%s' % (
            v_info.get("video_author"),
            v_info.get("video_name"),
            content_size / chunk_size / 1024,
            result,
            oss_path_url
    )


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return deal_wx_msg(msg)


# @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
# def text_reply(msg):
#     return deal_wx_msg(msg)


def deal_wx_msg(msg):
    #text = "#在抖音，记录美好生活#自动调整列宽～#wps #wps表格 #wps表格技巧 @山竹Excel表格教学 https://v.douyin.com/pTVEfY/ 复制此链接，打开【抖音短视频】，直接观看视频！"
    if "v.douyin.com" in msg.text:
        complete_url = "https://v.douyin.com/%s/" % (msg.text.split("/")[3])
        html_first_response = requests.get(url=complete_url, headers=create_headers())
        redirect_url = html_first_response.url
        html_content = html_first_response.content.decode("utf8")
        if "share/video" in redirect_url:
            dytk = re.findall(r'dytk: "(.+?)"', html_content)[0]
            video_id = re.findall(r"video\/(.+?)\/\?region", redirect_url)[0]
            video_info_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=%s&dytk=%s" % (video_id, dytk)
            video_json = requests.get(url=video_info_url).json()
            if len(video_json.get("item_list")) > 0:
                video_clear_url = video_json.get("item_list")[0].get("video").get("play_addr").get("url_list")[0]
                video_name = video_json.get("item_list")[0].get("desc")
                video_author = re.findall(r'<p class="user-info-name">(.+?)<', html_content)[0]
                video_info = {"video_name": video_name, "video_author": video_author}
                return do_download(video_clear_url, video_info)
            else:
                return "未检测到视频信息"
        else:
            return ""


itchat.auto_login(hotReload=True, enableCmdQR=0.5)
itchat.run()

#deal_wx_msg()
