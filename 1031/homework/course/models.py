from django.db import models

# Create your models here.


class Course(models.Model):
    CID = models.TextField(u'CID')

    def __unicode__(self):
        return self.title


class Course_enrollment(models.Model):
    CID = models.ForeignKey('Course', on_delete=models.CASCADE)
    SID = models.TextField(u'SID')
    midScore = models.FloatField(u'midScore')
    finalScore = models.FloatField(u'finalScore')
    Score = models.FloatField(u'Score')

    class Meta:
        db_table = "course_enrollment"

    def __unicode__(self):
        return self.title

# Course.objects.create(SID="D01",CID="C01",midScore=100,finalScore=100,Score=100)
