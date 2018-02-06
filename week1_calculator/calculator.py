#!/usr/bin/env python3

import sys
if len(sys.argv) != 2:
    print("Usage: %s [500]"%sys.argv[0])
    exit()

try:
    salary = int(sys.argv[1])
except ValueError:
    print("Parameter Error")

def salary_cal(salary,insurance):
    tax_count = salary - insurance - 3500
    if tax_count <= 0:
        tax = 0
    elif tax_count <= 1500:
        tax = tax_count * 0.03 - 0
    elif tax_count <= 4500:
        tax = tax_count * 0.1 - 105
    elif tax_count <= 9000:
        tax = tax_count * 0.2 - 555
    elif tax_count <= 35000: 
        tax = tax_count * 0.25 - 1005
    elif tax_count <= 55000:
        tax = tax_count * 0.3 - 2755
    elif tax_count <= 80000:
        tax = tax_count * 0.35 - 5505
    else:
        tax = tax_count * 0.45 - 13505
    tax = format(tax, ".2f")
    return tax

insurance = 0
tax = salary_cal(salary,insurance)
print(tax) 
