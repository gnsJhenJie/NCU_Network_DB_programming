from course.models import Course_enrollment, Course
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def detail(request, sid, cid):
    try:
        c = Course.objects.get(CID=cid)
        ce = Course_enrollment.objects.get(SID=sid, CID=c)

        s = f"""
        <html>
        <head></head>
        <body>
        <h1>學生{sid}在{cid}的學期末成績
        <br/>
        {ce.Score}
        <br/>
        修課結果:{"及格" if ce.Score>60 else "不及格"}
        </h1>
        
        </body>
        </html>
        """
        return HttpResponse(s)
    except:
        s = f"""
        <html>
        <head></head>
        <body>
        <h1>查無修課成績
        </h1>
        </body>
        </html>
        """
        return HttpResponse(s)
