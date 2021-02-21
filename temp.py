import re
n =[]
n = [m.start() for m in re.finditer('\.', '1.2_2.3_4.5_')]
print(n)