from urlextract import  URLExtract
from wordcloud import  WordCloud
from collections import  Counter
import  pandas as pd
import emoji
def fetch_status(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    num_messages= df.shape[0]

    words=[]
    for message in df['message']:
        words.extend(message.split())
    num_words=len(words)

    num_media_msg=df[df['message']=='<Media omitted>'].shape[0]

    urls = []
    ur = URLExtract()
    for message in df['message']:
        urs = ur.find_urls(message)
        if urs:
            urls.extend(urs)
    num_urls_msg=len(urls)

    return num_messages,num_words,num_media_msg,num_urls_msg

def fetch_busy_user(df):
    df=df[df['user']!='group_notifications']
    X=df['user'].value_counts().head()
    df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'user':'user','count':'percentage'})
    return X,df

def crearte_word_cloud(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    df = df[df['message'] != '<Media omitted>']
    df = df[df['user'] != 'group_notification']
    def remove_stopwords(message):
        words = []
        f = open('stop_hinglish.txt', 'r')
        stop_words = f.read()

        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return ' '.join(words)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df['message']=df['message'].apply(remove_stopwords)
    df_wc=wc.generate(df['message'].str.cat(sep=' '))
    return df_wc

def most_common_word(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))

def fetch_emoji(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>']
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df=emoji_df.rename(columns={0:'emoji',1:'count'})
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>']
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>']
    daily_timelines = df.groupby('date_only')['message'].count().reset_index()
    return daily_timelines

def weekly_activity(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>']
    return  df['day_name'].value_counts()

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>']
    return  df['month'].value_counts()
