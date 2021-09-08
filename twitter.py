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

    def get_tweets_by_poi_screen_name(self):
        
        raise NotImplementedError

    def get_tweets_by_lang_and_keyword(self):
        raise NotImplementedError

    def get_replies(self):
        raise NotImplementedError
