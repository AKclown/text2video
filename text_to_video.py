import time
import requests
import json
import cv2
import os
import textwrap
from dotenv import load_dotenv
import numpy as np
import subprocess
import re
import random
import datetime
import math

from add_text_to_image import add_text_to_image
from translate import translate_to_english


# 尝试加载线上环境变量文件
load_dotenv('.env', override=True)

# 尝试加载本地开发环境变量文件
load_dotenv('.local.env', override=True)

# 获取当前脚本所在的目录
current_directory = os.getcwd()

# 读取环境变量
api_token = os.getenv('API_TOKEN')

# headers_list = [
#     {
#         'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666'
#     }, {
#         'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
#     }, {
#         'user-agent': 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+'
#     }, {
#         'user-agent': 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G965U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)'
#     }, {
#         'user-agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 3 Build/PQ1A.181105.017.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
#     }, {
#         'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
#     }, {
#         'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
#     }, {
#         'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
#     }
# ]

# basicHeaders = random.choice(headers_list)


# headers = {
#     **basicHeaders,
#     "Authorization": f"Bearer {api_token}",
#     "Content-Type": "application/json"
# }

# !!! 模型依赖生成图片
# def requestImage(model, prompt):
#     r = any
#     try:
#         body = {
#             "inputs": translate_to_english(prompt)
#         }
#         if model == "pollinations-ai":
#             r = requests.post("https://image.pollinations.ai/prompt/"+body['inputs'])
#         else:
#             r = requests.post("https://api-inference.huggingface.co/models/" + model,
#                         data=json.dumps(body), headers=headers)
#             return r
#     except:
#         print("requestImage：远程主机强迫关闭一个现有链接,正在重试")
#         return  requestImage(model, prompt)


# def generateImage(model, prompt):
#         # body = {
#         #     "inputs": translate_to_english(prompt)
#         # }
#         # if model == "pollinations-ai":
#         #     r = requests.post("https://image.pollinations.ai/prompt/"+body['inputs'])
#         # else:
#         #     r = requests.post("https://api-inference.huggingface.co/models/" + model,
#         #                 data=json.dumps(body), headers=headers)
#         img = requestImage(model, prompt)
#         # 将图片写入到 images 目录下，每个图片使用(时间戳+model).png 来命名
#         timeStamp = str(int(time.time()))
#         imagePath = "images/" + timeStamp + \
#             "-" + model.split("/")[-1] + ".png"
#         with open(imagePath, "wb") as f:
#             f.write(img.content)
#             f.close()

#         voicePath = "voices/" + timeStamp + \
#             "-" + model.split("/")[-1] + ".mp3"
#         convert_text_to_speech(
#             text=prompt, output_file=voicePath
#         )


def convert_text_to_speech(text, output_file):
    # 指定输出目录
    output_directory = os.path.join(current_directory, "voices")
    # 创建输出目录（如果不存在）
    os.makedirs(output_directory, exist_ok=True)
    # 执行命令，并将工作目录设置为输出目录
    try:
        command = ['edge-tts', '--voice', 'zh-CN-YunjianNeural', '--text', text,
                   '--write-media', output_file, '--write-subtitles', f'{output_file}.vtt']
        result = subprocess.run(command, cwd=current_directory, timeout=100)
        # duration = get_duration_from_vtt(output_file + ".vtt")
        # 删除 无效音频 or 重新生成？
        # if duration == 0.1:
        #     try:
        #         print(duration)
        #         os.remove(output_file + ".vtt")
        #     except(FileNotFoundError):
        #         print("文件不存在")

        # os.remove(output_file)
    except subprocess.CalledProcessError as e:
        print("Command execution failed with return code:", e.returncode)
        print("Command output:", e.output)


def clear_folder(folder_path):
    """清空指定文件夹中的文件"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def split_sentences(text):
    pattern = r'[\r\n]'
    sentences = re.split(pattern, text)
    # 移除空白的句子
    sentences = [sentence.strip()
                 for sentence in sentences if sentence.strip()]
    return sentences


def convertTextToVideo(model, text):

    # 将文本段落进行分句
    sentences = split_sentences(text)

    # 清空 images 文件夹
    # clear_folder("images")
    # 清空 voices 文件夹
    clear_folder("voices")
    # 清空 videos 文件夹
    clear_folder("videos")

    # 为每个句子生成语音
    for i in range(sentences.index(sentences[-1])+1):
        if sentences[i].strip() != "":
            voicePath = "voices/" + str(i) + ".mp3"
            convert_text_to_speech(
                text=sentences[i].strip(), output_file=voicePath
            )

    # 合成视频
    frame_width = 640
    frame_height = 480
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    video_name = f"【每日新闻热点】{year}年{month}月{day}日"
    output_video_path = "videos/" + video_name + ".origin.mp4"
    # https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
    # cv2.VideoWriter初始化视频write构造器
    # cv2.VideoWriter_fourcc指定解码器
    output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(
        *'mp4v'), 30, (frame_width, frame_height))

    image_files = os.listdir('images')
    image_files.sort()

    for image_file in image_files:
        if image_file.endswith(".png"):

            text_color = (255, 255, 255)  # 白色文字
            background = (0, 0, 0, 128)  # 黑色背景半透明
            image_path = "images/" + image_file
            draw_text = sentences[image_files.index(image_file)]
            add_text_to_image(draw_text, image_path,
                              text_color, background, padding=10)
            # 从文件中加载图片
            image = cv2.imread(image_path)
            # 缩放图片
            resized_image = cv2.resize(image, (frame_width, frame_height))
            # 写入视频的下一帧
            output_video.write(resized_image)
            # 添加停顿帧
            duration = get_duration_from_vtt(
                f"voices/{find_file_name_without_extension(image_file)}.mp3.vtt")
            print(duration)
            for _ in range(int(math.ceil(duration) * 31)):
                output_video.write(resized_image)
    # 关闭video write
    output_video.release()
    
    middle_output_video_path = "videos/" + video_name + ".withAudio.mp4"

    merge_audio_to_video("voices", output_video_path,
                         middle_output_video_path)
    desc_output_video_path = "videos/"+ video_name +".mp4"
    convert_to_h264(middle_output_video_path, desc_output_video_path)
    return desc_output_video_path


def convert_to_h264(input_file, output_file):
    # 使用 FFmpeg 进行视频转换
    command = ['ffmpeg', '-i', input_file, '-c:v', 'libx264',
               '-preset', 'slow', '-crf', '22', '-c:a', 'copy', output_file]
    try:
        subprocess.run(command, check=True)
        print('视频转换成功！')
    except subprocess.CalledProcessError as e:
        print('视频转换失败:', e)


def find_file_name_without_extension(file_path):
    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    return file_name_without_extension


def merge_audio_to_video(audio_directory, video_file, output_file):
    # 获取目录中的音频文件
    audio_files = [file for file in os.listdir(
        audio_directory) if file.endswith('.mp3')]

    if not audio_files:
        print("No audio files found in the directory.")
        return
    audio_files.sort()
    # 生成FFmpeg命令
    command = [
        'ffmpeg',
        '-i',
        video_file,
    ]

    # 添加音频文件参数
    for audio_file in audio_files:
        command.extend(['-i', audio_directory+'/'+audio_file])

    # 设置音频合并选项
    command.extend([
        '-filter_complex',
        ''.join([f'[{i+1}:0]' for i in range(len(audio_files))]) +
        f'concat=n={len(audio_files)}:v=0:a=1[outa]',
        '-map',
        '0:v',
        '-map',
        '[outa]',
        '-c:v',
        'copy',
        '-c:a',
        'aac',
        '-shortest',
        output_file
    ])

    # 执行FFmpeg命令
    result = subprocess.run(command, cwd=current_directory, timeout=30)
    print(result)


def get_duration_from_vtt(vtt_file):
    print(vtt_file)
    if not os.path.exists(vtt_file):
        return 0.1
    with open(vtt_file, 'r') as file:
        lines = file.readlines()

    total_duration = 0.1

    for line in lines:
        line = line.strip()
        if '-->' in line:
            start_time, end_time = line.split('-->')
            start_time = start_time.strip()
            end_time = end_time.strip()
            start_seconds = convert_time_to_seconds(start_time)
            end_seconds = convert_time_to_seconds(end_time)
            duration = end_seconds - start_seconds
            total_duration += duration

    return total_duration


def convert_time_to_seconds(time):
    hours, minutes, seconds = time.split(':')
    seconds, milliseconds = seconds.split('.')
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    total_seconds = (hours * 3600) + (minutes * 60) + \
        seconds + (milliseconds / 1000)
    return total_seconds


if __name__ == '__main__':
    text_test = '''
   一个风和日丽的早上，我骑着自行车去学校，在路上遇到了彩虹，当时我的心情非常的愉快。
'''
#    convertTextToVideo(models[0], text_test)
