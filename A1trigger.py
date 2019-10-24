import pandas as pd
import threading
from datetime import timedelta,datetime,date, timezone
import pytz
import os
from A1basefunctions import *


df = pd.read_csv("A1login",sep=",",index_col=False)
df=df.astype(str)
#save_login(apikey,apisecret,requesttoken)
#df.['apikey'].iloc[-1]
#df.['secretkey'].iloc[-1]
#df.['requesttoken'].iloc[-1]
#df.['backtestdate'].iloc[-1]
#df.['liveorbacktest'].iloc[-1]
#df.['trendsymbol'].iloc[-1]
#df.['tradesymbol'].iloc[-1]
#df.['capitalpercentage'].iloc[-1]

kite_setlogin(df['apikey'].iloc[-1],df['secretkey'].iloc[-1],df['requesttoken'].iloc[-1])

def live_trading():
	global datapull_error
	datapull_error=0
	tz = pytz.timezone('Asia/Kolkata')
	today_date = datetime.now().astimezone(tz)
	
	print("\n"+str(get_enddate('5minute').to_string(index=False)), end = "|")
	#start_fortrading()
	start_foroptiontrading()
	
def run_every_x_Sec_call():
	threading.Timer(120, run_every_x_Sec_call).start()
	tz1 = pytz.timezone('Asia/Kolkata')
	today_date1 = datetime.now().astimezone(tz1)
	emailsent=0
	if emailsent==0 and float(str(today_date1.strftime('%H%M')))>1540 and float(str(today_date1.strftime('%H%M')))<1700:
		#os.system('shutdown /p /f')
		
		'''
		s = smtplib.SMTP('smtp.gmail.com', 587) 
		s.starttls() 
		s.login("ramu772@gmail.com", "zaq12wsxc") 
		SUBJECT="xMarketposition"
		body="BUY/SELL call made at: "+str(message_body_text)
		message = 'Subject: {}\n\n{}'.format(SUBJECT, body)
		
		s.sendmail("ramu772@gmail.com", "ramu772@gmail.com", message) 
		s.quit() 
		'''
		emailsent=1
		pass
	else:
		pass
	if check_internet():
		set_startenddates()
		live_trading()
	else:
		tz = pytz.timezone('Asia/Kolkata')
		today_date = datetime.now().astimezone(tz)
		print(str(today_date.strftime('%H%M'))+"--No internet", end = '')
	
global today_date
global noofdays_backtest_start
global backtest_start_date
noofdays_backtest_start=0
print("----------------")
print(str(df['backtestdate'].iloc[-1]))
backtest_start_date_yyyy_mm_dd=str(df['backtestdate'].iloc[-1])
tradelive=float(df['liveorbacktest'].iloc[-1])
#for live trades make both valriables null/0
if backtest_start_date_yyyy_mm_dd!="":
	date1=datetime.strptime(backtest_start_date_yyyy_mm_dd[0:10], '%Y-%m-%d')
	tz = pytz.timezone('Asia/Kolkata')
	today_date1 = datetime.now().astimezone(tz)
	date2=datetime.strptime(today_date1.strftime('%Y-%m-%d'), '%Y-%m-%d')
	noofdays_backtest_start=(date2-date1).days
	
if str(tradelive)=="1":
	
	noofdays_backtest_start=0

kite=kite_connect()
col_names =  ['live','close','30B','30Hi','60B','60Hi','4hB','4hHi','dB','dHi','15B','15Hi']
my_df  = pd.DataFrame(columns = col_names)
my_df.to_csv('A1Final',sep=",", index=False, header=True)
if tradelive==1:	
	if 1:
		
		for file in os.scandir(os.getcwd()):
			if file.name.endswith(".txt"):
				os.unlink(file.path)
		'''
		if os.path.isfile("trendlive.txt"):
			os.remove("trendlive.txt")
		'''
	run_every_x_Sec_call()
else:
	if 1:
		print("back testing started--")
		for file in os.scandir(os.getcwd()):
			if file.name.endswith(".txt"):
				os.unlink(file.path)
		
	for nod in range(noofdays_backtest_start,-1,-1):
		if nod==-1:
			print("--last day f loop--",end="")
			set_startenddates()
			run_every_x_Sec_call()
		else:
			tz = pytz.timezone('Asia/Kolkata')
			livetime_var = datetime.now().astimezone(tz)
			IST_timex=str(livetime_var.strftime('%H'))
			today_date = datetime.now().astimezone(tz)- timedelta(nod)
			
			holidayslist = {'2018-01-26','2018-02-13','2018-03-02','2018-03-29','2018-03-30','2018-05-01','2018-08-15','2018-08-22','2018-09-13','2018-09-20','2018-10-02','2018-10-18','2018-11-07','2018-11-08','2018-11-23','2018-12-25','2019-03-04','2019-03-21','2019-04-17','2019-04-19','2019-04-29','2019-05-01','2019-06-05','2019-08-12','2019-08-15','2019-09-02','2019-09-10','2019-10-02','2019-10-08','2019-10-28','2019-11-12','2019-12-25'}
			if today_date.strftime("%A")=="Saturday" or  today_date.strftime("%A")=="Sunday" or (today_date.strftime('%Y-%m-%d') in holidayslist):
				pass
			else:
				
				for h in range(10,16):
					if nod<=0 and float(IST_timex)<=h:
						print("--last day of loop--Live",end="")
						set_startenddates()
						run_every_x_Sec_call()
						break
						
					
					for m in range (1,60,2):
						if h==9:
							if m<30:
								#print m
								pass
							else:
								
								tz = pytz.timezone('Asia/Kolkata')
								today_date = datetime.now().astimezone(tz)- timedelta(nod)
								today_time=today_date.strftime('%Y-%m-%d')+" "+str("%02d" % h)+":"+str("%02d" % m)+":10"
								IST_time=datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
								
								col_names =  ['timeframe','start', 'end']
								mydates  = pd.DataFrame(columns = col_names)
								
								if today_date.strftime("%A")=="Saturday" or  today_date.strftime("%A")=="Sunday" or (today_date.strftime("%A")=="Monday" and float(h)<12):
									mydates.loc[len(mydates)] = ['1minute', str((today_date - timedelta(5)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['3minute', str((today_date - timedelta(6)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['5minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['15minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['30minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['60minute', str((today_date - timedelta(100)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['day', str((today_date - timedelta(202)).strftime('%Y-%m-%d')), IST_time]
								else:
									mydates.loc[len(mydates)] = ['1minute', str((today_date - timedelta(3)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['3minute', str((today_date - timedelta(5)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['5minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['15minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['30minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['60minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['day', str((today_date - timedelta(200)).strftime('%Y-%m-%d')), IST_time]
								save_dates(mydates)
								live_trading()
						elif h==15:
							if m>30:
								pass
							else:
								tz = pytz.timezone('Asia/Kolkata')
								today_date = datetime.now().astimezone(tz)- timedelta(nod)
								today_time=today_date.strftime('%Y-%m-%d')+" "+str("%02d" % h)+":"+str("%02d" % m)+":00"
								IST_time=datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
								
								col_names =  ['timeframe','start', 'end']
								mydates  = pd.DataFrame(columns = col_names)
								
								if today_date.strftime("%A")=="Saturday" or  today_date.strftime("%A")=="Sunday" or (today_date.strftime("%A")=="Monday" and float(h)<12):
									mydates.loc[len(mydates)] = ['1minute', str((today_date - timedelta(5)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['3minute', str((today_date - timedelta(6)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['5minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['15minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['30minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['60minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['day', str((today_date - timedelta(202)).strftime('%Y-%m-%d')), IST_time]
								else:
									mydates.loc[len(mydates)] = ['1minute', str((today_date - timedelta(3)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['3minute', str((today_date - timedelta(5)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['5minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['15minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['30minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['60minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
									mydates.loc[len(mydates)] = ['day', str((today_date - timedelta(200)).strftime('%Y-%m-%d')), IST_time]
								save_dates(mydates)
								live_trading()
						else:
							tz = pytz.timezone('Asia/Kolkata')
							today_date = datetime.now().astimezone(tz)- timedelta(nod)
							today_time=today_date.strftime('%Y-%m-%d')+" "+str("%02d" % h)+":"+str("%02d" % m)+":00"
							IST_time=datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
							
							col_names =  ['timeframe','start', 'end']
							mydates  = pd.DataFrame(columns = col_names)
							
							if today_date.strftime("%A")=="Saturday" or  today_date.strftime("%A")=="Sunday" or (today_date.strftime("%A")=="Monday" and float(h)<12):
								mydates.loc[len(mydates)] = ['1minute', str((today_date - timedelta(5)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['3minute', str((today_date - timedelta(6)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['5minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['15minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['30minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['60minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['day', str((today_date - timedelta(202)).strftime('%Y-%m-%d')), IST_time]
							else:
								mydates.loc[len(mydates)] = ['1minute', str((today_date - timedelta(3)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['3minute', str((today_date - timedelta(5)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['5minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['15minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['30minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['60minute', str((today_date - timedelta(50)).strftime('%Y-%m-%d')), IST_time]
								mydates.loc[len(mydates)] = ['day', str((today_date - timedelta(200)).strftime('%Y-%m-%d')), IST_time]
							save_dates(mydates)
							live_trading()

