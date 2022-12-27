import requests
import json

class Kakao_friend():
    def __init__(self):
        self.app_key = "{REST API 키}" ## REST API 키 입력 

        with open("kakao/kakao_token.json", "r") as fp:
            self.tokens = json.load(fp)
            self.refresh_token()
            
        #self.getFriendsList()

    # reflash Kako Token
    def hi(self):
        print('hi')
        
    def refresh_token(self):
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.app_key,
            "refresh_token": self.tokens['refresh_token']
        }

        response = requests.post(url, data=data)

        # 갱신 된 토큰 내용 확인
        result = response.json()
        print('카카오 토큰 갱신:', result)

        # 갱신 된 내용으로 파일 업데이트
        if 'access_token' in result:
            self.tokens['access_token'] = result['access_token']
            print('access_token : ',  self.tokens['access_token'] )

        if 'refresh_token' in result:
            self.tokens['refresh_token'] = result['refresh_token']
            print('access_token: ', self.tokens['refresh_token'])
        else:
            pass

        with open("kakao_token.json", "w") as fp:
            json.dump(self.tokens, fp)



    def send_to_kakao(self, text):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {"Authorization": "Bearer " + self.tokens['access_token']}
        content = {
        "object_type": "text",
        "text": text,
        "link": {"mobile_web_url": "http://m.naver.com"}
        }

        data = {"template_object": json.dumps(content)}
        res = requests.post(url, headers=headers, data=data)

        ## 에러메시지 확인
        res.json()
        
    
    def send_to_friend(self,text):
        
        friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
        #friend_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        headers = {"Authorization": "Bearer " + self.tokens['access_token']}
        content = {
            "object_type": "text",
            "text": text,
            "link": {"mobile_web_url": "http://m.naver.com"}
        }

        data = {"template_object": json.dumps(content)}
        res = requests.post(friend_url, headers=headers, data=data)
        result = json.loads(requests.get(friend_url, headers=headers).text)
        
        friends_list = result.get("elements") 
        print(friends_list)
        # print(type(friends_list))
        print("=============================================")
        #print(friends_list[0].get("uuid"))
        friend_id = friends_list[0].get("uuid")
        print(friend_id)


        send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

        data={
            'receiver_uuids': '["{}"]'.format(friend_id),
            "template_object": json.dumps({
                "object_type": text,
                "text": "text",
                "link":{
                    "web_url":"www.daum.net",
                    "web_url":"www.naver.com"
                },
                "button_title": "확인"
            })
        }
        print(data)

        response = requests.post(send_url, headers=headers, data=data)
        response.status_code

        ## 에러메시지 확인
        res.json()
        
        if response.json().get('result_code') == 0:
            print('메시지를 성공적으로 보냄.')
        else:
            print('메시지를 실패. 오류메시지 : ' + str(response.json()))

    
    
    
    def send_to_mutli_friend(self,text):
        friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
        headers = {"Authorization": "Bearer " + self.tokens['access_token']}
        content = {
            "object_type": "text",
            "text": text,
            "link": {"mobile_web_url": "http://m.naver.com"}
        }

        data = {"template_object": json.dumps(content)}
        res = requests.post(friend_url, headers=headers, data=data)
        result = json.loads(requests.get(friend_url, headers=headers).text)
        print('friend_list !!!!')
        print(type(result))
        #print(result)
        #print("=============================================")

        friends_list = result.get("elements")
        friends_id = []
        friends_name = []
        for friend in friends_list:
            friends_id.append(str(friend.get("uuid")))
            friends_name.append(str(friend.get("profile_nickname")))

        print("[json] total_count:", result['total_count'])
        print('[json] nickname, id:', friends_name, friends_id)    
       
        print(friends_list)
        print(" for ------------------------------------------------------------------ ")
        
        for  id_item in friends_id:

            print( id_item)
            send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

            data={
                #'receiver_uuids': '["{}"]'.format(friend_id),
                'receiver_uuids': '["{}"]'.format(id_item),
                "template_object": json.dumps({
                    "object_type":"text",
                    "text": text,
                    "link":{
                        "web_url":"www.naver.com"
                    },
                    "button_title": "확인"
                })
            }

            response = requests.post(send_url, headers=headers, data=data)
            response.status_code

            ## 에러메시지 확인
            res.json()
            print("-------------------------------------------------------------------  for ")
           
    
    def getFriendsList(self):
        print("")
        print("[getFriendList() ]  -----------------------------------------------")
        header = {"Authorization": 'Bearer ' +  self.tokens['access_token']}
        url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 정보 요청

        result = json.loads(requests.get(url, headers=header).text)

        friends_list = result.get("elements")
        friends_id = []
        friends_name = []
        
        #print(requests.get(url, headers=header).text)
        #print(friends_list)

        for friend in friends_list:
            friends_id.append(str(friend.get("uuid")))
            friends_name.append(str(friend.get("profile_nickname")))
            #print('[json] friend nickname, id :', friends_name, friends_id)
            
        print("[json] total_count:", result['total_count'])
        print('[json] nickname, id:', friends_name, friends_id)    
        print("------------------------------------------------------------------- ")
        
        
    
    def sendToMeMessage(self):
        header = {"Authorization": 'Bearer ' +  self.tokens['access_token']}
        url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send" #api 주소
        uuid = ["친구의 UUID"]
        uuidsData = {"receiver_uuids" : json.dumps(uuid)}    
        
        post = {
            "object_type": "text",
            "text" : "보낼 TEXT",
            "link" : {
                "web_url" : "http://naver.com",
                "mobile_web_url" : "http://naver.com"
            },
            "button_title":"button title"
        }
        data = {"template_object": json.dumps(post)}
        uuidsData.update(data)

        return requests.post(url, headers=header, data=uuidsData).status_code
    
    
    def send_template_to_friend(self,text):
        friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
        #friend_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        headers = {"Authorization": "Bearer " + self.tokens['access_token']}
        content = {
            "object_type": "text",
            "text": text,
            "link": {"mobile_web_url": "http://m.naver.com"}
        }

        data = {"template_object": json.dumps(content)}
        res = requests.post(friend_url, headers=headers, data=data)
        result = json.loads(requests.get(friend_url, headers=headers).text)
        
        print('friend_list !!!!')
        print(type(result))
        print("=============================================")
        print(result)
        print("=============================================")
        friends_list = result.get("elements") 
        print(friends_list)
        # print(type(friends_list))
        
             
        print("[json] total_count:", result['total_count'])
        print('[json] nickname, id:', friends_name, friends_id)    
        print("------------------------------------------------------------------- ")
        
                
        print("=============================================")
        print(friends_list[0].get("uuid"))
        friend_id = friends_list[0].get("uuid")
        print(friend_id)

        send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        #talk_url = "https://kapi.kakao.com/v2/api/talk/memo/send"
        talk_url = 'https://kapi.kakao.com/v1/api/talk/friends/message/scrap/send'

        data={
            'receiver_uuids': '["{}"]'.format(friend_id),
            "template_object": json.dumps({
                "object_type":"text",
                "text": text,
                "link":{
                    "web_url":"www.daum.net",
                    "web_url":"www.naver.com"
                },
                "button_title": "Click!"
            })
        }
        
        payload = {
            'template_id' : 87152,
            'template_args' : '{"name": "테스트 제목"}'
        }


        #response = requests.post(send_url, headers=headers, data=data)
        response = requests.post(talk_url, headers=headers, data=payload)
        response.status_code

        ## 에러메시지 확인
        res.json()
    