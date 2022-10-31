import sqlite3 as lite

con = lite.connect('sqlite0926.db')

with con:
    cur = con.cursor()

    cur.execute('DELETE from ENROLLMENT')
    cur.execute("Delete from STUDENT")
    cur.execute("Delete from COURSE")

    cur.execute("Insert into STUDENT Values('D01', 'THOMAS', 'TUCKER', 3, '男')")
    cur.execute("Insert into STUDENT Values('D02', 'KAYLEE', 'SIMPSON', 3, '女')")
    cur.execute("Insert into STUDENT Values('D03', 'LEVI', 'BROOKS', 1, '男')")

    cur.execute("Insert into COURSE Values('C01','計概')")
    cur.execute("Insert into COURSE Values('C02','網路概論')")

    cur.execute("Insert into ENROLLMENT (SID,CID) Values('D01','C01')")
    cur.execute("Insert into ENROLLMENT (SID,CID) Values('D02','C01')")
    cur.execute("Insert into ENROLLMENT (SID,CID) Values('D03','C02')")

    con.commit()
    input("Insert done, press ENTER to continue")

    cur.execute(
        "update ENROLLMENT set MidScore=50, FinalScore=100, Score=85 where SID='D01'")
    cur.execute(
        "update ENROLLMENT set MidScore=60, FinalScore=80, Score=74 where SID='D02'")
    cur.execute(
        "update ENROLLMENT set MidScore=20, FinalScore=75, Score=58.5 where SID='D03'")

    con.commit()
    input("Update done, press ENTER to continue")

    cur.execute("select SID from ENROLLMENT where Score<60")
    print("Failed SIDs:")
    rows = cur.fetchall()
    for row in rows:
        print(row[0])

    cur.execute("delete from ENROLLMENT where Score<60")


con.commit()
con.close()
