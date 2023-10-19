import sys
sys.path.append("../..")
from src import config
import SparkApi

class XUNFEITEXTBOT:
    def __init__(self,appid:str, api_secret:str, api_key:str) -> None:
        self.appid = appid
        self.api_secret = api_secret
        self.api_key = api_key
        self.domain = "general"
        self.Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat" 
        self.text=[]
        
    def getText(self,role,content):
        jsoncon = {}
        jsoncon["role"] = role
        jsoncon["content"] = content
        self.text.append(jsoncon)
        return self.text

    def getlength(self,text):
        length = 0
        for content in text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length

    def checklen(self,text):
        while (self.getlength(text) > 8000):
            del text[0]
        return text
    
    def chat(self, question:str):
        SparkApi.main(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, question)
        return SparkApi.answer
        
    
if __name__ == "__main__":
    xunfei=XUNFEITEXTBOT(
        config.XUNFEI_TEXT_APPID,
        config.XUNFEI_TEXT_APISECRET,
        config.XUNFEI_TEXT_APIKEY
    )
    Input = input("\n" +"我:")
    question = xunfei.checklen(xunfei.getText("user",Input))
    # print(question)
    
    a=xunfei.chat(question)
    print("------")
    print(a)
    print("------")
    
    # SparkApi.answer =""
    # print("星火:",end = "")
    # SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    # getText("assistant",SparkApi.answer)
        
    
    