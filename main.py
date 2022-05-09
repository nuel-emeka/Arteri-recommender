import pandas as pd
import psycopg2
from sklearn.metrics.pairwise import cosine_similarity as cs
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from userData import userData
import uvicorn



def fetchData():
    # postgres database
    # just a little changes
    PG_USER= 'postgres'
    PG_PASSWORD= 'Arteri-Insura123!'
    PG_ADDRESS= 'arteri-insura-prod.ciejcbdgcnne.us-east-2.rds.amazonaws.com'
    PG_PORT= '5432'
    PG_DATABASE= 'arteri'
    # connecting to DB
    conn = psycopg2.connect(dbname=PG_DATABASE, user=PG_USER, password=PG_PASSWORD, host=PG_ADDRESS)
    sql = ("SELECT id, description, title, price, tier, coverage, family_planning, mental_health, dental_care, telemedicine_service, cashback_benefit, anc_delivery_coverage, eye_care_cost, gym_membership, annual_medical_screening FROM plans WHERE plans.deleted_at IS NULL")
    data = pd.read_sql_query(sql,conn)
    rawData = pd.DataFrame(data)
    
    # returning the database
    return rawData

def get_data_public(filename):
    filename = filename.replace(' ', '%20')
    owner = 'nuel-emeka'
    repo = 'RECOMMENDER'
    path = 'Data/{}'.format(filename)
    # get link
    r = 'https://raw.githubusercontent.com/{owner}/{repo}/main/{path}'.format(owner=owner, repo=repo, path=path)
    # Load data to df
    df = pd.read_csv(r)
    
    return df

def get_ready(data):
    now = data
    now['tier'] = now['tier'].apply(lambda x: x-1)
    for col in now.columns[6:]:
        now[col] = now[col].apply(lambda x: int(x))
    now = pd.get_dummies(now, columns=['coverage'], prefix=['location'])
    now = now.iloc[:, 4:]
    return now

# getting all data
data = fetchData()                                                  #hmo data
df = get_ready(data)                                                #necessary hmo data
hmoRating = get_data_public("HMO ratings - Form responses 1.csv")   #hmo ratings dataset

# Function to implement cosine similarity
def cosine_sim(response, data):
    """ largest value signifies great similarity"""
    df = data.copy()
    test = [response]
    index_ = []
    results = []
    for index in df.index:
        value = cs([df.loc[index,:].values], test)[0][0]
        index_.append(index)
        results.append(value)
    
    df_ = pd.DataFrame({'HMO index': index_ ,'cosine similarity': results})
    df_ = df_.sort_values('cosine similarity', ascending=False).set_index('HMO index')

    return df_.index[:5].values

#

def clean_ratings(ratings_data, hmo):
    ratings = ratings_data
    hmo = [i.upper() for i in hmo]
    
    ratings.rename(columns={'What is the name of your HMO?': 'Name'}, inplace=True)
    ratings.dropna(subset=['Name'], inplace=True)
    ratings['Name'] = ratings['Name'].apply(lambda x: x.upper().strip())
    ratings['sum ratings'] = ratings.iloc[:, [3,4,5,6]].sum(axis=1)
    ratings = ratings.groupby('Name').mean()[['sum ratings']]
    
    hmo = [hmo_ for hmo_ in hmo if hmo_ in ratings.index]
    hmo_ratings = ratings.loc[hmo, ['sum ratings']].sort_values(by='sum ratings', ascending=False)

    return hmo_ratings.index[:3].to_list()


def top_5_dict(result):
    top_5 = result
    
    hmo_names = [hmo.upper().strip() for hmo in data.loc[top_5, 'description']]
    hmo_dict = {hmo: [] for hmo in set(hmo_names)}
    for hmo, index in zip(hmo_names, top_5):
        hmo_dict.get(hmo).append(index)
    
    return hmo_dict, hmo_names


def top_3_index(top5):
    top5_dict = top_5_dict(top5)
    rating = clean_ratings(hmoRating, top5_dict[0].keys())
    for hmo in top5_dict[1]:
        if hmo not in rating:
            rating.append(hmo)
        else:
            pass

    index = []
    for name in rating[:3]:
        index.extend(top5_dict[0].get(name))
    
    return index[:3]


def recommend(test, df=df):
    tier = test[0]
    loc = test[-2]
    
    if loc == 0:
        rows_drop = df[(df['location_lagos']==1)].index
        df = df.drop(rows_drop, axis=0)
    else:
        pass
    
    if tier == 0:
        rows_drop = df[df['tier']>0].index
        df = df.drop(rows_drop, axis=0)
        results = cosine_sim(test, df)
    elif tier == 1:
        rows_drop = df[df['tier']>1].index
        df = df.drop(rows_drop, axis=0)
        results = cosine_sim(test, df)
    elif tier == 2:
        rows_drop = df[df['tier']>2].index
        df = df.drop(rows_drop, axis=0)
        results = cosine_sim(test, df)
    else:
        results = cosine_sim(test, df)
        
    index = top_3_index(results)
    index_ = ''
    for i in data.loc[index, 'id']:
        index_ = index_+str(i)+str(', ')
    index_ = index_[:-2]
    
    return index_


app = FastAPI()

app.add_middleware(CORSMiddleware,
                    allow_origins = ["*"],
                    allow_credentials = True,
                    allow_methods = ["*"],
                    allow_headers = ["*"])

@app.get('/')
def home():
    return "Welcome to Arteri Africa"

@app.post('/predict')
def predict(data: userData):
    data = data.dict()
    tier = data['tier'] - 1 # tier 1 to 4 is encoded as 0 to 3
    family_planning = int(data['family_planning'])
    mental_health = int(data['mental_health'])
    dental_care = int(data['dental_care'])
    telemedicine_service = int(data['telemedicine_service'])
    cashback_benefit = int(data['cashback_benefit'])
    anc_delivery_coverage = int(data['anc_delivery_coverage'])
    eye_care_cost = int(data['eye_care_cost'])
    gym_membership = int(data['gym_membership'])
    annual_medical_screening = int(data['annual_medical_screening'])
    location = data['location']
    user = [tier, family_planning, mental_health, dental_care, telemedicine_service, cashback_benefit, anc_delivery_coverage, eye_care_cost,
            gym_membership, annual_medical_screening, location]
    
    if user[-1].strip().lower()=='lagos':
        user.pop(-1)
        user.append(1)
        user.append(0)
    else:
        user.pop(-1)
        user.append(0)
        user.append(1)   
    value = recommend(test=user, df=df)
    return value
    

if __name__=='__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
