import requests  # 导入 Requests 库，用于发送 HTTP 请求
import os  # 导入 os 库，用于处理文件路径


def download_image(url, name):
    """
    下载图片
    :param url: 图片链接
    :param name: 图片名称
    """
    response = requests.get(url)  # 发送 GET 请求，获取图片内容
    with open(name, 'wb') as f:  # 以二进制写入模式打开文件
        f.write(response.content)  # 写入图片内容


def get_dynamic_images(mid):
    """
    获取某个 up 主的动态图片
    :param mid: up 主的 ID
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # 构造请求头，模拟浏览器访问
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={}'.format(
        mid)
    # 构造请求 URL，查询 up 主的动态
    # 发送 GET 请求，获取响应内容，并解析为 JSON 格式
    response = requests.get(url, headers=headers).json()
    items = response.get('data', {}).get('cards', [])  # 从响应内容中获取动态列表
    for item in items:  # 遍历动态列表
        pictures = item.get('item', {}).get('pictures', [])  # 获取当前动态中的图片列表
        if not pictures:  # 如果当前动态没有图片，跳过
            continue
        for picture in pictures:  # 遍历图片列表
            image_url = picture.get('img_src')  # 获取图片链接
            if not image_url:  # 如果图片链接不存在，
                continue
            filename = os.path.join('images', image_url.split('/')
                                    [-1])  # 构造图片文件名，以图片链接中的最后一段为名称
            download_image(image_url, filename)  # 下载图片


if __name__ == '__main__':
    mid = input('请输入up主的ID：')  # 输入 up 主的 ID
    if not os.path.exists('images'):  # 如果 images 文件夹不存在，创建
        os.makedirs('images')
        get_dynamic_images(mid)  # 获取 up 主的动态图片
