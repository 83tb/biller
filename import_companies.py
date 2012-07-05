#!/usr/bin/env python
# -- coding: utf-8 --


# this is very custom script to parse a txt files with companies and their ids, and also numbers used byu them



from django.core.management import setup_environ
import settings
setup_environ(settings)


#from django.contrib.auth.models import User
from biller.engine.models import *


#company = Company.objects.create()
#company.save()

#number = Number.objects.create()
#number.save()

import sys
# open file to read
f = file('companies.txt', 'r')
from django.contrib.auth.models import User


for line in f:
    number = line[0:9]
    client_id = line[10:13]
    name = line[14:46]

    company = Company.objects.filter(client_id = client_id)

    # if there is no company in the db
    if len(company) == 0:
        userid = User.objects.all()[0]        
        company = Company.objects.create(name=name,client_id=client_id,userid=userid)
        company.save()

    # if there's no such number in the db
    number_base = Number.objects.filter(full_number=number)
    if len(number_base) == 0:
        number_base = Number.objects.create(full_number=number,client_id=client_id)


    print number, client_id, name


