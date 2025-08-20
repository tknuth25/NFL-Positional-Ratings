# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:45:57 2022

@author: Thompson.Knuth
"""

import os
import numpy as np
import pandas as pd
from datetime import date
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import re
import statsmodels.formula.api as smf
import seaborn as sns

pd.set_option("max_colwidth", 200)
pd.set_option("display.precision", 1)
pd.set_option("display.max_columns", 500)
pd.set_option("display.float_format", "{:,.10}".format)

#%%
#Getting team records

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

total_df = []
    
for i in range(1922,2025):
    page = "https://www.pro-football-reference.com/years/" + str(i)
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    
    column_headers = pageSoup.find_all('tr')[0]
    column_headers = [j.getText() for j in column_headers.find_all('th')]
    
    rows = pageSoup.find_all('tr')[1:]
    team_stats = []
    for j in range(len(rows)):
        team_stats.append([col.getText() for col in rows[j].find_all('td')])
    data = pd.DataFrame(team_stats, columns=[column_headers[1:]]).reset_index()

    if len(data.columns)==12:
        data.columns = ['Index','W','L','W-L%','PF','PA','PD','MoV','SoS','SRS','OSRS','DSRS']
        a_data = data.loc[(~data['W'].astype(str).str.contains(' '))&~data['W'].isnull()]
    else:
        data.columns = ['Index','W','L','T','W-L%','PF','PA','PD','MoV','SoS','SRS','OSRS','DSRS']
        a_data = data.loc[(~data['W'].astype(str).str.contains(' '))&~data['W'].isnull()]
   
    #getting teams
    column_headers_1 = pageSoup.findAll('tr')[0]
    column_headers_1 = [j.getText() for j in column_headers_1.findAll('th')]
    column_headers_1 = column_headers_1[0]
    rows_1 = pageSoup.findAll('tr')[1:]
    team = []
    for j in range(len(rows_1)):
        team.append([col.getText() for col in rows_1[j].findAll('a')])
    data_name = pd.DataFrame(team, columns=[column_headers_1]).reset_index()
    data_name.columns=['Index','Tm']
    a_data_name = data_name.loc[~data_name['Tm'].isnull()]
    
    season_df = a_data_name.merge(a_data,how='left',on='Index')
    del season_df['Index']
    season_df['Year']=i
    total_df.append(season_df)
    print(f"{i} team performance data loaded.")
    time.sleep(5)
    
performance_df = pd.concat(total_df,ignore_index=True)

#%%
# Loading in offensive and defensive rating, concatenating

offensive_ratings = pd.read_csv(r'C:\Users\thompson.knuth\Desktop\Webscraping Practice\NFL\NFL Offensive Ratings Data Build (2000s) (TK).csv')
del offensive_ratings['Unnamed: 0']

defensive_ratings = pd.read_csv(r'C:\Users\thompson.knuth\Desktop\Webscraping Practice\NFL\NFL Defensive Ratings Data Build (2000s) (TK).csv')
del defensive_ratings['Unnamed: 0']

df_list = [offensive_ratings,defensive_ratings]

all_ratings = pd.concat(df_list,ignore_index=True)

#%%
# Team Name lookup for ratings database
unique_abbrev = list(all_ratings['Tm'].unique())
unique_abbrev.append('OTI')

team_names = []
Year = []
Abbrev = []
for i in range(1932,2025):
    for j in unique_abbrev:
      page = 'https://www.pro-football-reference.com/teams/' + str(j).lower() + '/' + str(i)+'.htm'
      try:
          pageTree = requests.get(page)
          pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
          y = list(str(pageSoup).split("<title>"))
          y1 = y[1].split('<')
          y2 = y1[0].replace(' ','')
          y3 = y2[4:].split(',')
          y4 = y3[0].split('Rosters')
          y5 = y4[0]
          team_name = re.sub(r"(?<=\w)([A-Z])", r" \1", y5)
          team_names.append(team_name)
          Year.append(i)
          Abbrev.append(j)
      except:
          pass
    print(f"{i} abbreviations added.")

abbrev_df = pd.DataFrame({'Year':Year,'Team':team_names,'Tm':Abbrev})

a_abbrev_df = abbrev_df.loc[abbrev_df['Team']!='Not Found(404error)|Pro-Football-Reference.com'].copy()
a_abbrev_df['Team'] = np.where(a_abbrev_df['Team']=='San Francisco49ers','San Francisco 49ers',a_abbrev_df['Team'])

a_all_ratings = all_ratings.merge(a_abbrev_df,how='left',on=['Tm','Year'])

test = a_all_ratings.loc[a_all_ratings['Team'].isna()].copy()
test_1 = test['Tm'].unique()

# Manual corrections

manual_dict = {'LVR':'Las Vegas Raiders','PRT':'Portsmouth Spartans','BAL':'Baltimore Ravens','STL':'St. Louis Rams',
               'OAK':'Oakland Raiders','HOU':'Houston Texans','IND':'Indianapolis Colts','PHO':'Phoenix Cardinals',
               'ARI':'Arizona Cardinals','TEN':'Tennessee Titans','LAR':'Los Angeles Rams','LAC':'Los Angeles Chargers',
               'CIN':'Cincinnati Bengals'}

a_all_ratings['Team'] = a_all_ratings.apply(lambda x: manual_dict.get(x['Tm']) if manual_dict.get(x['Tm']) is not None else x["Team"], axis=1)

a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='BOS')&(a_all_ratings['Year']==1932),'Boston Braves',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='BOS')&(a_all_ratings['Year']<=1936)&(a_all_ratings['Year']>=1933),'Boston Redskins',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='BOS')&(a_all_ratings['Year']<=1936)&(a_all_ratings['Year']>=1933),'Boston Redskins',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='BOS')&(a_all_ratings['Year']>=1960)&(a_all_ratings['Year']<=1970),'Boston Patriots',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='BOS')&(a_all_ratings['Year']>=1946)&(a_all_ratings['Year']<=1948),'Boston Yanks',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='BOS')&(a_all_ratings['Year']==1944),'Boston Yanks',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='BOS')&(a_all_ratings['Year']==1945),'Bos/Bkn Yanks/Tigers',a_all_ratings['Team'])

a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='BAL')&(a_all_ratings['Year']>=1953)&(a_all_ratings['Year']<=1983),'Baltimore Colts',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='CIN')&(a_all_ratings['Year']>=1933)&(a_all_ratings['Year']<=1934),'Cincinnati Reds',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='STL')&(a_all_ratings['Year']>=1946)&(a_all_ratings['Year']<=1994),'Los Angeles Rams',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='HOU')&(a_all_ratings['Year']>=1970)&(a_all_ratings['Year']<=1996),'Houston Oilers',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='TEN')&(a_all_ratings['Year']==1998),'Tennessee Oilers',a_all_ratings['Team'])
a_all_ratings['Team'] = np.where((a_all_ratings['Tm']=='TEN')&(a_all_ratings['Year']==1997),'Tennessee Oilers',a_all_ratings['Team'])

#%%
#Merging team and rating dfs
performance_df = performance_df.rename(columns={'Tm':'Team'})

total_df = a_all_ratings.merge(performance_df,how='left',on=['Team','Year'])

a_total_df = total_df[total_df['Team'].notna()].copy()

a_total_df['Pos'] = a_total_df['Pos'].astype(str).str.upper()
a_total_df['Pos'] = np.where(a_total_df['Pos']=='NAN',np.nan,a_total_df['Pos'])

pos_list = pd.DataFrame(a_total_df['Pos'].unique())

pos_test = a_total_df.loc[a_total_df['Pos']=='S'].copy()
pos_name = pos_test['Player'].unique()

#%%
#Cleaning Positions
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['LDE','RDE','RDE/LDE','LDT/LDE','LDE/RDE','RDE/LOLB','LDE/LDT','RDE/LDT','DE/DT','DL','RE']),'DE',a_total_df['Pos'])
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['DB/FS']),'FS',a_total_df['Pos'])
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['SS/LH','RH/SS','CB/SS']),'SS',a_total_df['Pos'])


a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['FB/HB','FB/LDE','FB/LH','FB/RB','FB/RDH','FB/RH','FB/RHB','LLB/FB','TE/FB']),'FB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['RDT','LDT','NT','LDT/RDT','RDT/LDT','NT/DT','DT/NT','RDE/NT',
                                                     'NT/RDT','RDT/NT','NT/LDT','LDE/NT']),'DT',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['FS/RCB','LCB/RCB','RCB/LCB','RCB/CB','RCB/DB','LCB','RCB','SS/LCB','RCB/WR','DB']),'CB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['FS/LH','HB/FB','LHB/RHB','LHB','LH/RH','LH/RDH','LH','RH','LH/FB','LH/QB','RH/RE','RH/DB','RH/LH/FS','RH/FB','RDH/LH',
                                                     'LHB/FB','RHB/LHB','FL/HB','RB/FB','HB/LE','RHB','LDH','RDH']),'HB',a_total_df['Pos'])


a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['SS/RLB']),'SS',a_total_df['Pos'])
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['RCB/LLB']),'LLB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['WR/QB']),'QB',a_total_df['Pos'])
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['WR/WR']),'WR',a_total_df['Pos'])
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['TE/TE']),'TE',a_total_df['Pos'])


a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Darryl Roberts','Avonte Maddox','Rashean Mathis','Brandon Carr','Logan Ryan']),'CB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Xavier McKinney','Kurt Schulz','Cory Hall','Dwight Smith','Devin McCourty',
                                                        'Brent Alexander','James Sanders','Calvin Lowry',
                                                        'Michael Griffin','Erik Harris','C.C. Brown','Reed Doughty',
                                                        'Morgan Burnett','Jordan Babineaux','Earl Thomas','Kyle Dugger','Jabrill Peppers']),'FS',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Ainsley Battles','Nick Ferguson','Mike Adams','Quintin Mikell','Bryan Scott',
                                                        'Craig Dahl','Lamar Campbell','Donte Whitner','Calvin Pryor','Daniel Sorensen',
                                                        'Ashtyn Davis','Amani Hooker','Taylor Rapp']),'SS',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Chris Jones','Cory Redding','John Browning','Junior Bryant',
                                                        'Cletidus Hunt','John Randle','Sheldon Richardson','Nick Williams','Dexter Lawrence',
                                                        'Christian Barmore','Kenny Clark','Maliek Collins','Leonard Williams','Vita Vea']),'DT',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Orpheus Roye','John Copeland','Andre Branch','Mike Wright','Deatrich Wise Jr.']),'DE',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['LLB/RDE','LBODE','LOLB/LLB','LLB/ROLB','LOLB/ROL','LLB/LOLB']),'LOLB',a_total_df['Pos'])
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['RLB/LDE','RLB/ROLB','ROLB/RIL','ROLB/LOL','RLB/LLB','ROLB/LIL']),'ROLB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['LILB/MLB','LILB/RIL','LILB/ROL']),'LILB',a_total_df['Pos'])
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['RILB/RLB','RILB/LIL','RLB/LILB','ILB']),'RILB',a_total_df['Pos'])
a_total_df['Pos'] = np.where(a_total_df['Pos'].isin(['MLB/ROLB','LLB/MLB','MLB/RLB','MLB/LLB','MLB/RILB','MLB/LILB']),'MLB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Barry Minter','Jon Beason',"Dont'a Hightower",'Isaiah Kacyvenski','Paris Lenon']),'MLB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Pisa Tinoisamoa','Carlos Emmons']),'ROLB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Daryl Smith','Paul Worrilow','Jeff Ulbrich','Sean Harris']),'RILB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['A.J. Hawk','Josh Bynes']),'LILB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Rocky Boiman','Jamie Collins','Kevin Hardy','Clint Ingram']),'LOLB',a_total_df['Pos'])

a_total_df['Pos'] = np.where(a_total_df['Player'].isin(['Olabisi Johnson','Troy Brown','Brad Smith']),'WR',a_total_df['Pos'])

#%%

a1_total_df = a_total_df.loc[~a_total_df['Pos'].isin(['BB','B','TB',np.NaN,'P','LS','PR','KR','WB','/','C','FL'])].copy()
a1_total_df['Pos'] = np.where(a1_total_df['Pos']=='HB','RB',a1_total_df['Pos'])
a1_total_df['Pos'] = np.where(a1_total_df['Pos']=='FB','RB',a1_total_df['Pos'])

a1_total_df['Pos'] = np.where(a1_total_df['Pos'].isin(['LILB','LLB','LOLB','MLB','OLB',
                                                       'ROLB','RLB','RILB']),'LB',a1_total_df['Pos'])

a1_total_df['Pos'] = np.where(a1_total_df['Pos'].isin(['FS','SS']),'S',a1_total_df['Pos'])


pos_test_1 = a1_total_df['Pos'].unique()

#%%
#Ranking
def hashValues(t,y,p):
    if t == None:
        t = "None"
    if y == None:
        y = 'None'
    if p== None:
        p='None'
    return hash(t + y + p)  

a1_total_df['ID'] = [hashValues(a1_total_df['Team'].to_list()[i], a1_total_df['Year'].astype(str).to_list()[i],a1_total_df['Pos'].to_list()[i]) for i in range(a1_total_df.shape[0])]

a2_total_df = a1_total_df.sort_values(by=['ID','GS','G','rating_adj_1'],ascending=False)

a2_total_df['pos_rank'] = a2_total_df.groupby(['ID'])['rating_adj_1'].rank(ascending=False,method='first')

# test = a2_total_df.loc[a2_total_df['ID']==-4044935879104010133]

#%%
#subsetting to positions
qb_sub = a2_total_df.loc[a2_total_df['Pos']=='QB'].copy()

rb_sub = a2_total_df.loc[a2_total_df['Pos']=='RB'].copy()

wr_sub = a2_total_df.loc[a2_total_df['Pos']=='WR'].copy()

te_sub = a2_total_df.loc[a2_total_df['Pos']=='TE'].copy()

cb_sub = a2_total_df.loc[a2_total_df['Pos']=='CB'].copy()

s_sub = a2_total_df.loc[a2_total_df['Pos']=='S'].copy()

lb_sub = a2_total_df.loc[a2_total_df['Pos']=='LB'].copy()

de_sub = a2_total_df.loc[a2_total_df['Pos']=='DE'].copy()

dt_sub = a2_total_df.loc[a2_total_df['Pos']=='DT'].copy()

#%%
#Position rank limits
a_qb_sub = qb_sub.loc[qb_sub['pos_rank']<=1].copy()
a_rb_sub = rb_sub.loc[rb_sub['pos_rank']<=2].copy()
a_wr_sub = wr_sub.loc[wr_sub['pos_rank']<=3].copy()
a_te_sub = te_sub.loc[te_sub['pos_rank']<=1].copy()
a_cb_sub = cb_sub.loc[cb_sub['pos_rank']<=3].copy()
a_s_sub = s_sub.loc[s_sub['pos_rank']<=2].copy()
a_lb_sub = lb_sub.loc[lb_sub['pos_rank']<=4].copy()
a_de_sub = de_sub.loc[de_sub['pos_rank']<=2].copy()
a_dt_sub = dt_sub.loc[dt_sub['pos_rank']<=2].copy()

pos_df_list = [a_qb_sub,a_rb_sub,a_wr_sub,a_te_sub,a_cb_sub,a_s_sub,a_lb_sub,a_de_sub,a_dt_sub]

limited_total_df = pd.concat(pos_df_list,ignore_index=True)

limited_total_df['new_rank'] = limited_total_df['Pos']+limited_total_df['pos_rank'].astype(str)

limited_total_df['new_rank'] = limited_total_df['new_rank'].astype(str).str.replace('.0','')

#%%
#Pivot

c_total_df = limited_total_df.pivot(index = ['Team','Year', 'W', 'L', 'T', 'W-L%','PF', 'PA', 'PD', 'MoV', 'SoS', 'SRS', 'OSRS', 'DSRS'],columns = ['new_rank'],values=['Player','rating_adj_1']).reset_index()

d_total_df = c_total_df.loc[c_total_df['Year']>=1999].copy()

#%%
#Column cleaning

def flat_cols(cols, rev_order=False):
    if rev_order:
        cols_new = ['_'.join(col[::-1]) if col[1] else col[0] for col in cols]

    else:
        cols_new = ['_'.join(col) if col[1] else col[0] for col in cols]

    return cols_new

d_total_df.columns = flat_cols(d_total_df.columns)

d_total_df = d_total_df.rename(columns = {'Player_CB1': 'CB1 Name','Player_CB2':'CB2 Name',
                                          'Player_CB3':'CB3 Name','Player_DE1':'DE1 Name',
                                          'Player_DE2':'DE2 Name','Player_DT1':'DT1 Name',
                                          'Player_DT2':'DT2 Name','Player_LB1':'LB1 Name',
                                          'Player_LB2':'LB2 Name','Player_LB3':'LB3 Name',
                                          'Player_LB4':'LB4 Name','Player_QB1':'QB1 Name',
                                          'Player_RB1':'RB1 Name','Player_RB2':'RB2 Name',
                                          'Player_S1':'S1 Name','Player_S2':'S2 Name',
                                          'Player_TE1':'TE1 Name','Player_WR1':'WR1 Name',
                                          'Player_WR2':'WR2 Name','Player_WR3':'WR3 Name'})

d_total_df = d_total_df.rename(columns = {'rating_adj_1_CB1': 'CB1 Rating','rating_adj_1_CB2':'CB2 Rating',
                                          'rating_adj_1_CB3':'CB3 Rating','rating_adj_1_DE1':'DE1 Rating',
                                          'rating_adj_1_DE2':'DE2 Rating','rating_adj_1_DT1':'DT1 Rating',
                                          'rating_adj_1_DT2':'DT2 Rating','rating_adj_1_LB1':'LB1 Rating',
                                          'rating_adj_1_LB2':'LB2 Rating','rating_adj_1_LB3':'LB3 Rating',
                                          'rating_adj_1_LB4':'LB4 Rating','rating_adj_1_QB1':'QB1 Rating',
                                          'rating_adj_1_RB1':'RB1 Rating','rating_adj_1_RB2':'RB2 Rating',
                                          'rating_adj_1_S1':'S1 Rating','rating_adj_1_S2':'S2 Rating',
                                          'rating_adj_1_TE1':'TE1 Rating','rating_adj_1_WR1':'WR1 Rating',
                                          'rating_adj_1_WR2':'WR2 Rating','rating_adj_1_WR3':'WR3 Rating'})

d_total_df = d_total_df[['Team', 'Year', 'W', 'L', 'T', 'W-L%', 'PF', 'PA', 'PD', 'MoV', 'SoS',
                         'SRS', 'OSRS', 'DSRS','QB1 Name','QB1 Rating','RB1 Name','RB1 Rating',
                         'RB2 Name','RB2 Rating','WR1 Name','WR1 Rating','WR2 Name','WR2 Rating',
                         'WR3 Name','WR3 Rating','TE1 Name','TE1 Rating','DE1 Name','DE1 Rating',
                         'DE2 Name','DE2 Rating','DT1 Name','DT1 Rating','DT2 Name','DT2 Rating',
                         'LB1 Name','LB1 Rating','LB2 Name','LB2 Rating','LB3 Name','LB3 Rating',
                         'LB4 Name','LB4 Rating','CB1 Name','CB1 Rating','CB2 Name','CB2 Rating',
                         'CB3 Name','CB3 Rating','S1 Name','S1 Rating','S2 Name','S2 Rating']].copy()

# d_total_df.to_csv(r'C:\Users\thompson.knuth\Desktop\Webscraping Practice\NFL\NFL Final Databuild (1999-Present) (TK).csv')
