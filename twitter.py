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
    
    def get_tweets_by_poi_screen_name(self,screen_name,total_count):
        final_tweets = []
        collected_tweets_count = 0

        # country and poi dictionary
        country_poi_dict = {"USA": ["CDCgov", "JoeBiden", "KamalaHarris", "BarackObama", "tedcruz","HHSGov"], 
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


    def get_tweets_by_lang_and_keyword(self,keyword_item):
        count = keyword_item["count"], 
        keyword = keyword_item["name"],
        country = keyword_item["country"]
        final_tweets = []
        prev_id = 0
        previous_collected_tweets_count = 0
        try:
            for tweet in tweepy.Cursor(self.api.search, q=keyword, result_type='recent', timeout=999999, tweet_mode='extended').items(3000):
                prev_id = tweet.id
                tweet.country = country
                if is_proper_tweet(tweet):
                    print(tweet.full_text)
                    print("outside loop", len(final_tweets))
                    final_tweets.append(tweet)
            i = 1    
            while(len(final_tweets) < 1500):
                if(previous_collected_tweets_count == len(final_tweets)):
                    break
                i+=1
                previous_collected_tweets_count = len(final_tweets)
                for tweet in tweepy.Cursor(self.api.search, q=keyword,max_id = prev_id-1 ,timeout=999999, tweet_mode='extended').items(2000):
                    tweet.country = country
                    if is_proper_tweet(tweet):
                        print(tweet.full_text)
                        print("outside loop",i,  len(final_tweets))
                        final_tweets.append(tweet)       
        except Exception as e:
            print(e)
            print("an exception has occured.. continuing\n")
        finally:
            return final_tweets


    def get_poi_replies(self,poi):
        poi_name = poi["screen_name"]
        poi_local_id = poi["id"]
        country = poi["country"]
        final_replies = []
        prev_id = 0
        prev_final_replies = 0
        pickle_file = open(f"data/poi_{poi_local_id}.pkl", "rb")
        df = pickle.load(pickle_file)
        tweet_ids = []
        for index, row in df.iterrows() :
            tweet_ids.append(row['id'])
        tweet_ids.sort(reverse=True)
        for reply in tweepy.Cursor(self.api.search, q='to:{} filter:replies'.format(poi_name), sinceId=tweet_ids[0],tweet_mode='extended').items(3000):
            if hasattr(reply, 'in_reply_to_status_id_str'):
                    prev_id = reply.in_reply_to_status_id
                    if reply.in_reply_to_status_id in tweet_ids:
                        reply.country = country
                        final_replies.append(reply)
                        print(len(final_replies))
                        print(reply.full_text)
        i = 0;
        while(len(final_replies) < 2000):
            if(prev_final_replies == len(final_replies)):
                break
            i+=1
            prev_final_replies = len(final_replies)
            try:
                for reply in tweepy.Cursor(self.api.search, q='to:{} filter:replies'.format(poi_name), sinceId= prev_id +1 ,tweet_mode='extended').items(3000):
                    if hasattr(reply, 'in_reply_to_status_id_str'):
                        prev_id = reply.in_reply_to_status_id
                        if reply.in_reply_to_status_id in tweet_ids:
                            reply.country = country
                            final_replies.append(reply)
                            print("inside loop",i,  len(final_replies))
                            print(reply.full_text)   
            except:
                break     
        
        return final_replies