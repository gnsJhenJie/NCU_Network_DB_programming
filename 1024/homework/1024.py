# see  https://pythonspot.com/wxpython-tabs/ for reference
# from random import choices
# from tkinter.ttk import Style
# from turtle import position
from pymongo import MongoClient
import pprint
import wx
import sqlite3 as lite
from PIL import Image
import io
import matplotlib.pyplot as plt


class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t_sid = wx.StaticText(self, -1, "姓名", (60, 20))
        self.tc_sid = wx.TextCtrl(self, pos=(60, 40), size=(300, -1))
        t_Fname = wx.StaticText(self, -1, "電話號碼", (60, 70))
        self.tc_Fname = wx.TextCtrl(self, pos=(60, 90), size=(300, -1))
        btn_insert = wx.Button(self, wx.ID_ANY, 'Insert', (200, 245))
        btn_insert.Bind(wx.EVT_BUTTON, self.onButtonInsert)

    def onButtonInsert(self, event):
        db.STUDENT.insert_one({
            "Name": self.tc_sid.Value,
            "Phone": self.tc_Fname.Value
        })
        self.tc_sid.Value = ""
        self.tc_Fname.Value = ""


class TabTwo(wx.Panel):

    def __init__(self, parent):  # init 記得不是Init
        wx.Panel.__init__(self, parent)
        t_sid = wx.StaticText(self, -1, "Post name", (60, 20))
        self.tc_Grade = wx.TextCtrl(self, pos=(60, 40), size=(150, -1))
        btn_show = wx.Button(self, wx.ID_ANY, 'Check', (230, 40))
        btn_show.Bind(wx.EVT_BUTTON, self.onButtonShow)
        self.t_cresult = wx.StaticText(self, -1, "", (350, 40))

        t_imgaddr = wx.StaticText(self, -1, "Image file address", (60, 80))
        self.tc_imgaddr = wx.TextCtrl(self, pos=(60, 100), size=(150, -1))

        self.tc_tagt = wx.TextCtrl(self, pos=(60, 140), size=(120, -1))
        self.tc_tagv = wx.TextCtrl(self, pos=(200, 140), size=(120, -1))
        btn_addt = wx.Button(self, wx.ID_ANY, 'add tag', (350, 140))
        btn_addt.Bind(wx.EVT_BUTTON, self.onButtonAddt)

        self.t_tags = wx.StaticText(self, -1, "tags", (60, 180))
        self.t_result = wx.StaticText(self, -1, "", (200, 180))

        btn_upload = wx.Button(self, wx.ID_ANY, 'upload', (300, 180))
        btn_upload.Bind(wx.EVT_BUTTON, self.onButtonUpload)

        self.tags = {}

    def onButtonShow(self, event):
        count = 0
        print("hi", self.tc_Grade.Value)
        count = db.IMAGE.count_documents({"Name": self.tc_Grade.Value})
        print(count)
        # pprint.pprint(STs)
        if count > 0:
            self.t_cresult.SetLabelText("post found")
        else:
            self.t_cresult.SetLabelText("post not found")
        pass

    def onButtonAddt(self, event):
        self.t_result.SetLabelText(
            self.t_result.LabelText+'\n'+self.tc_tagt.Value+":"+self.tc_tagv.Value)
        self.tags[self.tc_tagt.Value] = self.tc_tagv.Value
        self.tc_tagt.Value = ""
        self.tc_tagv.Value = ""
        pass

    def onButtonUpload(self, event):
        im = Image.open(self.tc_imgaddr.Value)
        image_bytes = io.BytesIO()
        im.save(image_bytes, format='JPEG')
        db.IMAGE.insert_one({
            "Name": self.tc_Grade.Value,
            "image": image_bytes.getvalue(),
        } | self.tags)
        self.tc_Grade.Value = ""
        self.tc_imgaddr = ""
        self.tc_tagt = ""
        self.tc_tagt = ""
        pass


class TabThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t_sid = wx.StaticText(self, -1, "Name", (60, 20))
        self.tc_sid = wx.TextCtrl(self, pos=(60, 40), size=(200, -1))
        btn_insert = wx.Button(self, wx.ID_ANY, 'search', (350, 40))
        btn_insert.Bind(wx.EVT_BUTTON, self.onButtonInsert)

        t_resultl = wx.StaticText(self, -1, "tags", (60, 80))
        self.t_result = wx.StaticText(self, -1, "", (120, 80))

    def onButtonInsert(self, event):
        img = db.IMAGE.find_one({
            "Name": self.tc_sid.Value,
        })
        if (img):
            pil_img = Image.open(io.BytesIO(img['image']))
            plt.imshow(pil_img)
            plt.show()
            self.t_result.SetLabelText("")
            print(type(img))
            # print(img)
            for i in img.items():
                if i[0] != "Name" and i[0] != "image" and i[0] != "_id":
                    if db.STUDENT.count_documents({"Name": i[1]}) > 0:
                        self.t_result.SetLabelText(
                            str(self.t_result.LabelText)+'\n'+i[0]+':'+i[1]+f"("+db.STUDENT.find_one({
                                "Name": i[1]
                            })['Phone']+")")
                    else:
                        self.t_result.SetLabelText(
                            str(self.t_result.LabelText)+'\n'+i[0]+':'+i[1])


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, None, title="109502573 109502571", size=wx.Size(500, 400))

        # Creating the Tab holders: Panel and Notebook
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # Creating the Tab windows
        tab1 = TabOne(nb)
        tab2 = TabTwo(nb)
        tab3 = TabThree(nb)

        # add Tabs to Notebook and give a name to the Tabs
        nb.AddPage(tab1, "Insert")
        nb.AddPage(tab2, "Image")
        nb.AddPage(tab3, "Search")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


client = MongoClient(host="localhost", port=27017)

db = client.School


app = wx.App()
MainFrame().Show()
app.MainLoop()
