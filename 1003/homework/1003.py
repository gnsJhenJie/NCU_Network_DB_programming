# see  https://pythonspot.com/wxpython-tabs/ for reference
# from random import choices
# from tkinter.ttk import Style
# from turtle import position
import wx
import sqlite3 as lite


class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t_sid = wx.StaticText(self, -1, "SID", (60, 20))
        self.tc_sid = wx.TextCtrl(self, pos=(60, 40), size=(300, -1))
        t_Fname = wx.StaticText(self, -1, "Fname", (60, 70))
        self.tc_Fname = wx.TextCtrl(self, pos=(60, 90), size=(300, -1))
        t_Lname = wx.StaticText(self, -1, "Lname", (60, 120))
        self.tc_Lname = wx.TextCtrl(self, pos=(60, 140), size=(300, -1))
        t_Grade = wx.StaticText(self, -1, "Grade", (60, 170))
        self.cho_Grade = wx.ComboBox(
            self, choices=[str(i) for i in range(1, 5)], pos=(60, 190))
        t_Sex = wx.StaticText(self, -1, "Sex", (60, 220))
        self.rb_Sex = wx.RadioBox(self, label='', pos=(60, 240), choices=['男', '女'],
                                  majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        btn_insert = wx.Button(self, wx.ID_ANY, 'Insert', (200, 245))
        btn_insert.Bind(wx.EVT_BUTTON, self.onButtonInsert)

    def onButtonInsert(self, event):
        con = lite.connect('./dbtest.db')
        with con:
            cur = con.cursor()
            cur.execute(
                f"Insert into STUDENT Values('{self.tc_sid.Value}', '{self.tc_Fname.Value}',' {self.tc_Lname.Value}', {self.cho_Grade.GetSelection()+1}, '{self.rb_Sex.GetString(self.rb_Sex.GetSelection())}')")
            con.commit()


class TabTwo(wx.Panel):

    def __init__(self, parent):  # init 記得不是Init
        wx.Panel.__init__(self, parent)
        t_sid = wx.StaticText(self, -1, "Grade", (60, 20))
        self.cho_Grade = wx.ComboBox(
            self, choices=[str(i) for i in range(1, 5)], pos=(60, 40))
        btn_show = wx.Button(self, wx.ID_ANY, 'Show', (200, 40))
        btn_show.Bind(wx.EVT_BUTTON, self.onButtonShow)
        self.t_result = wx.StaticText(self, -1, "", (60, 60))

    def onButtonShow(self, event):
        con = lite.connect('./dbtest.db')
        with con:
            cur = con.cursor()
            cur.execute(
                f"select * from STUDENT where Grade={self.cho_Grade.GetSelection()+1}")
            rows = cur.fetchall()
            self.t_result.SetLabelText('')
            for row in rows:
                self.t_result.SetLabelText(
                    self.t_result.GetLabelText()+'\n'+str(row))
            con.commit()


class TabAvg(wx.Panel):

    def __init__(self, parent):  # init 記得不是Init
        wx.Panel.__init__(self, parent)
        t_course = wx.StaticText(self, -1, "Course",
                                 (60, 20))
        con = lite.connect('./dbtest.db')
        rows = []
        rows2 = []
        with con:
            cur = con.cursor()
            cur.execute(
                f"select CID from COURSE")
            rows = cur.fetchall()
        for row in rows:
            rows2.append(str(row[0]))
        self.cho_Course = wx.ComboBox(
            self, choices=rows2, pos=(60, 40))
        btn_count = wx.Button(self, wx.ID_ANY, 'Count', (60, 80))
        btn_count.Bind(wx.EVT_BUTTON, self.onButtonCount)
        self.t_result = wx.StaticText(self, -1, "", (60, 100))

    def onButtonCount(self, event):
        con = lite.connect('./dbtest.db')
        with con:
            cur = con.cursor()
            cur.execute(
                f"SELECT AVG(Score) FROM ENROLLMENT WHERE CID='{self.cho_Course.GetString(self.cho_Course.GetSelection())}';")
            rows = cur.fetchall()
            self.t_result.SetLabelText('')
            self.t_result.SetLabelText(
                self.t_result.GetLabelText()+'\nAvg Score: '+str(rows[0][0]))
            cur.execute(
                f"SELECT SID,MAX(Score) FROM ENROLLMENT WHERE CID='{self.cho_Course.GetString(self.cho_Course.GetSelection())}' ;")
            rows = cur.fetchall()
            cur.execute(
                f"SELECT Fname,Lname FROM STUDENT WHERE SID='{rows[0][0]}'")
            rows2 = cur.fetchall()
            self.t_result.SetLabelText(
                self.t_result.GetLabelText()+'\nMax: '+str(rows2[0][0]) + ' ' + str(rows2[0][1]) + ' ' + str(rows[0][1]))


class TabUpdate(wx.Panel):

    def __init__(self, parent):  # init 記得不是Init
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Search with SID and CID", (60, 20))
        t_sid = wx.StaticText(self, -1, "SID", (60, 40))
        con = lite.connect('./dbtest.db')
        rows = []
        rows2 = []
        with con:
            cur = con.cursor()
            cur.execute(
                f"select SID from ENROLLMENT")
            rows = cur.fetchall()
        for row in rows:
            rows2.append(str(row[0]))
        self.cho_sid = wx.ComboBox(
            self, choices=rows2, pos=(60, 60))
        t_sid = wx.StaticText(self, -1, "CID", (140, 40))
        rows = []
        rows2 = []
        with con:
            cur = con.cursor()
            cur.execute(
                f"select CID from ENROLLMENT")
            rows = cur.fetchall()
        for row in rows:
            rows2.append(str(row[0]))
        self.cho_cid = wx.ComboBox(
            self, choices=rows2, pos=(140, 60))
        btn_search = wx.Button(self, wx.ID_ANY, 'Search', (210, 60))
        btn_search.Bind(wx.EVT_BUTTON, self.onButtonSearch)
        self.t_score = wx.StaticText(self, -1, "Score:", (300, 60))
        self.tc_update = wx.TextCtrl(self, pos=(60, 90), size=(30, -1))
        btn_update = wx.Button(self, wx.ID_ANY, 'Enter to update', (130, 90))
        btn_update.Bind(wx.EVT_BUTTON, self.onButtonUpdate)

    def onButtonSearch(self, event):
        con = lite.connect('./dbtest.db')
        rows = []
        with con:
            cur = con.cursor()
            cur.execute(
                f"SELECT Score FROM ENROLLMENT WHERE CID='{self.cho_cid.GetString(self.cho_cid.GetSelection())}' AND SID = '{self.cho_sid.GetString(self.cho_sid.GetSelection())}';")
            rows = cur.fetchall()
        self.t_score.SetLabelText("Score: "+str(rows[0][0]))

    def onButtonUpdate(self, event):
        con = lite.connect('./dbtest.db')
        rows = []
        with con:
            cur = con.cursor()
            cur.execute(
                f"update ENROLLMENT set SCORE = {self.tc_update.Value} where CID='{self.cho_cid.GetString(self.cho_cid.GetSelection())}' AND SID = '{self.cho_sid.GetString(self.cho_sid.GetSelection())}'")


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
        tab3 = TabAvg(nb)
        tab4 = TabUpdate(nb)

        # add Tabs to Notebook and give a name to the Tabs
        nb.AddPage(tab1, "Insert")
        nb.AddPage(tab2, "Show")
        nb.AddPage(tab3, "Avg")
        nb.AddPage(tab4, "Update")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


app = wx.App()
MainFrame().Show()
app.MainLoop()
