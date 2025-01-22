import pandas as pd
import  re


def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s[APM\u202f]+) - (.+)'
    matches = re.findall(pattern, data)

    # Separate dates and messages
    dates = [match[0] for match in matches]
    messages = [match[1] for match in matches]

    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = df['date'].str.replace(r'\s?(AM|PM)', '', regex=True)

    date_format = "%m/%d/%y, %H:%M"
    df['date'] = pd.to_datetime(df['date'], format=date_format)



    users = []
    messagess = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messagess.append(entry[2])
        else:
            users.append('group_notification')
            messagess.append(entry[0])

    df['user'] = users
    df['message'] = messagess

    df.drop(columns=['user_message'],inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num']=df['date'].dt.month
    df['date_only']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()

    return df

