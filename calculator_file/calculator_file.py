#!/usr/bin/env python3

import sys

if len(sys.argv) != 7:
    print("Usage: %s -c config.cfg -d user.csv -o salary.csv"%sys.argv[0])
# python3 calculator_file.py -c cal.cfg -d user.csv -o salary.csv
    exit()

args = sys.argv[1:]

class Config(object):
    def __init__(self,args):
        self.conf = {}
        self.filename = args[args.index('-c') + 1]

    def get_conf(self):
        with open(self.filename,'r') as f:
            for lines in f.readlines():
                key,value = lines.split('=')
                key = key.strip()
                value = value.strip()
                self.conf[key] = value
        print(self.conf)
        return self.conf
                    
conf = Config(args)
conf.get_conf()
                

#stuff[person_id] = [salary, insurance, tax, salary_after]
#stuff = {}
#for person in persons:
#    try:
#        person_id,salary = person.split(':')
#        stuff[int(person_id)] = [int(salary)]
#    except ValueError:
#        print("Parameter Error")
#
##print(stuff)
#
#def salary_cal(person_id):
#    salary = stuff[person_id][0]
#    insurance = salary * 0.08 + salary * 0.02 + salary * 0.005 + salary * 0.06
#    stuff[person_id].append(format(insurance,'.2f'))
#    tax_count = salary - insurance - 3500
#    if tax_count <= 0:
#        tax = 0
#    elif tax_count <= 1500:
#        tax = tax_count * 0.03 - 0
#    elif tax_count <= 4500:
#        tax = tax_count * 0.1 - 105
#    elif tax_count <= 9000:
#        tax = tax_count * 0.2 - 555
#    elif tax_count <= 35000: 
#        tax = tax_count * 0.25 - 1005
#    elif tax_count <= 55000:
#        tax = tax_count * 0.3 - 2755
#    elif tax_count <= 80000:
#        tax = tax_count * 0.35 - 5505
#    else:
#        tax = tax_count * 0.45 - 13505
#    stuff[person_id].append(format(tax, ".2f"))
#    stuff[person_id].append(format(salary - insurance - tax, '.2f'))
#    print("%s:%s"%(person_id,stuff[person_id][3]))
#
#if __name__ == '__main__':
#    for person_id in stuff.keys():
#        salary_cal(person_id)

