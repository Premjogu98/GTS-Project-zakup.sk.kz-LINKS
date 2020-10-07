import re
import time
import urllib.request
import urllib.parse
import sys, os
import string
from datetime import datetime
import global_var
from InsertOnDatabase import insert_in_Local, create_filename
import requests
import html
# from googletrans import Translator
import dateparser


# def Translate_close(text_without_translate):
#     String2 = ""
#     try:
#         String2 = str(text_without_translate)
#         url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
#         response1 = requests.get(str(url))
#         response2 = response1.url
#         user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
#         headers = {'User-Agent': user_agent, }
#         request = urllib.request.Request(response2, None, headers)  # The assembled request
#         time.sleep(1)
#         response = urllib.request.urlopen(request)
#         htmldata: str = response.read().decode('utf-8')
#         time.sleep(1)
#         trans_data = re.search(r'(?<=dir="ltr" class="t0">).*?(?=</div>)', htmldata).group(0)
#         trans_data = html.unescape(str(trans_data))
#         return trans_data
#     except:
#         return String2


def Scrap_data(browser, get_htmlSource):
    try:
        for popup_close in browser.find_elements_by_xpath("/html/body/sk-app/sk-notifier/div/div/div/button[2]"):
            popup_close.click()
    except:
        pass

    SegFeild = []
    for data in range(42):
        SegFeild.append('')
    new_get_htmlSource: str = get_htmlSource.replace("\n", "")
    new_get_htmlSource: str = new_get_htmlSource.replace("<!---->", "").replace("&quot;", "\"").replace("&QUOT;","\"").replace("&nbsp;", " ").replace("&NBSP;", " ").replace("&amp;amp", "&").replace("&AMP;AMP", "&").replace("&amp;", "&").replace("&AMP;", "&").replace("&;amp", "&").replace("&;AMP", "&").replace(" ng-if=\"!isjson\"", "")
    new_get_htmlSource: str = re.sub('\s+', ' ', new_get_htmlSource)

    try:
        # Due_date = re.search(r'(?<=jhitranslate="main.dialog.acceptanceEndDateTime">).*?(?=</div> </div> <div)', new_get_htmlSource).group(0)
        # Due_date = re.search(r'(?<=class="m-rangebox__date">).*?(?=</div>)', Due_date).group(0)
        # time.sleep(3)
        Due_date = ''
        Due_Date_b = browser.find_elements_by_xpath('//*[@class="m-rangebox__date"]')
        if len(Due_Date_b) == 2:
            Due_Date = Due_Date_b[1].get_attribute('innerText')
            Due_Date = Due_Date.replace('.','').replace('г','').replace(',','').lower().strip()
            Due_date = re.sub('\s+', ' ', Due_Date)
        if Due_date != "":
            Due_date = Due_date.replace("p.m.", "").strip()
            Due_date = Due_date.replace("a.m.", "").strip()
            Due_date = Due_date[:-5].strip()
            datetime = dateparser.parse(str(Due_date))
            if datetime is None or datetime == '':
                browser.switch_to.window(browser.window_handles[0])
                for i in browser.find_elements_by_xpath('//*[@id="source"]'):
                    i.clear()
                    time.sleep(2)
                    i.send_keys(str(Due_date))
                    break
                time.sleep(2)
                for Due_date in browser.find_elements_by_xpath('//*[@class="tlid-translation translation"]'):
                    Due_date = Due_date.get_attribute('innerText').strip()
                    break
                browser.switch_to.window(browser.window_handles[1])
                datetime = dateparser.parse(str(Due_date))
                mydate = datetime.strftime("%Y-%m-%d")
            else:   
                mydate = datetime.strftime("%Y-%m-%d")
            
            SegFeild[24] = mydate.strip()
            a = 0
            while a == 0:
                    try:
                        #  ========================================================================================================
                        # Email
                        try:
                            Email = re.search(r'(?<=main.dialog.email"><span>).*?(?=<div)', new_get_htmlSource).group(0)
                            Email = re.search(r'(?<=</div>).*?(?=</div>)', Email).group(0).strip()
                            SegFeild[1] = Email
                        except:
                            pass

                        #  ========================================================================================================
                        # Address
                        Address = ""
                        Phone = ""

                        Address_test = ''
                        Address_test = str(new_get_htmlSource).partition('МЕСТО ПОСТАВКИ</span></div>')[2].partition("</span> </div> </div> <div")[0].strip()
                        clean = re.compile('<.*?>')
                        Address_test = re.sub(clean, '', Address_test).replace(",", " ")
                        Address_test = re.sub(' +', ' ', Address_test).strip()
                        if Address_test != '':
                            # Address_test = Translate(Address_test)
                            Address_test = string.capwords(str(Address_test))
                        if Address_test == '':
                            for Address_test in browser.find_elements_by_xpath('/html/body/ngb-modal-window/div/div/sk-main-dialog/div[3]/div[3]/div/div[1]/div[6]/div[1]'):
                                Address_test = Address_test.get_attribute("innerText").strip()
                                if Address_test == "МЕСТО ПОСТАВКИ":
                                    time.sleep(2)
                                    for Address in browser.find_elements_by_xpath('/html/body/ngb-modal-window/div/div/sk-main-dialog/div[3]/div[3]/div/div[1]/div[6]/div[2]'):
                                        Address = Address.get_attribute("innerText")
                                        # Address = Translate(Address)
                                        Address_test = string.capwords(str(Address))
                                    break
                                else:
                                    Address_test = ''
                        time.sleep(1.5)
                        if Address_test == "":
                            for Address_test in browser.find_elements_by_xpath('/html/body/ngb-modal-window/div/div/sk-main-dialog/div[3]/div[3]/div/div[1]/div[5]/div[1]'):
                                Address_test = Address_test.get_attribute("innerText").strip()
                                if Address_test == "МЕСТО ПОСТАВКИ":
                                    time.sleep(2)
                                    for Address in browser.find_elements_by_xpath('/html/body/ngb-modal-window/div/div/sk-main-dialog/div[3]/div[3]/div/div[1]/div[5]/div[2]'):
                                        Address = Address.get_attribute("innerText")
                                        # Address = Translate(Address)
                                        Address_test = string.capwords(str(Address))
                        else:
                            pass

                        try:
                            Phone = re.search(r'(?<=main.dialog.phone"><span>).*?(?=<div)', new_get_htmlSource).group(0)
                            Phone = re.search(r'(?<=</div>).*?(?=</div>)', Phone).group(0).strip()
                        except:
                            pass
                        Collected_Address = Address_test.replace("\"", "").strip() + "<br>\n" + "Телефон: " + Phone
                        SegFeild[2] = Collected_Address

                        #  ========================================================================================================
                        # Country
                        SegFeild[7] = "KZ"

                        #  ========================================================================================================
                        # Customer name
                        try:
                            Customer = re.search(r'(?<=main.dialog.customer"><span>).*?(?=<div)', new_get_htmlSource).group(
                                0)
                            Customer = re.search(r'(?<=</div>).*?(?=</div>)', Customer).group(0).upper()
                            Customer = Customer.replace("<!---->", "")
                            Customer = Customer.replace("\"", " ").strip()
                            if Customer != "":
                                # Customer = Translate(Customer)
                                SegFeild[12] = Customer.upper()
                        except:
                            pass
                        #  ========================================================================================================
                        # Tender no
                        try:
                            tender_no = re.search(r'(?<=class="m-modal__num">).*?(?=</div>)',
                                                  new_get_htmlSource).group(0).replace("№", "").replace(" ", "").strip()
                            SegFeild[13] = tender_no
                        except:
                            pass
                        #  ========================================================================================================
                        # notice type
                        SegFeild[14] = "2"

                        #  ========================================================================================================
                        # Tender Details
                        Title = ""
                        tender_no_detail = ""
                        ENC_TRU_code = ""
                        brief_description = ""
                        Status = ""
                        amount = ""
                        unit_of_measurement = ""
                        Unit_price = ""
                        Amount = ""
                        MONTH_OF_CARRYING_OUT = ""
                        TERMS = ""
                        TERMS_OF_PAYMENT = ""
                        PURCHASE_METHOD = ""
                        total_amount = ""
                        try:
                            Title = re.search(r'(?<=class="m-modal__title m-title m-title--h2">).*?(?=</div>)',
                                              new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            Title = re.sub(clean, '', Title).strip(" ", )
                            if Title != "":
                                # Title = Translate(Title)
                                Title = string.capwords(str(Title))
                        except:
                            pass
                        try:
                            tender_no_detail = re.search(
                                r'(?<=cursor: pointer; text-decoration: inherit;").*?(?=<legend class=")',
                                new_get_htmlSource).group(0).replace("№", "").replace(">", "").replace(" ", "").strip()
                            # if tender_no_detail != "":
                                # tender_no_detail = Translate(tender_no_detail)

                        except:
                            pass

                        try:
                            ENC_TRU_code = re.search(r'(?<=Код ЕНС ТРУ</span></div>).*?(?=</div>)',
                                                     new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            ENC_TRU_code = re.sub(clean, '', ENC_TRU_code).strip()
                        except:
                            pass

                        try:
                            brief_description = re.search(r'(?<=Краткая характеристика</span></div>).*?(?=</div>)',
                                                          new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            brief_description = re.sub(clean, '', brief_description).strip()
                            if brief_description != "":
                                # brief_description = Translate(brief_description)
                                brief_description = string.capwords(str(brief_description)).strip()
                        except:
                            pass

                        try:
                            Status = re.search(r'(?<=Статус</span></div>).*?(?=</div>)', new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            Status = re.sub(clean, '', Status).strip()
                            if Status != "":
                                # Status = Translate(Status)
                                Status = string.capwords(str(Status)).strip()
                        except:
                            pass

                        try:
                            amount = re.search(r'(?<=Количество</span></div>).*?(?=</div>)', new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            amount = re.sub(clean, '', amount).strip()
                            amount = re.sub(' +', ' ', str(amount))  # Remove Multiple Spaces From String
                        except:
                            pass

                        try:
                            unit_of_measurement = re.search(r'(?<=Единица измерения</span></div>).*?(?=</div>)',
                                                            new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            unit_of_measurement = re.sub(clean, '', unit_of_measurement).strip()
                        except:
                            pass

                        try:
                            Unit_price = re.search(r'(?<=Цена за единицу</span></div>).*?(?=</div>)',
                                                   new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            Unit_price = re.sub(clean, '', Unit_price).strip()
                        except:
                            pass

                        try:
                            Amount = re.search(r'(?<=Сумма</span></div>).*?(?=</div>)', new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            Amount = re.sub(clean, '', Amount).strip()
                        except:
                            pass

                        try:
                            MONTH_OF_CARRYING_OUT = re.search(r'(?<=МЕСЯЦ ПРОВЕДЕНИЯ</span></div>).*?(?=</div>)',
                                                              new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            MONTH_OF_CARRYING_OUT = re.sub(clean, '', MONTH_OF_CARRYING_OUT).strip()
                        except:
                            pass

                        try:
                            TERMS = re.search(r'(?<=СРОКИ</span></div>).*?(?=</div>)', new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            TERMS = re.sub(clean, '', TERMS).strip()
                            if TERMS != "":
                                TERMS_list = []
                                TERMS = [TERMS[idx:idx + 100] for idx, val in enumerate(TERMS) if idx % 100 == 0]
                                for TERMS in TERMS:
                                    # TERMS = Translate(TERMS)
                                    TERMS_list.append(TERMS)
                                for TERMS_list in TERMS_list:
                                    TERMS += TERMS_list
                                TERMS = string.capwords(str(TERMS))
                        except:
                            pass

                        try:
                            TERMS_OF_PAYMENT = re.search(
                                r'(?<=УСЛОВИЯ ОПЛАТЫ</span></div>).*?(?=</div> </div> </div> <div)',
                                new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            TERMS_OF_PAYMENT = re.sub(clean, '', TERMS_OF_PAYMENT)
                            TERMS_OF_PAYMENT = re.sub(' +', ' ', TERMS_OF_PAYMENT)
                            TERMS_OF_PAYMENT = TERMS_OF_PAYMENT.replace("%", "% , ")
                            # if TERMS_OF_PAYMENT != "":
                            #     TERMS_OF_PAYMENT = Translate(TERMS_OF_PAYMENT)
                        except:
                            pass

                        try:
                            PURCHASE_METHOD = re.search(r'(?<=МЕТОД ЗАКУПКИ</span></div>).*?(?=</div> <div)',
                                                        new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            PURCHASE_METHOD = re.sub(clean, '', PURCHASE_METHOD).strip()
                            # if PURCHASE_METHOD != "":
                            #     PURCHASE_METHOD = Translate(PURCHASE_METHOD)
                        except:
                            pass

                        try:
                            total_amount = re.search(r'(?<=Общая сумма лотов</span></div>).*?(?=</div> </div>)',
                                                     new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            total_amount = re.sub(clean, '', total_amount).strip()
                        except:
                            pass

                        TenderDetails = str(Title) + "<br>\n""Тендер № детали: " + str(
                            tender_no_detail) + "<br>\n""Код ENC TRU: " + str(
                            ENC_TRU_code) + "<br>\n""Краткое описание: " + str(brief_description) + "<br>\n" \
                                                                                                     "статус: " + str(
                            Status) + "<br>\n""Количество: " + str(amount) + "<br>\n""Единица измерения: " + str(
                            unit_of_measurement) + "<br>\n""Цена за единицу: " + str(Unit_price) + "<br>\n" \
                                                                                              "Количество: " + str(
                            Amount) + "<br>\n""Месяц проведения: " + str(
                            MONTH_OF_CARRYING_OUT) + "<br>\n""сроки: " + str(TERMS) + "<br>\n""Условия оплаты: " + str(
                            TERMS_OF_PAYMENT) + "<br>\n" \
                                                "сроки: " + str(
                            PURCHASE_METHOD) + "<br>\n""Общее количество лотов: " + str(
                            total_amount)
                        SegFeild[18] = TenderDetails

                        try:
                            Title = re.search(r'(?<=class="m-modal__title m-title m-title--h2">).*?(?=</div>)',
                                              new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            Title = re.sub(clean, '', Title).strip()
                            if Title != "":
                                # Title = Translate(Title)
                                Title = string.capwords(str(Title))
                            SegFeild[19] = Title
                        except:
                            pass

                        try:
                            total_amount = re.search(r'(?<=Общая сумма лотов</span></div>).*?(?=</div> </div>)',new_get_htmlSource).group(0)
                            clean = re.compile('<.*?>')
                            total_amount = re.sub(clean, '', total_amount).strip()
                            total_amount = total_amount.replace(' ','').replace('₸','').replace(',','.')
                            SegFeild[20] = total_amount.strip()
                        except:
                            pass
                        if str(SegFeild[20]) != '':
                            SegFeild[21] = 'KZT'
                        # try:
                        #     Due_date = re.search(r'(?<=class="m-rangebox__date">).*?(?=</div>)', new_get_htmlSource).group(0)
                        #     Due_date = Due_date.replace("p.m.", "").strip()
                        #     Due_date = Due_date.replace("a.m." , "").strip()
                        #     if Due_date != "":
                        #         Due_date = Translate(Due_date)
                        #     if Due_date != '':
                        #         datetime_object = datetime.strptime(Due_date , '%B %d, %Y %H:%M')
                        #         mydate = datetime_object.strftime("%Y-%m-%d")
                        #         SegFeild[24] = mydate.strip()
                        #     else:
                        #         SegFeild[24] = ""
                        # except Exception as e:
                        #     print("Error: ",e)
                        SegFeild[22] = "0"
                        SegFeild[26] = "0.0"
                        SegFeild[27] = "0"  # Financier
                        SegFeild[28] = "https://zakup.sk.kz/#/ext(popup:item/" + str(SegFeild[13]) + "/advert)"
                        # Source Name
                        SegFeild[31] = 'zakup.sk.kz'

                        SegFeild[42] = SegFeild[7]

                        SegFeild[43] = ''

                        for SegIndex in range(len(SegFeild)):
                            print(SegIndex, end=' ')
                            print(SegFeild[SegIndex])
                            SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                            SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''")
                        a = 1
                        if len(SegFeild[19]) >= 200:
                            SegFeild[19] = str(SegFeild[19])[:200] + '...'
                        check_date(get_htmlSource, SegFeild)
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
                        a = 0
        else:
            print(" ♥ Deadline was not given ♥ ")
            global_var.deadline_Not_given += 1
    # except:
    #     print(" ♥ Deadline was not given ♥ ")
    #     global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)


def check_date(get_htmlSource, SegFeild):
    tender_date = str(SegFeild[24])
    nowdate = datetime.now()
    date2 = nowdate.strftime("%Y-%m-%d")
    try:
        if tender_date != '':
            deadline = time.strptime(tender_date, "%Y-%m-%d")
            currentdate = time.strptime(date2, "%Y-%m-%d")
            if deadline > currentdate:
                insert_in_Local(get_htmlSource, SegFeild)
                print('Live Tender')
            else:
                print("Tender Expired")
                global_var.expired += 1
        else:
            print("Deadline was not given")
            global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
