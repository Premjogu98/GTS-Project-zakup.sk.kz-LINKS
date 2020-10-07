import wx
import global_var
import pymysql.cursors
import sys, os
import time


def Local_connection_links():
    a = 0
    while a == 0:
        try:
            connection = pymysql.connect(host='185.142.34.92',
                                         user='ams',
                                         password='TgdRKAGedt%h',
                                         db='tenders_db',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            sql = 'SELECT COUNT(*) FROM `zakupskkz_temptbl`'
            cursor = connection.cursor()
            cursor.execute(sql)
            Links : str = cursor.fetchall()
            global_var.Links = str(Links).partition(':')[2].partition("}")[0].strip()
            a = 1
        except pymysql.connect  as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


Local_connection_links()


class MainWindow(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition,
                          wx.Size(300, 200),
                          wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |
                                                      wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        # ------ Area for the user's controls
        userin = wx.Panel(self, -1, (0, 100), (200, 100))

        wx.StaticText(userin, -1, "Number Of Links Fetch", pos=(20, 13))

        wx.StaticText(userin, -1, "Number Of Links Remaining :  "+str(global_var.Links)+"", pos=(20, 40))
        # ------ Area for user to input text
        userbox = wx.TextCtrl(userin, -1, "", pos=(150, 10))
        self.box1 = userbox

        # ------ Button to take text from userbox and place it in textarea
        Press = wx.Button(userin, -1, "Get Links", (45, 80))

        Press.Bind(wx.EVT_BUTTON, self.inserttext)

        Close = wx.Button(userin, -1, "Close", (45, 110))

        Close.Bind(wx.EVT_BUTTON, self.onClose)

    def inserttext(self, event):
        global_var.Number_Of_Links = self.box1.GetValue()
        print("Number OF Link Selected: ", global_var.Number_Of_Links)

    def mouseclick(self, event):
        self.box1.Clear()

    def onClose(self, event):
        self.Close()


class MainApp(wx.App):
    def OnInit(self):
        myWindow = MainWindow(None, -1, "zakup.sk.kz")
        myWindow.Show(True)
        self.SetTopWindow(myWindow)
        return (True)


AppStart = MainApp(0)
AppStart.MainLoop()

from Navigating_Page import Collect_Link
Collect_Link()
