import re
from macpath import join

a = "13111111111"
b = "13122222222"
c = "13133333333"
d = "13155555555,13266666666"
e = "13377777777,13688888888,13699999999"
t = "021-88888888"

s = (a,b,c,d,e,t)

list_mobile = []
for i in s:

    tt = re.findall(r"1\d{10}",i)
    # print(tt)
    if tt:
        for oo in tt:
            mobile = re.split(r",",oo)

            # print(mobile)
            for num in mobile:
                # print(111111)
            # aa = ','.join(mobile)
                print(num)
                list_mobile.append(num)

print(list_mobile)