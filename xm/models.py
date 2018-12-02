from django.db import models

# Create your models here.
class Info(models.Model):
    salary=models.CharField(max_length=1000)
    company=models.CharField(max_length=1000)
    company_address=models.CharField(max_length=1000)
    position1=models.CharField(max_length=1000)
    company_size=models.CharField(max_length=1000)
    company_ip=models.CharField(max_length=1000)
    company_nature=models.CharField(max_length=1000)
    company_business=models.CharField(max_length=1000)
    exp_require=models.CharField(max_length=1000)
    edu_require=models.CharField(max_length=1000)
    recruit_num=models.CharField(max_length=1000)
    city=models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    status1=models.CharField(max_length=1000)
    status2=models.CharField(max_length=1000)
    class Meta:
        db_table='info'
class Regist(models.Model):
    userid=models.CharField(max_length=30)
    usrtel=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    psw=models.CharField(max_length=30)
