from django.db import models

class login_table(models.Model):
    username=models.CharField(max_length=25)
    password=models.CharField(max_length=25)
    type=models.CharField(max_length=25)


class staff_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    fname=models.CharField(max_length=25)
    lname=models.CharField(max_length=25)
    dob=models.DateField()
    gender=models.CharField(max_length=25)
    place=models.CharField(max_length=25)
    post=models.CharField(max_length=25)
    pin=models.IntegerField()
    phone=models.BigIntegerField()
    email=models.CharField(max_length=25)
    photo=models.FileField()

class user_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    dob = models.DateField()
    gender = models.CharField(max_length=25)
    place = models.CharField(max_length=25)
    post = models.CharField(max_length=25)
    pin = models.IntegerField()
    phone = models.BigIntegerField()
    email = models.CharField(max_length=25)
    photo = models.FileField()

class complaint_table(models.Model):
    complain=models.CharField(max_length=25)
    replay=models.CharField(max_length=25)
    user=models.ForeignKey(user_table,on_delete=models.CASCADE)
    date=models.DateField()

class feedback_table(models.Model):
    Feedback=models.CharField(max_length=25)
    user=models.ForeignKey(user_table,on_delete=models.CASCADE)
    date = models.DateField()

class notification_table(models.Model):
    notification=models.CharField(max_length=25)
    date=models.DateField()

class assignwork_table(models.Model):
    work=models.CharField(max_length=25)
    staff=models.ForeignKey(staff_table,on_delete=models.CASCADE)
    description=models.CharField(max_length=25)
    date=models.DateField()
    deadline=models.DateField()
    status=models.CharField(max_length=25)


class usernotification_table(models.Model):
    user=models.ForeignKey(user_table,on_delete=models.CASCADE)
    staff=models.ForeignKey(staff_table,on_delete=models.CASCADE)
    image=models.FileField()
    date=models.DateField()
    status=models.CharField(max_length=25)


