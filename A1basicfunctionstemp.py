def create_coreengine_columns(df):
	
	df=GET_HIGHLOW_CHECK(df,20,3)
	df=GET_LASTEND_LIVE(df)
	df=MACD_SIGN(df,"ema",3,8,4,"LASTCLOSE")
	df=MACD_SIGN(df,"ema",7,16,4,"LASTCLOSE")
	df=get_lastbar_health(df,"LAST")
	df=ma_lastclose_check(df,5)
	df=get_livebarpercentage(df)
	df=get_bodysize(df)
	df=get_bodykper(df)
	df=get_bodyratio(df)
	
	df=lastbar_breakout_value012(df)
	df=get_max(df,'highcheck','ms_7164','highcheckmax')
	df=get_min(df,'lowcheck','ms_7164','lowcheckmin')
	df=get_max(df,'breakout','ms_7164','breakoutmax')
	df=get_max(df,'barhealth','ms_7164','barhealthmax')
	df=ma_rateofchange(df,20)
	df=ma_rateofchange(df,7)
	df=ma_rateofchange(df,3)
	
	
	df=get_gap_analysis(df)
	df=get_carryonliveorlastbar(df)
	df=get_first(df,"lastendfirst")
	df=get_first(df,"barhealthfirst")
	df=get_first(df,"highcheckfirst")
	df=get_first(df,"check_ma_5first")
	df=get_ms_strength(df)
	df=get_kcross(df)
	
	
	#ordersystem - hearth of the system
	
	df['buyconfirm']=0
	
	#forbuy
	df['bigtrend']=0
		
	df['bigtrend']=np.NaN
	#failed msloop but new breakout inside a failed loop. # failed bcz of lastend/bar health, highcheck>4
	#df.loc[ (df['ms_7164_counter'].astype(float)>0) & (df['highcheckfirst'].astype(float)>=3.9) & (df['highcheckfirst'].astype(float)<=4.7) & (df['lowcheck'].astype(float)<=4.2) & (df['barhealthfirst'].astype(float)>=1) & (df['breakout'].astype(float)==1) & (df['check_ma_5'].astype(float)==1),['bigtrend']]=4
	df.loc[ ((df['ms_7164_counter'].astype(float)>0) & ((df['highcheckfirst'].astype(float)>=3.9) | (df['lastendfirst'].astype(float)!=2) | (df['barhealthfirst'].astype(float)!=1)) & (df['highcheck'].shift(1).astype(float)<=3.5) & (df['lastend'].astype(float)==2) & (df['barhealth'].astype(float)==1)) & (df['check_ma_5'].astype(float)==1),['bigtrend']]=3
	df.loc[ ((df['ms_7164_counter'].astype(float)>0) & (df['closecheck'].astype(float)<4.7) & (df['closecheck'].astype(float)>4.1) & (df['highcheckmax'].shift(1).astype(float)>4.1) & (df['highcheckmax'].shift(2).astype(float)<4) & (df['lastendfirst'].astype(float)==2) & (df['barhealthself'].astype(float)==1)),['bigtrend']]=2
	df.loc[ ((df['ms_7164_counter'].astype(float)>0) & (df['highcheckfirst'].astype(float)<=3.9) & (df['lastendfirst'].astype(float)==2) & (df['barhealthfirst'].astype(float)>=1)),['bigtrend']]=1
	df.loc[ (df['highcheckmax'].astype(float)>=6) | (df['highcheck'].astype(float)>=6),['bigtrend']]=-1
	#df.loc[ (df['ms_7164_counter'].astype(float)<0) & (df['lowcheckmin'].astype(float)<=2),['bigtrend']]=-3
	df.loc[ (df['ms_7164_counter'].astype(float)<0) & (df['barhealthfirst'].astype(float)==-1) & (df['lowcheckmin'].shift(1).astype(float)>2),['bigtrend']]=-2
	#df.loc[ ((df['highcheckmax'].astype(float)>=5.6) & (df['closecheck'].astype(float)<4) & (df['closecheck'].shift(1).astype(float)<4)),['bigtrend']]=-2
	df.loc[ (df['ms_7164_counter'].astype(float)<-1) & (df['closecheck'].astype(float)<1.8) & (df['closecheck'].shift(1).astype(float)<1.8),['bigtrend']]=-4
	#sell on -1,-2,-3,-4 not on -5.	
	
	df['bigtrend']=df['bigtrend'].fillna(method='ffill')
	
	df['buyconfirm']=df['bigtrend']
	df['lastxy']=np.NaN
	df.loc[(df['buyconfirm'].astype(float)>0) & (df['buyconfirm'].shift(1).astype(float)<=0),['lastxy']]=1
	df.loc[(df['buyconfirm'].astype(float)<0),['lastxy']]=-1
	df['lastxy']=df['lastxy'].fillna(method='ffill')
	
	
	var2='lastxy'
	v = df[var2].dropna()
	grouper = (v!=v.shift()).cumsum()
	x=df.groupby(grouper)[var2].cumsum()
	x=x.rename('lastbuyorexit')
	df = df.join(x)
	
	
	var1='lastxy'
	var2='date'
	df['lastgroup'] = (df[var1].diff(1) != 0).astype('int').cumsum()
	x = df.groupby('lastgroup')['date'].first()
	x=x.rename('lastentry-time')
	df = df.join(x,on='lastgroup')
	
	x = df.groupby('lastgroup')['open'].first()
	x=x.rename('lastentry-price')
	df = df.join(x,on='lastgroup')
	
	df.loc[df['lastxy']<0,['lastentry-price']]=0
	x = df.groupby('lastgroup')['low'].min()
	x=x.rename('lastentry-low')
	df = df.join(x,on='lastgroup')
	df.loc[df['lastxy']<0,['lastentry-low']]=0
	
	df['profit']=round(((df['high']-df['lastentry-price'])/df['lastentry-price'])*100,2)
	df.loc[df['lastbuyorexit']<0,['profit']]=0
	
	df['var-target']=round(((df['k_6']-df['close'])/df['close'])*100,2)
	df['var-low']=round(((df['close']-df['k_2'])/df['close'])*100,2)
	
	return df
