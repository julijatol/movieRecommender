import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('tmdb_5000_credits.csv')

movies['combined_features'] = movies.apply(lambda x: ' '.join(x['description'].split()) + ' ' + x['keywords'] + ' ' + x['genre'], axis=1)

#TF-IDF is a descriptive method to analyze the text
#Cosine Similarity is prescriptive method, used to generate recommendations
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_simscore(title,cosine_sim=cosine_sim):
    index = movies[movies['title'] == title].index[0]
    similarity_scores = list(enumerate(cosine_sim[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:]
    target_certification = movies.loc[index, 'certification']
    filtered_scores = []
    for score in similarity_scores:
        if len(filtered_scores) >= 10:
            break
        if movies.loc[score[0], 'certification'] == target_certification:
            filtered_scores.append(score)
    return filtered_scores

def get_recommendations(title):
    scores = get_simscore(title)
    movie_indices = [i[0] for i in scores]
    recommendations = movies.iloc[movie_indices]
    return recommendations['title'].tolist()

def get_ids(title):
    movie_list = get_recommendations(title)
    idx = []
    for item in movie_list:
        movie_row = movies[movies['title'] == item]
        if not movie_row.empty:
            movie_id = movie_row.iloc[0]['movie_id']
            idx.append(movie_id)
    return idx

def similarity_distribution(title):
    recs_list = get_recommendations(title)
    if len(recs_list) == 0:
        return []

    movie_desc = movies[movies['title'].str.lower() == title.lower()]['description'].values[0]
    movie_keyw = movies[movies['title'].str.lower() == title.lower()]['keywords'].values[0]
    movie_genre = movies[movies['title'].str.lower() == title.lower()]['genre'].values[0]

    dist_data = []

    for item in recs_list:
        desc = movies[movies['title'].str.lower() == item.lower()]['description'].values[0]
        keyw = movies[movies['title'].str.lower() == item.lower()]['keywords'].values[0]
        gn = movies[movies['title'].str.lower() == item.lower()]['genre'].values[0]

        descriptions = [movie_desc, desc]
        keywords = [movie_keyw, keyw]
        genres = [movie_genre, gn]

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_description = tfidf.fit_transform(descriptions)
        tfidf_keywords = tfidf.fit_transform(keywords)
        tfidf_genre = tfidf.fit_transform(genres)


        cosine_sim_description = cosine_similarity(tfidf_description[0:1], tfidf_description[1:2])[0][0]
        cosine_sim_keywords = cosine_similarity(tfidf_keywords[0:1], tfidf_keywords[1:2])[0][0]
        cosine_sim_genre = cosine_similarity(tfidf_genre[0:1], tfidf_genre[1:2])[0][0]

        dist_data.append([
            int(cosine_sim_description * 100),
            int(cosine_sim_keywords * 100),
            int(cosine_sim_genre * 100)
        ])

    return dist_data, recs_list












