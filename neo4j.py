# -*- coding: utf-8 -*-
from py2neo import Graph

graph = Graph("bolt://localhost:7687", auth=("neo4j", "123")) 

#Les parametres alpha, beta, gamma, delta

alpha = 0.3
beta = 0.3 
gamma = 0.3
delta = 0.1


TEST1 = {
    "ville" : "Wilmington",
    "Ambiances" :  ["casual"],
    "Categories" :  ["Pizza","Burgers","Italian"],
    "pricerange" : 1
}

ID = "4156"
NB_USER = 23082

TEST2 = {
    "ville" : "Wilmington",
    "Ambiances" :  ["casual","romantic"],
    "Categories" :  ["Chinese"],
    "pricerange" : 2
}

TEST3 = {
    "ville" : "Wilmington",
    "Ambiances" :  ["hipster"],
    "Categories" :  ["Nightlife","Bars"],
    "pricerange" : 1
}

TEST4 = {
    "ville" : "New Castle",
    "Ambiances" :  ["causal","classy"],
    "Categories" :  ["Coffee & Tea"],
    "pricerange" : 2
}

TEST5 = {
    "ville" : "New Castle",
    "Ambiances" :  ["classy"],
    "Categories" :  ["Seafood"],
    "pricerange" : 1
}


# ========================================== QUERY ===================================================


# ++++++++++++++++++++ CENTRALITE ++++++++++++++++++++

#centrality_s1

nb_max_friends = "MATCH (u:User)   RETURN size(u.friends), u.friends AS list ORDER BY size(list) DESC LIMIT 1"
nb_friends = "MATCH (u:User{user_id: $id}) RETURN size(u.friends)"

# centrality_s2
params2 = {'id':ID}
# return pour un seul user, faire la somme plus tard
nb_ff = "match (u1:User{user_id: $id})-[:FRIEND]->(u2:User) return sum(size(u2.friends))"
#max_ff = "match (u1:User)-[:FRIEND]->(u2:User) return size(u2.friends) , u2.friends AS f ORDER BY size(f) DESC LIMIT 1"
max_ff = "match (u1:User{user_id: $id})-[:FRIEND]->(u2:User) return sum(size(u2.friends))"

# centrality_s3
fans = "Match (u:User{user_id: $id}) return u.fans"
max_fans = "Match (u:User) return toInteger(u.fans) ORDER BY toInteger(u.fans) DESC LIMIT 1"

# ++++++++++++++++++++ VALIDITE ++++++++++++++++++++

# validite_s4
# by id
nb_usefule = "match (u:User{user_id:$id})-[:WROTE]->(r:Review) where toInteger(r.useful) >= 1  return Count(r.review_id)"
review_count = "match (u:User{user_id:$id}) return u.review_count"

# validite_s5
nb_cool = "match (u:User{user_id:$id})-[:WROTE]->(r:Review) where toInteger(r.cool) >= 1 return Count(r.review_id)"

# ++++++++++++++++++++ ADEQUATION ++++++++++++++++++++

#s_5
review_count = "match (u:User{user_id:$id}) return u.review_count"
m = "match (u:User{user_id:$id})-[:WROTE]->(r:Review)-[:REVIEW_OF]->(b:Business) return size(b.`attributes.Ambience`)"

# return : Count(*), b.Ambience
# à filtrer pour récuprer seulement les restaurants ayant $ambiance_j et faire la somme des count
# en suite determiné reviewPos(j)
count_and_ambiancies = "match (u:User{user_id:$id})-[:WROTE]->(r:Review)-[:REVIEW_OF]->(b:Business)  where toInteger(r.stars) >= 4 return Count(*),b.`attributes.Ambience`"

#s_7
n = "match (u:User{user_id:$id})-[:WROTE]->(r:Review)-[:REVIEW_OF]->(b:Business) return size(b.categories)"
# à filtrer aussi comme count_and_ambiancies
count_and_categories = "match (u:User{user_id:$id})-[:WROTE]->(r:Review)-[:REVIEW_OF]->(b:Business)  where toInteger(r.stars) >= 4 return Count(*),b.categories"

#s_8
pricerange = "match (u:User{user_id:$id})-[:WROTE]->(r:Review)-[:REVIEW_OF]->(b:Business) return b.`attributes.RestaurantsPriceRange2`"
reviewPos_pricerange = "match (u:User{user_id:$id})-[:WROTE]->(r:Review)-[:REVIEW_OF]->(b:Business) return Count(*),b.`attributes.RestaurantsPriceRange2`"


# ++++++++++++++++++++ GEOGRAPHIQUE ++++++++++++++++++++

#s_9
nb_review_ui_vr = "match (u1:User{user_id:$id})-[:FRIEND]->(u2:User)-[:WROTE]->(r:Review)-[:REVIEW_OF]->(b:Business{city:$city}) return Count(r.review_id)"
total_reviews_count = "match (u1:User{user_id:$id})-[:FRIEND]->(u2:User) return sum(toInteger(u2.review_count))"



#==================== FONCTIONS ====================

import re 
from tqdm import tqdm
import operator


def get_mean(scores,n):
    
    s = 0
    for i in range(len(scores)):
        s+=scores[i]
    
    return s/n




def get_users_scores(TEST):

    RES = {}

    for i in tqdm(range(NB_USER)):

        params = {'id':str(i)}

        # ********** CENTRALITY ************
        max_friends = graph.run(nb_max_friends).to_table()
        MAX_FRIENDS = int(max_friends[0][0]) if len(max_friends) > 0 else 0 
        nb_fr = graph.run(nb_friends,params).to_table()
        NB_FRIENDS = int(nb_fr[0][0]) if len(nb_fr) > 0 else 0 

        nb_f = graph.run(nb_ff,params).to_table()
        NB_FF = int(nb_f[0][0]) if len(nb_f) > 0 else 0
        MAX_FF = int(graph.run(max_ff,params2).to_table()[0][0])
        fan = graph.run(fans,params).to_table()
        FANS = int(fan[0][0]) if len(fan) > 0 else 0
        MAX_FANS = int(graph.run(max_fans).to_table()[0][0])

        s_1 = NB_FRIENDS/MAX_FRIENDS
        s_2 = NB_FF/MAX_FF
        s_3 = int(FANS)/int(MAX_FANS)

        score_centralite =  get_mean([s_1,s_2,s_3],3)
        
        # ********** VALIDITE ************

        nb_useful = graph.run(nb_usefule,params).to_table()
        NB_USEFULE = int(nb_useful[0][0]) if len(nb_useful) > 0 else 0
        review_c = graph.run(review_count,params).to_table()
        # 1 pour éviter les divisions par 0
        REVIEW_COUNT = int(review_c[0][0]) if len(review_c) > 0 else 1
        cools = graph.run(nb_cool,params).to_table()
        NB_COOL = int(cools[0][0]) if len(cools) > 0 else 0

        if REVIEW_COUNT > 0:
            s_4 = int(NB_USEFULE)/int(REVIEW_COUNT)
            s_5 = int(NB_COOL)/int(REVIEW_COUNT)
        else:
            s_4,s_5 = 0,0

        score_validite = get_mean([s_4,s_5],2)

        # ********** ADEQUATION ************
        ambiances = graph.run(m,params).to_table()
        M = int(ambiances[0][0]) if len(ambiances) > 0 else 1
        cats = graph.run(n,params).to_table()
        N = int(cats[0][0]) if len(cats) > 0 else 1
        
        AMBIANCE = TEST["Ambiances"]
        CATEGORY = TEST["Categories"]
        reviewPos_j1 = 0
        reviewPos_j2 = 0
        reviewPos_j3 = 0
        COUNT_AMBIANCIES = graph.run(count_and_ambiancies,params).to_table()
        COUNT_CATEGORIES =  graph.run(count_and_categories,params).to_table()
        #PRICERANGE = graph.run(pricerange,params).to_table()
        REVIEWPOS_PRICERANGE = graph.run(reviewPos_pricerange,params).to_table()

        pricerange = TEST["pricerange"]

        for line in REVIEWPOS_PRICERANGE:
            c = line[0]
            #review_pricerange = line[1]
            if len(line[1]) !=0:
                if pricerange == int(line[1]):
                    reviewPos_j3+=c

        for line in COUNT_AMBIANCIES:
            #la requete return les ambiances sous forme de str 
            #alors on fait une opération regex pour voir si l'ambiance existe ou pas 
            #Puis incrementer le compteur 
            for ambiance in AMBIANCE:
                x = re.findall(ambiance, line[1])
                if(len(x)!=0):
                    reviewPos_j1 += line[0]

        for line in COUNT_CATEGORIES:
            for category in CATEGORY:
                x = re.findall( category, line[1])
                if(len(x)!=0):
                    reviewPos_j2 += line[0]
        if REVIEW_COUNT > 0 and M > 0:
            s_6 = (reviewPos_j1/int(REVIEW_COUNT))/M
        else:
            s_6 = 0
        if  REVIEW_COUNT > 0 and N > 0:
            s_7 = (reviewPos_j2/int(REVIEW_COUNT))/N
        else:
            s_7 = 0
        if REVIEW_COUNT > 0:
            s_8 = (reviewPos_j2/int(REVIEW_COUNT))
        else:
            s_8 = 0


        # ********** GEOGRAPHIE ************

        score_adequation = get_mean([s_6,s_7,s_8],3)

        total_r = graph.run(total_reviews_count,params).to_table()
        TOTAL_REVIEW_COUNT = total_r[0][0] if len(total_r)>0 else 1
        re_j4 =  graph.run(nb_review_ui_vr,{'id':i,'city':TEST["ville"]}).to_table()
        reviewPos_j4 = re_j4[0][0] if len(re_j4)>0 else 0

        if TOTAL_REVIEW_COUNT > 0:
            score_geo = reviewPos_j4/TOTAL_REVIEW_COUNT
        else:
            score_geo = 0

        # ************ RESULTAT ***********
        #print(score_centralite,score_validite,score_adequation,score_geo)
        SCORE = alpha*score_centralite + beta*score_validite + gamma*score_adequation + delta*score_geo
        RES[i] = SCORE

        #print("SCORE i : ", SCORE)

    return RES

#====================== TEST ===========================


# SCORES_TEST1 = get_users_scores(TEST1)
# SCORES_TEST2 = get_users_scores(TEST2)
# SCORES_TEST3 = get_users_scores(TEST3)

print("Exécution de test 4 en cours ")

SCORES_TEST4 = get_users_scores(TEST4)

#print("Exécution de test 5 en cours ")
#SCORES_TEST5 = get_users_scores(TEST5)




#prendre uniquement les 10 meilleurs users
BEST_SCORES_TEST4 = sorted(SCORES_TEST4.items(), reverse=True , key=operator.itemgetter(1))[:10]
BEST_SCORES_TEST44 = sorted(SCORES_TEST4.items(), key=operator.itemgetter(1))[:10]

#print(len(SCORES_TEST1))
print(BEST_SCORES_TEST4)
print(BEST_SCORES_TEST44)

#  

#=================== RESULTATS DES TESTS AVEC nombre d'utilisateur total ================

TEST4_NB_USER = """[(7146, 0.4023656236138967), (21174, 0.40189389490380323), (18600, 0.3052921334134525), (21847, 0.3052825114060152), (12531, 0.3039399536906079), (16935, 0.3038649132794126), (20381, 0.303854561047423), (17184, 0.3033733766461039), (20171, 0.30270687666294066), (12978, 0.30236949510412975)]
[(522, 7.4487895716946e-05), (546, 7.4487895716946e-05), (628, 7.4487895716946e-05), (744, 7.4487895716946e-05), (878, 7.4487895716946e-05), (903, 7.4487895716946e-05), (1011, 7.4487895716946e-05), (1029, 7.4487895716946e-05), (1142, 7.4487895716946e-05), (1153, 7.4487895716946e-05)]"""
#=================== RESULTATS DES TESTS AVEC 3000 USERS ================


TEST1_3000 = """ 
                 [(84, 0.22201032265740103), (2939, 0.2179419812489107), (2712, 0.20811883797828362), (2655, 0.20546139265762173), 
                 (297, 0.20339329012979906), (2644, 0.2021142041023019), (2286, 0.18714257463362843), (1569, 0.18220920706764163), 
                 (1175, 0.1764654284213893), (1320, 0.17373673948085297)]
            """

TEST2_3000 = """
                 [(1980, 0.25491173925195565), (2425, 0.25491173925195565), (84, 0.22201078429955448), (1175, 0.17625743794340593), 
                 (1320, 0.17346651496660595), (985, 0.16889710559318794), (2939, 0.16792554199196513), 
                  (529, 0.16756811172996117), (32, 0.16323896742013388), (2504, 0.15622156636122828)]
            """
TEST4_3000 = """
                [(84, 0.22201032265740103), (1175, 0.1764654284213893), (1320, 0.17346484059784298), (985, 0.16857863425560832),
                 (529, 0.16756811172996117), (2939, 0.16729263059956007), (32, 0.163302327186304), (2504, 0.15622156636122828), 
                 (297, 0.15262405936056828), (2600, 0.1519466379277465)] 
            """
            
TEST3_3000 = """
                [(985, 0.2694960654482689), (84, 0.22201032265740103), (2311, 0.21707509322259344), (2378, 0.20631745997003637), 
                (2167, 0.20628157089358531), (1274, 0.20315185743088865), (2286, 0.18714257463362843), (1175, 0.1764654284213893), 
                (1320, 0.17346484059784298), (436, 0.1713381799973485)]
            """

TEST5_3000 = """
                [(84, 0.2220845417573025), (2600, 0.20279409555486513), (1716, 0.18462341295097112), (1175, 0.17625085916916314), 
                (1320, 0.17346484059784298), (985, 0.16857863425560832), (529, 0.16756811172996117), (2939, 0.16729263059956007), 
                (32, 0.1632547898434929), (2504, 0.15622156636122828)]
            """
            


#====================== Resultats avec erreur ===========================


RES2_BEST = """ Les 10 meilleures utilisateurs : 

[(529, 3.631853826015675), (84, 0.9549358180405055), (159, 0.9321995966336962), 
 (4156, 0.9298546602549067), (7448, 0.8583564960539637), (1287, 0.8167084672950886), 
 (889, 0.8139402790398268), (245, 0.7332823241346722), (32, 0.7166519157658049), 
 (14237, 0.6785879107529034)]

"""

RES2_WORST = """ Les 10 pires utilisateurs : 

[(522, 7.4487895716946e-05), (546, 7.4487895716946e-05), (628, 7.4487895716946e-05), 
 (744, 7.4487895716946e-05), (878, 7.4487895716946e-05), (903, 7.4487895716946e-05), 
 (1011, 7.4487895716946e-05), (1029, 7.4487895716946e-05), (1142, 7.4487895716946e-05), 
 (1153, 7.4487895716946e-05)]

"""

RES4_BEST = """ Les 10 meilleures utilisateurs : 

[(529, 3.631853826015675), (84, 0.9549353563983521), (159, 0.9322419967418498), 
 (4156, 0.9298522656188914), (7448, 0.8583561986871469), (1287, 0.816740433371203), 
 (889, 0.813940152305467), (245, 0.7332814551739492), (32, 0.716715275531975), 
 (14237, 0.6785871661512652)]

"""

RES4_WORST = """ Les 10 pires utilisateurs : 

[(522, 7.4487895716946e-05), (546, 7.4487895716946e-05), (628, 7.4487895716946e-05), 
 (744, 7.4487895716946e-05), (878, 7.4487895716946e-05), (903, 7.4487895716946e-05), 
 (1011, 7.4487895716946e-05), (1029, 7.4487895716946e-05), (1142, 7.4487895716946e-05), 
 1153, 7.4487895716946e-05)]
"""


RES5_BEST = """ Les 10 meilleures utilisateurs : 

[(529, 3.631853826015675), (84, 0.9550095754982536), (159, 0.9321987614506222), 
 (4156, 0.9298522656188914), (7448, 0.8583561986871469), (1287, 0.8167078684448811), 
 (889, 0.813940152305467), (245, 0.7332814551739492), (32, 0.716667738189164), 
 (14237, 0.6785871661512652)]

"""

RES5_WORST = """ Les 10 pires utilisateurs : 

[(522, 7.4487895716946e-05), (546, 7.4487895716946e-05), (628, 7.4487895716946e-05), 
 (744, 7.4487895716946e-05), (878, 7.4487895716946e-05), (903, 7.4487895716946e-05), 
 (1011, 7.4487895716946e-05), (1029, 7.4487895716946e-05), (1142, 7.4487895716946e-05), 
 (1153, 7.4487895716946e-05)]

"""









