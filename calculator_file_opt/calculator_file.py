#!/usr/bin/env python3

import sys,os,getopt, configparser
from datetime import datetime
from multiprocessing import Process, Pool, Queue
queue1 = Queue()
queue2 = Queue()

def usage():
    print("Usage: %s -C cityname -c configfile -d userdata -o resultdata"%sys.argv[0])
    sys.exit()
    
# python3 calculator_file.py -C CHENGDU -c cal.cfg -d user.csv -o salary.csv

try:
    optlist,arg = getopt.getopt(sys.argv[1:],'C:c:d:o:h',['help'])
except getopt.GetoptError as err:
    print(str(err))
    usage()

parameter_count = []
for o,a in optlist:
#    print(optlist)
    if o in ['-h','--help']:
        usage()
    elif o == '-C':
        cityname = a
    elif o == '-c':
        configfile = a
        if not os.path.exists(configfile):
            print('Can not find config file.')
            sys.exit()
        parameter_count.append('configfile')
    elif o == '-d':
        userfile = a
        if not os.path.exists(userfile):
            print('Can not find user file')
            sys.exit()
        parameter_count.append('userfile')
    elif o == '-o':
        salaryfile = a
        parameter_count.append('salaryfile')
    else:
        assert False, 'Unhandled options'

if 'configfile' not in parameter_count:
    print('Can not find Config file!')
    usage()
elif 'userfile' not in parameter_count:
    print('Can not find user file!')
    usage()
elif 'salaryfile' not in parameter_count:
    print('Can not find result data!')
    usage()


#configfile = args[args.index('-c') + 1]
#userfile = args[args.index('-d') + 1]
#salaryfile = args[args.index('-o') + 1]
#if not os.path.exists(configfile) or not os.path.exists(userfile):
#   print('Can not find configfile or userfile, Please check again!')

#print('configfile: %s , userfile: %s , salaryfile: %s '%(configfile,userfile,salaryfile))

class Config(object):
    def __init__(self,configfile):
        self.conf = {}
        self.filename = configfile

    def get_conf(self, cityname = 'DEFAULT', conf_key = 0):
        config = configparser.ConfigParser()
        config.read(self.filename)
        city_check = 0
        if cityname != 'DEFAULT':
            for cname in config.sections():
                if cityname.lower() == cname.lower():
                    cityname = cname
                    city_check = 1
            if city_check == 0:
                print('Can not find relate city!')
                usage()
        for key in config[cityname]:
            try:
                self.conf[key] = float(config[cityname][key])
            except:
                self.conf[key] = config[cityname][key]
#        print(self.conf)
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
        #print(conf)
        for user_id in self.user.keys():
            s = int(self.user[user_id]['salary_total'])     
            if s < conf['jishul']:
               s_count = conf['jishul']
            elif s > conf['jishuh']:
               s_count = conf['jishuh']
            else:
               s_count = s
            insurance = s_count * conf['yanglao'] + s_count * conf['yiliao'] + s_count * conf['shiye'] + s_count * conf['gongshang'] + s_count * conf['shengyu'] + s_count * conf['gongjijin']
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
            exc_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M%S')[:-2]
            self.user[user_id]['date'] = exc_date
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
                u_list.append(str(u['date']))
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
    config = conf.get_conf(cityname)
    user = UserData(userfile)
    user.run_calculator(config,salaryfile)
                
#conf = Config(configfile)
#config = conf.get_conf()
#user = UserData(userfile)
#user.get_user(101)
#user.calculator(config)             
#print(config)
#user.dumptofile(salaryfile)

