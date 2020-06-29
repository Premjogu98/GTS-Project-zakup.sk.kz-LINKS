from selenium import webdriver
import time
from Scraping_Things import  Scrap_data
import sys, os
import global_var
import ctypes
import pymysql.cursors


def Local_connection_links():
    a = 0
    while a == 0:
        try:
            # File_Location = open(
            #     "D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\zakup_sk_kz\\Location For Database & Driver.txt",
            #     "r")
            # TXT_File_AllText = File_Location.read()

            # Local_host = str(TXT_File_AllText).partition("Local_host_link=")[2].partition(",")[0].strip()
            # Local_user = str(TXT_File_AllText).partition("Local_user_link=")[2].partition(",")[0].strip()
            # Local_password = str(TXT_File_AllText).partition("Local_password_link=")[2].partition(",")[0].strip()
            # Local_db = str(TXT_File_AllText).partition("Local_db_link=")[2].partition(",")[0].strip()
            # Local_charset = str(TXT_File_AllText).partition("Local_charset_link=")[2].partition("\")")[0].strip()

            connection = pymysql.connect(host='185.142.34.92',
                                         user='ams',
                                         password='TgdRKAGedt%h',
                                         db='tenders_db',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except pymysql.connect  as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


def Collect_Link():
    a = 0
    while a == 0:
        try:
            Links_List = []
            mydb_Local = Local_connection_links()
            mycursorLocal = mydb_Local.cursor()
            mycursorLocal.execute(f"SELECT `doc_links` FROM `zakupskkz_temptbl` ORDER BY ID DESC LIMIT {str(global_var.Number_Of_Links)}")
            rows = mycursorLocal.fetchall()
            for row in rows:
                links = "%s" % (row["doc_links"])
                if links not in Links_List:
                    Links_List.append(links)
            print("Number OF Link Get From Database: ",len(Links_List))
            navigating_pages(Links_List)
            a = 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


def navigating_pages(Collected_T_Number):
    # File_Location = open("D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\zakup_sk_kz\\Location For Database & Driver.txt", "r")
    # TXT_File_AllText = File_Location.read()
    # Chromedriver = str(TXT_File_AllText).partition("Driver=")[2].partition("\")")[0].strip()
    # browser = webdriver.Chrome(executable_path=str(Chromedriver))
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"))
    browser.maximize_window()
    a = 0
    while a == 0:
        try:
            for href in Collected_T_Number:
                for popup_close in browser.find_elements_by_xpath(
                        "/html/body/sk-app/sk-notifier/div/div/div/button[1]"):
                    popup_close.click()
                    break

                for tab_close in browser.find_elements_by_class_name("m-modal__close-button"):
                    tab_close.click()
                    break

                browser.get(href)
                global_var.Total += 1
                for popup_close in browser.find_elements_by_xpath("/html/body/sk-app/sk-notifier/div/div/div/button[1]"):
                    popup_close.click()
                    break
                time.sleep(2)
                for Document in browser.find_elements_by_xpath("/html/body/ngb-modal-window/div/div/sk-main-dialog/div[2]/div[5]/div/div[2]/div[1]/div/div/button/span[2]/span"):
                    Document.click()
                    break
                b = 0
                while b == 0:
                    try:
                        for get_HTML_data in browser.find_elements_by_class_name("modal-content"):
                            get_htmlSource = get_HTML_data.get_attribute("outerHTML")
                            if get_htmlSource != "":
                                get_htmlSource = get_htmlSource.replace("""<svg xmlns:xlink="http://www.w3.org/1999/xlink" class="icon__svg" version="1.1" viewBox="0 0 512 512" x="0px" xmlns="http://www.w3.org/2000/svg" y="0px">""" ,"")
                                get_htmlSource = get_htmlSource.replace("href=\"" , "href=\"https://zakup.sk.kz/")
                                get_htmlSource = get_htmlSource.replace("<li class=\"m-list__layout\">" , "")
                                get_htmlSource = get_htmlSource.replace("<button " , "")
                                get_htmlSource = get_htmlSource.replace("class=\"button button--default\" type=\"button\">" , "")
                                Scrap_data(browser, get_htmlSource)
                            else:pass
                            b = 1
                    except:
                        b = 0
                DeleteLink_From_Database(href)

            ctypes.windll.user32.MessageBoxW(0, "Total: " + str(global_var.Total) + "\n""Duplicate: " + str(
                global_var.duplicate) + "\n""Expired: " + str(global_var.expired) + "\n""Inserted: " + str(
                global_var.inserted) + "\n""Deadline Not given: " + str(
                global_var.deadline_Not_given) + "\n""QC Tenders: " + str(
                global_var.QC_Tender) + "\n""Delete From Database: " + str(global_var.Delete_From_database) + "",
                                             "Zakup_sk_kz", 1)
            global_var.Process_End()
            browser.close()
            sys.exit()
            a = 1
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)
            a = 0


def DeleteLink_From_Database(href):
    mydb_Local = Local_connection_links()
    mycursorLocal = mydb_Local.cursor()
    a5 = 0
    while a5 == 0:
        try:
            mydb_Local = Local_connection_links()
            mycursorLocal = mydb_Local.cursor()
            mycursorLocal.execute(f"DELETE FROM `zakupskkz_temptbl` WHERE `doc_links` = '{str(href)}'")
            mydb_Local.commit()
            global_var.Delete_From_database += 1
            print("Link Delete From Table")
            print(" Total: " + str(global_var.Total) + " Duplicate: " + str(
                global_var.duplicate) + " Expired: " + str(global_var.expired) + " Inserted: " + str(
                global_var.inserted) + " Deadline Not given: " + str(
                global_var.deadline_Not_given) + " QC Tenders: " + str(
                global_var.QC_Tender) + " Delete From Database: " + str(global_var.Delete_From_database),'\n')
            mycursorLocal.close()
            mydb_Local.close()
            a5 = 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            a5 = 0
            mycursorLocal.close()
            mydb_Local.close()


Collect_Link()


