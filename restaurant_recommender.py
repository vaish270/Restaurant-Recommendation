import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
# Load dataset
df = pd.read_csv("zomato.csv")
 
# Select relevant columns
df = df[['name', 'location', 'rest_type', 'dish_liked', 'cuisines']]
 
# Fill missing values
for col in ['location', 'rest_type', 'dish_liked', 'cuisines']:
    df[col] = df[col].fillna('')
 
# Combine text fields into one column for vectorization
df['combined'] = df['location'] + ' ' + df['rest_type'] + ' ' + df['dish_liked'] + ' ' + df['cuisines']
df['combined'] = df['combined'].str.strip()
 
# Drop rows with empty combined field
df = df[df['combined'] != '']
df = df[df['name'].notnull()]
 
# Reset index
df = df.reset_index(drop=True)
 
# Limit number of features to avoid memory issues
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['combined'])
 
# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
 
# Map restaurant names to indices
indices = pd.Series(df.index, index=df['name']).drop_duplicates()
 
# Recommendation function
def get_recommendations(name, num=5):
    idx = indices.get(name)
    if idx is None:
        return []
 
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num+1]
    restaurant_indices = [i[0] for i in sim_scores]
 
    # Return a list of dictionaries with full info
    results = df.iloc[restaurant_indices][['name', 'location', 'rest_type', 'dish_liked']]
    return results.to_dict(orient='records')
 
 
 