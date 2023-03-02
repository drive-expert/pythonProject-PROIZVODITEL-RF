import requests
from lxml import html
import csv



url ="https://xn--b1aedfedwrdfl5a6k.xn--p1ai/" #основной сайт
url_dop ="producers?page=" #дополнение адреса (каталог)
url_cat=url+url_dop
pre_link_mass = [] #массив ссылок на страница каталога
link_mass = [] #массив ссылок на страницы организаций
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-fetch-mode': 'navigate',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'authority': 'xn--b1aedfedwrdfl5a6k.xn--p1ai',
        'sec-fetch-dest': 'document',
        'cookie': 'beget = begetok; _ym_uid=1677650675582214406; _ym_d=1677650675; _ym_isad = 2' #без этого не заработает
    }


def pre_link_page_mass_create(nach_cat,kon_cat): #создает массив ссылок на страница каталога

    for page in range(nach_cat,kon_cat):
        url_cat_n=url_cat+str(page)
        print(url_cat_n)
        pre_link_mass.append(url_cat_n)
    print()
    print('Функция pre_link_mass_create >>> FINISH')
    print()
    print(pre_link_mass)
    print()
    return pre_link_mass

def link_mass_create(pre_link_mass,max_link_on_page): #создает массив ссылок на страницы организаций
    chet_link_mass = 1 #счетчик ссылок на страницу каталога
    print('Работает функция LINK_MASS_CREATE:')
    for page_link in pre_link_mass:
        response = requests.get(page_link, headers=headers)
        print(f'{chet_link_mass}>>>Обрабатываем ссылку:{page_link}')
        chet_link_mass=chet_link_mass+1 #счетчик страниц каталога
        if response.status_code == 200:
            tree=html.fromstring(response.text)
            chet_link_org = 1 #счетчик ссылок на организацию
            for i in range(2,max_link_on_page+1):
                link_org=tree.xpath(f'////div/div/div[3]/div[1]/div/div[{str(i)}]/a/@href')
                if len(link_org) > 0:
                    print(f'Организация №{chet_link_org} на странице {chet_link_mass-1} каталога>>>>https://xn--b1aedfedwrdfl5a6k.xn--p1ai{link_org[0]}#bconts')
                    link_mass.append(f'https://xn--b1aedfedwrdfl5a6k.xn--p1ai{link_org[0]}#bconts')
                    chet_link_org = chet_link_org+1
    print()
    print(link_mass)
    print()
    return link_mass
def tel_mob_extract(phone):
    phone_list = {'tel_mob': '', 'tel_office':'', 'wa_link':''}
    if len(phone) > 0:
        phone = phone.replace("-", "").replace("(", "").replace(")", "").replace("+", "").replace(" ", "").replace("'", "").replace("]", "") #убираем лишние символы
        phone = phone[0:11]
        if phone[1] == '9':
            phone_list['wa_link'] = f'https://wa.me/7{phone[1:11]}'
            phone_list['tel_mob'] = f'7{phone[1:11]}'
            phone_list['tel_office'] = ''
        else:
            phone_list['wa_link'] = ''
            phone_list['tel_mob'] = ''
            phone_list['tel_office'] = f'8{phone[1:11]}'
    return phone_list

def replace_char(in_string): #убирает лишние символы из строки in_string
    a = str(in_string).replace(",","").replace("(","").replace(")","").replace("[","").replace("]","").replace("'","")
    return a



def create_file_csv(link_mass):
    with open("производитель-рф.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        names = ["Наименование", "ИНН", "WhatsApp", "Телефон (офис)", "Телефон (мобильный)", "Сайт", "VK", "Email", "Город",
                 "Адрес"]
        file_writer = csv.DictWriter(w_file, delimiter=",", lineterminator="\r", fieldnames=names)
        file_writer.writeheader()
        chet_itog = 0 #итоговый счетчик компаний
        for link_org in link_mass:
            chet_itog = chet_itog+1
            print()
            print(f'{chet_itog}>>>>>>>Обрабатываем ссылку:{link_org}')
            response = requests.get(link_org, headers=headers)
            if response.status_code == 200:
                tree=html.fromstring(response.text)
                tel = str(tree.xpath('//*[@id="bconts"]/div/div[2]/div[2]/a/text()'))
                tel_dict = tel_mob_extract(str(tel[2:20]))
                org_tel = str(tel_dict['tel_office'])
                org_inn = str('000000000')
                org_wa = str(tel_dict['wa_link'])
                org_vk = ''
                org_mob = str(tel_dict['tel_mob'])
                org_email = replace_char(tree.xpath('//*[@id="bconts"]/div/div[3]/div[2]/a/text()'))
                org_site = replace_char(tree.xpath('//*[@id="bconts"]/div/div[4]/div[2]/a/@href'))
                org_city = replace_char(tree.xpath('/html/body/div/div[2]/div/div[1]/div/ul/li[4]/a/text()'))
                org_addr = replace_char(tree.xpath('//*[@id="bconts"]/div/div[1]/div[2]/text()'))
                org_name = replace_char(tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div/ul/li[5]/span/text()'))
                file_writer.writerow({"Наименование": str(org_name), "ИНН": str(org_inn), "WhatsApp": str(org_wa),"Телефон (офис)": str(org_tel), "Телефон (мобильный)": str(org_mob),"Сайт": str(org_site), "VK": str(org_vk), "Email": str(org_email), "Город": str(org_city), "Адрес": str(org_addr)})
                print(f'{chet_itog}> Name:{str(org_name)}, INN{chet_itog}: {str(org_inn)}, TelOffice{chet_itog}:{str(org_tel)}, TelMob{chet_itog}:{str(org_mob)},WA{chet_itog}:{str(org_wa)}, Site{chet_itog}:{str(org_site)}, VK{chet_itog}:{str(org_vk)}, Email{chet_itog}:{str(org_email)}, City{chet_itog}:{str(org_city)}, Addr{chet_itog}:{str(org_addr)}')




pre_link_page_mass_create(0,2063) #(первая страница каталога,последняя страница каталога+1)
link_mass_create(pre_link_mass,13) #(количество компаний на странице каталога+1)
create_file_csv(link_mass)
