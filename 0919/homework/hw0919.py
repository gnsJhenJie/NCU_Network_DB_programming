import csv
from tempfile import NamedTemporaryFile
import shutil

tempfile = NamedTemporaryFile(mode='w', delete=False)
fields = ['姓名', '期中成績', '期末成績', '學期成績']
scoredict = dict()

with open('score.csv', 'r+', newline='') as csvfile, tempfile:  # 記得要有newline=''否則不能正確解讀換行
    filewriter = csv.DictWriter(tempfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL, fieldnames=fields)
    filereader = csv.DictReader(csvfile)
    row = {'姓名': '姓名', '期中成績': '期中成績',
           '期末成績': '期末成績', '學期成績': '學期成績'}
    filewriter.writerow(row)
    for row in filereader:
        # print(row)
        if row['姓名'] == "李小明":
            row['期中成績'] = 60
        row['姓名'], row['期中成績'], row['期末成績'], row['學期成績'] = row['姓名'], row['期中成績'], row['期末成績'], float(
            row['期中成績'])*0.3 + float(row['期末成績'])*0.7
        # print(row)
        filewriter.writerow(row)
    row = {'姓名': input("輸入姓名"), '期中成績': input(
        "輸入期中成績"), '期末成績': input('輸入期末成績')}
    row['學期成績'] = float(
        row['期中成績'])*0.3 + float(row['期末成績'])*0.7
    filewriter.writerow(row)

shutil.move(tempfile.name, 'score.csv')
