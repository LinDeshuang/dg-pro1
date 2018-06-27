import re

from django.test import TestCase

# Create your tests here.
s = 'hello!, **xyz**!'

rere = re.compile(r'\*\*(.*)(y)(.*)\*\*')
res = rere.sub(r'\1H\2H\3',s)
print(res)