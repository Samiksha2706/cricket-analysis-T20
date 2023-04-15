import pandas as pd
import json

#transforming dataset "match results"
with open('t20_wc_match_results.json') as f:
    #data will be displayed in json format
    data = json.load(f)
#converting json format to csv format    
df_match= pd.DataFrame(data[0]['matchSummary'])  
df_match.head()
df_match.shape
# in this table we have 45 rows and 7 columns

#now, will refer scorecard column as unique identification number, so we can
# connect this tables to other tables
#here scorecard = match_id = primary key
df_match.rename({'scorecard':'match_id'},axis=1,inplace=True)
df_match.head() 


# modification (creating dictionary)
match_ids_dict={}
for index, row in df_match.iterrows():
    #here, we are reversing the order
    key1 = row['team1']+'Vs'+row['team2']
    key2 = row['team2']+'Vs'+row['team1']
    
    match_ids_dict[key1] = row["match_id"]
    match_ids_dict[key2] = row["match_id"]
match_ids_dict    
    #now we want to bring this match_id column on df_battimg database amd therefore we will create new column in df_batting dataframe
   
'''{	
	"Namibia Vs Sri Lanka":"T201 # 1823",
     "Sri Lanka Vs Namibia": "T201# 1823",
     "U.A.E. Vs Netherlands":"T201 # 1825",
     "Netherlands Vs U.A.E":"T201 # 1825",
     
 }
'''
#transforming dataset "batting summary"
with open('t20_wc_batting_summary.json') as g:
    data2=json.load(g)
    
    all_record=[] #to store all matches
    for rec in data2:        
        all_record.extend(rec['battingSummary']) #a11 batting Summary are there,and in each batting summary there are further records of matches

print(all_record)
#now we will create dataframe
df_batting= pd.DataFrame(all_record)
df_batting.head()


#data transformation - 
#if dismissal column is null = not out , else = out
#so, we creating new column based on the values in dismissal column
df_batting['out/not_out']=df_batting.dismissal.apply(lambda x: "out" if len(x)>0 else "not out")

df_batting.drop(columns=["dismissal"],inplace=True)

#data cleaning
#removing special characters
df_batting['batsmanName']=df_batting['batsmanName'].apply(lambda x: x.replace('\xa0',''))

#connecting df_match and df_batting
# to connect some modifications are required, we need to create the dictionary in df_match table

#creating new column match_id
df_batting["match_id"]=df_batting["match"].map(match_ids_dict)
df_batting.head()


#now , we want this modification on our actual table
df_batting.to_csv('batting.csv',index=False)




'''with open('t20_wc_batting_summary.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('csvfile.csv', encoding='utf-8', index=False)

df = pd.read_json(r'C:\cricket\already\t20_json_files\t20_wc_batting_summary.json')
df.to_csv(r'C:\cricket\file1.csv',index=None)'''

