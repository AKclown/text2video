import requests
from langdetect import detect

def translate_to_english(text):
    try:
        if not is_chinese(text):
            return text
        url = "http://fanyi.youdao.com/translate?doctype=json"
        params = {
            "i": text,
            "from": "auto",
            "to": "en",
        }
        response = requests.get(url, params=params)
        print(response.json())
        translation = response.json()
        response.close()
        if "translateResult" in translation:
            return translation["translateResult"][0][0]["tgt"]
        else:
            return text
    except:
       print("translate_to_english：远程主机强迫关闭一个现有链接,正在重试")
       return  translate_to_english(text)


# if __name__ == "__main__":
#     print(translate_to_english("我是中国人"))

def is_chinese(text):
    try:
        lang = detect(text)
        print(lang)
        return lang == 'zh-cn' or lang == 'zh-tw'
    except:
        return False

