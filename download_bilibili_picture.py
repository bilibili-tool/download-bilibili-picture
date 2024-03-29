import requests  # 导入 Requests 库，用于发送 HTTP 请求
import os  # 导入 os 库，用于处理文件路径
import json

# 构造请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def download_image(url, name):
    """
    下载图片
    :param url: 图片链接
    :param name: 图片名称
    """
    try:
        response = requests.get(url, headers=headers)  # 发送 GET 请求，获取图片内容
        with open(name, 'wb') as f:  # 以二进制写入模式打开文件
            f.write(response.content)  # 写入图片内容
    except Exception as ex:
        print(ex)


def get_dynamic_images(mid, next_offset=0):
    """
    获取某个 up 主的动态图片
    :param mids: up 主的 ID list
    :next_offset: 偏移量
    """
    try:
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={mid}&offset_dynamic_id={next_offset}'
        # 发送 GET 请求，获取响应内容，并解析为 JSON 格式
        response = requests.get(url, headers=headers).json()
        # 构造请求 URL，查询 up 主的动态
        data = response.get('data')
        if not data:
            return
        items = data.get('cards', [])  # 从响应内容中获取动态列表
        next_offset = data.get('next_offset')
        print('next_offset', next_offset)
        for item in items:  # 遍历动态列表
            item = json.loads(item.get('card')).get('item')
            if not item:
                continue
            pictures = item.get('pictures')  # 获取当前动态中的图片列表
            if not pictures:  # 如果当前动态没有图片，跳过
                continue
            for picture in pictures:  # 遍历图片列表
                image_url = picture.get('img_src')  # 获取图片链接
                if not image_url:  # 如果图片链接不存在，
                    continue
                if not os.path.exists('images'):  # 如果 images 文件夹不存在，创建
                    os.makedirs('images')
                filename = os.path.join('images', image_url.split(
                    '/')[-1])  # 构造图片文件名，以图片链接中的最后一段为名称
                download_image(image_url, filename)  # 下载图片
        if next_offset:  # 如果偏移量存在
            get_dynamic_images(mid, next_offset)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    # mid = input('请输入up主的ID：')  # 输入 up 主的 ID
    get_dynamic_images('13127564')  # 获取 up 主的动态图片
    # get_dynamic_images('3493137785817215')  # 获取 up 主的动态图片
