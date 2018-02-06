#!/usr/bin/env python3

import sys,os
from multiprocessing import Process, Pool, Queue
queue1 = Queue()
queue2 = Queue()

if len(sys.argv) != 7:
    print("Usage: %s -c config.cfg -d user.csv -o salary.csv"%sys.argv[0])
    # python3 calculator_file.py -c cal.cfg -d user.csv -o salary.csv
    exit()

args = sys.argv[1:]
configfile = args[args.index('-c') + 1]
userfile = args[args.index('-d') + 1]
salaryfile = args[args.index('-o') + 1]
if not os.path.exists(configfile) or not os.path.exists(userfile):
   print('Can not find configfile or userfile, Please check again!')

#print('configfile: %s , userfile: %s , salaryfile: %s '%(configfile,userfile,salaryfile))

class Config(object):
    def __init__(self,configfile):
        self.conf = {}
        self.filename = configfile

    def get_conf(self, conf_key = 0):
        with open(self.filename,'r') as f:
            for lines in f.readlines():
                key,value = lines.split('=')
                key = key.strip()
                value = value.strip()
                try:
                    self.conf[key] = float(value)
                except ValueError:
                    self.conf[key] = value
#        print(self.conf)
       # print(conf_key)
        if conf_key == 0:
            return self.conf
        else: 
            return self.conf.get(conf_key)

class UserData(object):
    def __init__(self, userfile):
        self.user = {}
        self.userfile = userfile
    def get_user(self,user_id = 0):
        with open(self.userfile,'r') as f:
            for line in f.readlines():
                try:
                    user_id,salary_total = line.split(',') 
                    user_id = int(user_id.strip())
                    salary_total = int(salary_total.strip())
                    self.user[user_id] = {'salary_total': salary_total}
                except:
                    print('Issue found when processing userfile, please check!')
                    sys.exit(-1)
        queue1.put(self.user)
        if user_id == 0:
            return self.user[user_id]
        else:
            return self.user

    def calculator(self,conf):
        #print(conf['JiShuL'])
        self.user = queue1.get()
        for user_id in self.user.keys():
            s = int(self.user[user_id]['salary_total'])     
            if s < conf['JiShuL']:
               s_count = conf['JiShuL']
            elif s > conf['JiShuH']:
               s_count = conf['JiShuH']
            else:
               s_count = s
            insurance = s_count * conf['YangLao'] + s_count * conf['YiLiao'] + s_count * conf['ShiYe'] + s_count * conf['GongShang'] + s_count * conf['ShengYu'] + s_count * conf['GongJiJin']
            tax_count = s - insurance - 3500
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
            salary_final = s - insurance - tax
            self.user[user_id]['insurance'] = insurance
            self.user[user_id]['tax'] = tax
            self.user[user_id]['salary_final'] = salary_final
        queue2.put(self.user)            
#            print(self.user[user_id])   
    def dumptofile(self,salaryfile):    
        self.user = queue2.get()          
        with open(salaryfile,'w') as f:
            for user_id in self.user.keys():
                u = self.user[user_id]
                u_list = []
                u_list.append(str(user_id))
                u_list.append(str(u['salary_total']))
                u_list.append(format(u['insurance'],'.2f')) 
                u_list.append(format(u['tax'],'.2f'))
                u_list.append(format(u['salary_final'],'.2f'))
                line = ','.join(u_list)
                line = line + '\n'
                f.write(line)
    def run_calculator(self,conf,salaryfile):
        pool = Pool(processes=3)
        Process(target=self.get_user).start()
        pool.apply(self.calculator,(conf,))
        #Process(target=self.calculator,args=(conf,)).start()
        Process(target=self.dumptofile,args=(salaryfile,)).start() 
        
  
if __name__ == '__main__':
    conf = Config(configfile)
    config = conf.get_conf()
    user = UserData(userfile)
    user.run_calculator(config,salaryfile)
                
#conf = Config(configfile)
#config = conf.get_conf()
#user = UserData(userfile)
#user.get_user(101)
#user.calculator(config)             
#print(config)
#user.dumptofile(salaryfile)

