from django.db import models

from django.contrib.auth.models import User

CONNECTION_TYPE = (
    ('1','OUTGOING'),
    ('2','INCOMING'),
)

class Company(models.Model):
    name = models.CharField(max_length=50)
    client_id = models.CharField(max_length=50)
    userid = models.ForeignKey(User)


    def __unicode__(self):
        return u'%s' % (self.name)




     
class Number(models.Model):
    full_number = models.CharField(max_length=50)
    client_id = models.CharField(max_length=50)
    separate_billing = models.BooleanField()

    
    
    def __unicode__(self):
        return u'%s' % (self.full_number)




#1) source of the call ex. 227383060
#2) destination, ex 600026904
#3) duration of the call like "124" seconds
#4) exact datetime of the beginning of the call,
#5) exact datetime of the end of the call,
#6) operator - trunk in which connection was originated
#7) uniqueid of the connection
#8) type
#9) host

class Connection(models.Model):
    source = models.CharField(max_length=50)
    destination =  models.CharField(max_length=50)
    duration = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    operator = models.CharField(max_length=50)
    uniqueid = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    host = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)



    def __unicode__(self):

        client_name = Company.objects.filter(client_id=self.owner)[0].name
        return_string = "%s [ %s ] called %s at %s and it took %s seconds" % (self.source, client_name, self.destination, self.start, self.duration)


        return return_string





