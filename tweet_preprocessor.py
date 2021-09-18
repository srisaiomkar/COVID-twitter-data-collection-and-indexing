import demoji, re, datetime
import preprocessor


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweets,are_poi_tweets):
        ldict = []
        for tweet in tweets:
            dct = {
            'verified': tweet.user.verified,
            'country': tweet.country,
            'id':tweet.id,
            'replied_to_tweet_id': tweet.in_reply_to_status_id,
            'replied_to_user_id': tweet.in_reply_to_user_id,
            'tweet_text': tweet.full_text,
            'tweet_lang': tweet.lang,
            'tweet_date':_get_tweet_date(tweet.created_at.strftime('%a %b %d %H:%M:%S +0000 %Y')).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'geolocation:': tweet.geo,
            }
            if(are_poi_tweets):
                dct['poi_name'] = tweet.user.screen_name
                dct['poi_id'] = tweet.user.id
            hastags = _get_entities(tweet,'hashtags')
            mentions = _get_entities(tweet,'mentions')
            tweet_urls = _get_entities(tweet,'urls')
            tweet_emoticons = _text_cleaner(tweet.full_text)[1]
            if(len(hastags)):
                dct['hashtags'] = hastags
            if(len(mentions)):
                dct['mentions'] = mentions
            if(len(tweet_urls)):
                dct['tweet_urls'] = tweet_urls
            if(len(tweet_emoticons)):
                dct['tweet_emoticons'] = tweet_emoticons

            if (tweet.in_reply_to_status_id is not None):
                dct['reply_text'] = tweet.full_text
            if tweet.lang == 'hi':
                dct["text_hi"] = tweet.full_text   
            elif tweet.lang == 'en':
                dct["text_en"] = tweet.full_text   
            elif tweet.lang == 'es':
                dct["text_es"] = tweet.full_text   
            ldict.append(dct)
        return ldict

def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet.entities['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet.entities['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet.entities['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text,emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))

def is_proper_tweet(tweet):
        return (not tweet.retweeted) and ('RT @' not in tweet.full_text) and (tweet.in_reply_to_status_id  is None)    