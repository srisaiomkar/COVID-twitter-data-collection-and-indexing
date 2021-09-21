import pickle
# pickle_file = open("C:/Users/srisa/Downloads/crowdsourced_keywords.pickle", "rb")
# objects = []
# while True:
#     try:
#         objects.append(pickle.load(pickle_file))
#     except EOFError:
#         break
# pickle_file.close()

# print(objects)
pickle_file = open("data/poi_1.pkl", "rb")
df = pickle.load(pickle_file)
tweet_ids = []
for index, row in df.iterrows() :
    tweet_ids.append(row['id'])

print(tweet_ids)
# from datetime import datetime

# now = datetime.now() # current date and time

# date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
# print("date and time:",date_time)