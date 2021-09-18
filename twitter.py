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


    def get_tweets_by_lang_and_keyword(self,required_count,keyword,lang,country):
        final_tweets = []
        for tweet in self.api.search(q=keyword, count=1,lang = lang , result_type = "popular",tweet_mode='extended'):
            oldest_tweet_id = tweet.id
        while len(final_tweets) < required_count:
            count = required_count - len(final_tweets)
            try:
                for tweet in self.api.search(q=keyword, count=count,lang = lang ,max_id=oldest_tweet_id - 1, result_type = "popular",tweet_mode='extended'):
                    tweet.country = country
                    oldest_tweet_id = tweet.id
                    if is_proper_tweet(tweet):
                        final_tweets.append(tweet)
            except tweepy.TweepError as e:
                print(e)
                break
            
        return final_tweets
    
    def get_replies(self):
        raise NotImplementedError
