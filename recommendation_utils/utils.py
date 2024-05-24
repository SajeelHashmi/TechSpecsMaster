from home.models import Wishlist,History
import pickle
import ast
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings   

def get_recommendation(user_id):
    objs_to_consider=3 #how many objects from wishlist/history to be taken into account. 3 means last three objects from history/wishlist will be considered.   
    wishlist = Wishlist.objects.filter(user_id=user_id)
    history = History.objects.filter(user_id=user_id)
    wishlist=[product.product_id for product in wishlist]
    history=[product.product_id for product in history]

    if len(wishlist)>objs_to_consider:
        wishlist=wishlist[-objs_to_consider:]
    
    if len(history)>objs_to_consider:
        history=history[-objs_to_consider:]
    
    to_consider=set(wishlist+history)
    to_recommend=set({})
    file_path = settings.BASE_DIR / 'recommendation_utils' / 'products_vectors.csv'
    vectors=pd.read_csv(file_path)
    print(':here')
    vectors['vector']=vectors['vector'].apply(ast.literal_eval)
    vec_matrix=np.array(list(vectors['vector']))
    
    for product_id in to_consider:
        row=vectors[vectors['product_id']==product_id]
        if row.empty:
            continue
        vector=np.array(list(row['vector']))
        similarities=cosine_similarity(vector,vec_matrix).reshape(-1,)

        indices = np.argsort(similarities)[-3:]  #2 most similar product selected for each product in to consider.
        for i in indices:
            recommendation=vectors.iloc[i]['product_id']
            if recommendation!=product_id:
                to_recommend.add(recommendation)            
    
    return(list(to_recommend))


def getRecommendedStore(storeList):
    file_path = settings.BASE_DIR / 'recommendation_utils' / 'store_ratings.csv'
    df = pd.read_csv(file_path)
    stores = []

    priceSum = 0
    average_r = {}
    zeroPrice = 0
    for i, s in enumerate(storeList):
        row = df[df['Name'] == s.name][['r1', 'r2', 'r3']]
        rowList = row.values.tolist()[0]
        average_r[s.name] = sum(rowList) / len(rowList)
        if s.price == 0:
            zeroPrice += 1
            continue
        priceSum += s.price
    averagePrice = priceSum / (len(storeList) - zeroPrice)

    bestIndex = 0
    bestScore = 0
    for i, s in enumerate(storeList):
        if s.price == 0:
            s.score = 0
            continue
        score = (( averagePrice - s.price) / averagePrice) + average_r[s.name]
        s.score = score
        if bestScore < score:
            bestScore = score
            bestIndex = i
    
    for i, s in enumerate(storeList):
        if i == bestIndex:
            s.lowestPrice = True
        else:
            s.lowestPrice = False
        stores.append(s)
    return stores

