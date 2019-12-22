import vk_api.vk_api
import random
import urllib.request, json 
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import requests
import time, os
import string
import datetime
import requests
import lxml.html as html
import apiai #ИИ
class Server:

            def __init__(self, api_token, group_id, server_name: str="Empty"):

                # Даем серверу имя
                self.server_name = server_name

                # Для Long Poll
                self.vk = vk_api.VkApi(token=api_token)

                self.upload = vk_api.VkUpload(self.vk)

                # Для использования Long Poll API
                self.long_poll = VkBotLongPoll(self.vk, group_id)

                # Для вызова методов vk_api
                self.vk_api = self.vk.get_api()

            def send_img(self, send_id, message):
                """
                Отправка сообщения через метод messages.send
                :param send_id: vk id пользователя, который получит сообщение
                :param message: содержимое отправляемого письма
                :return: None
                """
                self.vk_api.messages.send(peer_id=send_id,
                                          attachments=attachments,
                                          random_id=123456 + random.randint(1,27))

            def send_msg(self, send_id, message):
                """
                Отправка сообщения через метод messages.send
                :param send_id: vk id пользователя, который получит сообщение
                :param message: содержимое отправляемого письма
                :return: None
                """
                self.vk_api.messages.send(peer_id=send_id,
                                          message=message,
                                          random_id=123456 + random.randint(1,27))
            def start(self):
                for event in self.long_poll.listen():
                    print(event.object.text, " ", event.object.from_id)
                    lst = event.object.text.split()
                    print(lst)
                    print(len(lst))
                    if lst[0] == 'новости':
                        test = ""
                        for i in range(1, len(lst)):
                            test = test + " " + str(lst[i])
                        r = requests.get('https://news.yandex.ru/yandsearch?text={}&rpt=nnews2&grhow=clutop&rel=rel'.format(test)).text
                        parser = html.fromstring(r)
                        news = ""
                        for i in range(20):
                            try:
                                elem = parser.cssselect('a[class="link link_theme_normal title__link i-bem"]')[i]
                                print(elem)
                                print(elem.get('title'))
                                news = news + elem.get('title') + "\n\n"
                                #print(elem.get('href'))
                            except:
                                print("\nВсего " + str(i) + " новостей")
                                break
                        self.send_msg(event.object.peer_id, news)
                    
                    if lst[0].lower() == "scp":
                        scp = lst[1]
                        print(scp)
                        try:
                            url = 'http://scpfoundation.net/scp-{}'.format(scp)
                            r = requests.get(url).text
                            parser = html.fromstring(r)
                            scp_name = ""
                            elem = parser.cssselect('div[id="page-title"]')[0]
                            print(elem.text)
                            elem = elem.text
                            self.send_msg(event.object.peer_id, elem + "\n" + url)
                        except:
                            self.send_msg(event.object.peer_id, "Напишите корректный номер")
if __name__ ==  "__main__":
    server1 = Server("токен группы", id группы, "server1")
    server1.start()
