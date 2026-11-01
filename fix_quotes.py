with open('generate_report_diagrams.py','r',encoding='utf-8') as f:
    c = f.read()
for s in ["'2.5'","'1.5'","'2.8'","'2.2'","'1.4'","'1.2'","'3.0'","'1.6'"]:
    c = c.replace(s, s.strip("'"))
with open('generate_report_diagrams.py','w',encoding='utf-8') as f:
    f.write(c)
print('Fixed quoted numbers')

