import requests
import json
from kakao_friend import *
import datetime


class Product:
    def __init__(self):
        self.pdName = ""
        self.pdPrice = 0
        self.pdLeftCount = 0
        self.pdSellCount = 0

    def sellTotalMoney(self):
        return self.pdSellCount * self.pdPrice

    def leftTotalMoney(self):
        return self.pdLeftCount * self.pdPrice


class Kakao_friend_message:
    
    def __init__(self):
                
        self.Kakao_friend = Kakao_friend()
        #self.Kakao_friend.send_to_friend(text = param01)
        #self.Kakao_friend.send_to_mutli_friend(text=param01)
        #self.Kakao_friend.getFriendsList()


        
  
if __name__ == "__main__":        
    now = datetime.datetime.now()
    kakao_msg = Kakao_friend_message()    
    
    kakao_msg.Kakao_friend.send_to_mutli_friend(text="test messsage From SSAI Alarm, 2022.12.14, HDCLabs 7F "+now.strftime("%Y-%M-%D:%h-%m-%S"))
    
    