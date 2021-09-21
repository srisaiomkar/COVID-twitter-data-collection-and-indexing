import pickle
from tweet_preprocessor import is_proper_tweet
import tweepy


class Twitter:
    def __init__(self):
        consumer_key = "LSB6SZwAfaAfDPT71kXRtUnQE"
        consumer_secret = "yOOJeF6MPJHjdRT98SXm6RtIic9WeHqTOND8g1RvQ3lxLejiYM"
        access_token = "1432439931281059842-eHsbjreyVfdy5kOgYeM67SqOCFjTTH"
        access_token_secret = "jM3P3Dq2BLEOO63hr0DAPSr72iSOcrkrDt9IPFaSOS92m"
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _meet_basic_tweet_requirements(self):
        raise NotImplementedError
    
    def get_tweets_by_poi_screen_name(self,screen_name,total_count):
        final_tweets = []
        collected_tweets_count = 0

        # country and poi dictionary
        country_poi_dict = {"USA": ["CDCgov", "JoeBiden", "KamalaHarris", "BarackObama", "tedcruz"], 
                    "INDIA": ["MoHFW_INDIA", "narendramodi", "RahulGandhi", "AmitShah", "ArvindKejriwal"],
                    "MEXICO": ["SSalud_mx", "lopezobrador_", "m_ebrard", "PRI_Nacional", "PRDMexico", "rodrigobocardi"]}

        for country,pois in country_poi_dict.items():
            for poi in pois:
                if screen_name == poi:
                    poi_country = country

        tweets = []
        for tweet in tweepy.Cursor(self.api.user_timeline, screen_name=screen_name,tweet_mode='extended').items(199):
            oldest_tweet_id = tweet.id
            if is_proper_tweet(tweet):
                final_tweets.append(tweet)
                collected_tweets_count+=1
                tweet.country = poi_country

        oldest_tweet_id-=1 

        while collected_tweets_count < total_count:
            tweets = tweepy.Cursor(self.api.user_timeline, screen_name=screen_name, max_id=oldest_tweet_id,tweet_mode='extended').items(199)
            for tweet in tweets:
                oldest_tweet_id = tweet.id
                if is_proper_tweet(tweet):
                    final_tweets.append(tweet)
                    collected_tweets_count+=1
                    tweet.country = poi_country
                
            oldest_tweet_id-=1

        return final_tweets


    def get_tweets_by_lang_and_keyword(self,required_count,keyword,country):
        final_tweets = []
        try:
            for tweet in tweepy.Cursor(self.api.search, q=keyword, result_type='recent', timeout=999999, tweet_mode='extended').items(required_count*15):
                tweet.country = country
                oldest_tweet_id = tweet.id
                if is_proper_tweet(tweet):
                    print(tweet.full_text)
                    print("outside loop, count = ", len(final_tweets))
                    final_tweets.append(tweet)
        except Exception as e:
            print("an exception has occured.. continuing\n")
        finally:
            return final_tweets
        # while len(final_tweets) < required_count:
        #     for tweet in tweepy.Cursor(self.api.search, q=keyword, result_type='recent', timeout=999999, tweet_mode='extended', max_id=oldest_tweet_id).items(2000):
        #         print(tweet.full_text)
        #         print("inside loop, count = ", len(final_tweets))
        #         tweet.country = country
        #         oldest_tweet_id = tweet.id
        #         if is_proper_tweet(tweet):
        #             final_tweets.append(tweet)
        #     oldest_tweet_id-=1
            
    
    def get_poi_replies(self,poi_name,poi_local_id):
        final_replies = []
        reply_counter = {}
        prev_id = 0
        pickle_file = open(f"poi_{poi_local_id}.pkl", "rb")
        df = pickle.load(pickle_file)
        tweet_ids = []
        for index, row in df.iterrows() :
            tweet_ids.append(row['id'])
            reply_counter[row['id']] = 0
        tweet_ids.sort(reverse=True)

        for tweet_id in tweet_ids:
            if len(final_replies) == 0:
                tweet_replies = tweepy.Cursor(self.api.search, q='to:{} filter:replies'.format(poi_name), sinceId=tweet_id,
                                            tweet_mode='extended').items(300)
            else:
                tweet_replies = tweepy.Cursor(self.api.search, q='to:{} filter:replies'.format(poi_name), sinceId=tweet_id,
                                            max_id=prev_id - 1, tweet_mode='extended').items(300)

            while True:
                reply = tweet_replies.next()
                if hasattr(reply, 'in_reply_to_status_id_str'):
                    if reply.in_reply_to_status_id in tweet_ids:
                        if reply_counter[reply.in_reply_to_status_id] >= 100:
                            break
                        final_replies.append(reply)
                        reply_counter[reply.in_reply_to_status_id]+=1

            prev_id = tweet_id
        return final_replies



            

