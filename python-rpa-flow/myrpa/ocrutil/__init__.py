import base64
import urllib
import requests

API_KEY = "ntx6sRv3Q2Fdmu8dSiqYwPep"
SECRET_KEY = "QC2lMsRz9BX6RdmKBzKsGzVZzpD2pH97"

def baidu_ocr(picture):
        
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()
    # picture = picture.replace('\\','/')
    
    # image 可以通过 get_file_content_as_base64("C:\fakepath\getVerifyCode.jfif",True) 方法获取
    # payload='image=%2F9j%2F4AAQSkZJRgABAgAAAQABAAD%2F2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL%2F2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL%2FwAARCAAoAIIDASIAAhEBAxEB%2F8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL%2F8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4%2BTl5ufo6erx8vP09fb3%2BPn6%2F8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL%2F8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3%2BPn6%2F9oADAMBAAIRAxEAPwD3%2BqUGpwyzLbyrJa3TZ2wTgKzcZ%2BUglXwOTtJxnnFSX32lbYyWnzTR%2FOsRxiXAPyEnpnsexweRkGWCeK5hWaFtyNnsQQQcEEHkEHIIPIIwaAItRso9S0y7sJmdYrmF4XKEBgrAg4z35rwnxNo%2BkeG%2FiPomn6XDcNHAbY3Cxuxlkk8zJIOR8xXb93AyeMV7zd3UNjZz3dy%2ByCCNpZHwTtVRknA5PArwXxNr2jXnxS03XLO%2F8%2BxWa2lmk8l18vY4DDBGTwoPA74rmxPLZN7mNa1l3PUfGfipPAvhiW6ku%2FtmoSnbZxXO0GRuAeEUfKo%2BY9PTIJFeE%2BN%2FC15omnaRq%2Bq3DyatrbT3V0hj2CInYwUrgYbLtu4AB4A4yfSfEuial8Rte0%2FxF4R1uz%2ByaaFSP7T5qeXcK28sEMZHQx898YPSuG%2BKVj4xsv7K%2FwCEs1Wzv9%2FnfZvsyhdmNm%2FOI065X16HpXSmmro9jB8q5eVrXc%2BidVvhpek3d%2B%2Fl%2BXbRNNIZGZVCKMsSVVjwATwDmvH4%2Fil498V217e%2BEPCkH9n2qFZJJSZZN%2BCcp8yhm27TsCsQcddwFaXji08S2fwS8QR%2BKdQtr6%2BM8LJJbqAoj82HA4Rechj079a2PhHM9v8ACPQ5FhaVQZ%2FMCcsF8%2BTkD%2BIjjjrjOMnANLa55slaVrkXhn4x%2BH9W8MtqerSHTZ4Jkt7iPy3kXewYoVKqchgj9eQVIPYnQ%2F4W94F%2F6Dn%2FAJKT%2FwDxFeZ%2FD2w0zW%2Fjh4tS9tLS%2FtSbyWMTRrKhP2lMMMgjoTz71sfGceG9A0O30rTtE0qDUr5g5khtY1eGJTnIK4KlmAAOCCA4pNGUpSSueoeGvFWl%2BKrF7rTbhZFWaSLGGUnYRzhgDjayHpxuA61t1wXw78KDQPDT6JqAYXgkS9k2OUZDJGBwyNwQVdMg8hSejc9Z9sl075dSeMW44W8LAA%2F9dBgBCemRwSP4SVUo0je2oWdx9luf7NuZsyctbu7cyoSTtGeWZAMHqcbWJyxA0azNZtby4%2BxNYlVmgnaQM%2BNo%2FdSAbv8AZLFQcc4JxjqNGNi8SOyNGzAEo2Mr7HBIz9DQMEkSVS0bq6glSVOeQcEfUEEfhTUnikmlhVv3kWN6kEEAjg%2B4PPI4yCOoNVp4JYJmu7RdztjzoMgCYAYyM8BwOh6EDB7FYblw8SatYhpGjB82NFO%2BaMZzHj%2B%2BrcgEZBBX5dzUAadFNjkSaJJI3V43AZWU5DA9CD6UUAUnkfTpw0jtJaTSBQWOWhdmwB7oWIHqpP8Ad%2B46SCWC%2FW6t13JL8lxECBuPAWTnjKgYPQkHvtUU61mTUrOXzIV8sySwMjfMGCuyHPsdvT3p0MctpbSLvkuQmTEpxvK44UsT8x6gE44xkk5JAJpoY7iGSGaNJIpFKOjqCrKeCCD1BrEn8FeGplkxolhGzhQHjtkG3ByCBjGcnnjnocjiti1u4byIyQs2FO1ldCjKeuCrAEHBB5HQg96mpNJ7iaTKFtZ2uiaXILWxhjCKZXisbcR%2BY4Xkqg7nAAGfQZplzp2ieIYYZrqz0%2FU4k3eU8sSTKMnDbSQfQZx6VoSSJDE8kjqkaAszMcBQOpJ9Kx7TQrZPPWW28t1mYR3EDmJ3iPzKu5CGCrnYFJxiMHA4w9hp22NO%2BsrfUrC5sbuPzLa5iaGVMkbkYEEZHI4J6V4xcfDXxr4LsdVTwl4rii0aWN5pY7jKSrgN90hGAbbj51KEkDgYFe0WtubaIxm4mmXOVMpBKjsucZIHqcn1JqtrkbzeH9SjjRnke1lVVUZLEocAD1pp2FY4%2FwALfD2w8B%2BG7u2inubu8u5Fea9SAtsZCTERECThWxwMkknPy%2Fd4XwbHcfEr4s3PiS9H%2BgaYyyRRh2KqQSIUGWBHIMhwMEqcgbq95rOmh08atGRJ9mv5MOCjbDOB1BHSTABHOSoORtyDSJlC9hzMLXVHlnRQtwEiScZ4wTtRxnAJLNhu%2Bdp527r9NkjSaJ45EV43BVlYZDA9QR6VUgglsZlhhXfZNnauQDbnHQeqHsOqngfL9wLLccaQxJHGipGgCqqjAUDoAPSnUVG08S3KW5b966M6rg8qpUE%2F%2BPL%2BdAFafUPsczC6gkS3423K%2FMg4%2FjxymOckjaAASwJxUem%2FvZriV%2F3d0jmG5ROEdgAVfHOCUKng9GAJO0YzrKa50rxDPY3cm60uEWWGY4UeYWKkbQBgtwTg43EHgyBaddvfaNdrqE4W5tABHdTxqRIsQ3FWZBwSpOSykcM3ycAgAv8A9h2Q4RryNeyR3syKo9AocAD2HAorRooAzF05IUWJLlUvBJPPDJjkB5CzArn5k%2BZQR9DwcEObUJnhmiig26jEm%2F7PJnbJgjIRzgMDwN38O5dwB%2BWiigCC%2FBurO31PTGb7RIYfLlVWIaNnXJdARuUKzHnpkkYPNaVrJcSRH7TAsMoOCEk3qfcHAOO3IHIPbBJRQAy6uZbbY620k0XPmGLBZPfb%2FEOvTJ6YBzxS0%2B4htvJghmjnsrh2FpLEwYA%2FMxj44wAG2kcALtOCBuKKANR5EiUNI6opIUFjjknAH1JIH406iigArMijQltI1BFuVYNJEZRvEkYYcNnPzJuUZOc8NknIBRQBYtbN7SUhLqaS3I4imbeVPqHPzY653Fu2MAYNuiigArOvP3WtaZP18zzbXb6bl8zd%2FwCQcY%2F2vbkooAm1HTrfVLQ29wGABDpIh2vG46Mp7MPWodNklurA2eppG15Gnl3MZwVkByN%2BMAFWAJ6Y6jqCKKKAL8aCKJI1LFVAUFmLHj1J5J9zRRRQB%2F%2FZ&language_type=ENG'
    payload='image='+get_file_content_as_base64(picture,True) # &language_type=ENG'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    words_result = response.json()["words_result"]
    print(words_result)
    
    # 去除空格部分
    words = words_result[0]["words"].replace(' ','') 
    print("words == ", words)
    return words
    

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

# if __name__ == '__main__':
#     main()
    # print(get_file_content_as_base64("D:\jpg\yan1.png",True))
