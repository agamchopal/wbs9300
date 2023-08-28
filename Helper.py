from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import nltk
import emoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')
stopWords = set(stopwords.words("english"))


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        # 1. number of messages
    extractor = URLExtract()
    urls = extractor.find_urls("Let's www.gmail.com have URL stackoverflow.com as an example google.com, http://facebook.com, ftp://url.in")
    y = []
    for message in df['message']:
        y.extend(extractor.find_urls(message))
    num_of_links = len(y)
    num_messages = df.shape[0]
    # 2. Number of words
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    for i in df["user"]:
        unique_counts = df["user"].nunique()

    return num_messages, len(words), num_media_messages, num_of_links,unique_counts
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns = {'index': 'names', 'user': 'percentage'})
    return x, df
def generate_text_file_content():
    content="ab"
    return content
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)
    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc
def most(df, k):
    df = df['user'][df['value'] == k]
    x = df.value_count().head(10)
    return x
def name(df):
    for i in df["user"]:
        #unique_counts = df["user"].value_counts()
        unique_counts=df["user"].unique()
        l=len( unique_counts)
        one_third=l//3
        first_one_third=unique_counts[:one_third]


    return first_one_third
def namee(df):
    for i in df["user"]:
        u= df["user"].unique()
        l1 = len(u)
        one_third = l1 // 3
        middle_one_third = u[one_third:2*one_third]
    return middle_one_third
def names(df):
    for i in df["user"]:
        unique_names=df["user"].unique()
        t=len(unique_names)
        two_third=(2* t)//3
        remaining=unique_names[two_third:]
        return remaining

def most_common_words(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    def sentiment(d):
        if d["pos"] >= d["neg"] and d["pos"] >= d["nu"]:
            return 1
        if d["neg"] >= d["pos"] and d["neg"] >= d["nu"]:
            return -1
        if d["nu"] >= d["pos"] and d["nu"] >= d["neg"]:
            return 0
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    m = []
    for i in temp['message']:
        for x in i.split():
            m.append(x)
    df2 = pd.DataFrame({'message': m})
    sentiments = SentimentIntensityAnalyzer()
    df2["pos"] = [sentiments.polarity_scores(i)["pos"] for i in df2["message"]]  # Positive
    df2["neg"] = [sentiments.polarity_scores(i)["neg"] for i in df2["message"]]  # Negative
    df2["nu"] = [sentiments.polarity_scores(i)["neu"] for i in df2["message"]]
    df2['value'] = df2.apply(lambda row: sentiment(row), axis=1)
    for message in df2['message'][df2['value'] == k]:
        for word in message.lower().split():
            if word not in stop_words:
                    words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    if most_common_df.shape != (0,0):
        number = []
        for message in most_common_df[1]:
            number.append(str(message))
        most_common_df['number'] = number
        most_common_df.rename(columns={0: 'word'}, inplace=True)
        del most_common_df[1]
    return most_common_df
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    number = []
    text = []
    for emo in emoji_df[0]:
        text.append(emoji.demojize(emo))
    for message in emoji_df[1]:
        number.append(str(message))
    emoji_df['number'] = number
    emoji_df['emo'] = text
    emoji_df.rename(columns={0: 'emoji'}, inplace=True)
    positive = ['😂', '👍', '✌', '🔥', '🤣', '🙂', '✨', '❤', '😄', '😌', '🥳', '😎', '😁', '🫂', '😇', '🗿', '👌', '🙌',
                '😳', '😗', '😘']
    negitive = ['🥲', '😭', '🤦', '😔', '😤', '😑', '🤧', '😓', '😩', '😬', '😢', '🤨', '🤓', '🙄', '😥', '🥱', '😞',
                '😖', '💔', '😒']
    neutral = ['🥺', '♀', '🌝', '😅', '🫡', '🙏', '🙃', '🤔', '🌧', '♂', '🌚', '😶', '🤌', '⛈', '👀', '😈', '🌫', '🤷',
               '🤝', '😏', '🌩', '😒', '☔', '😝']
    p = 0
    neg = 0
    nu = 0
    for i in emojis:
        if i in positive:
            p+=1
        elif i in negitive:
            neg += 1
        else:
            nu += 1
    table = []
    for i in emoji_df['emoji']:
        if i in positive:
            table.append(1)
        elif i in negitive:
            table.append(-1)
        else:
            table.append(0)
    del emoji_df[1]
    emoji_df['value'] = table
    return emoji_df, p, neg, nu
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = (df.groupby(['year', 'month_num', 'month']).count()['message']*100/len(df)).reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def top_emoji(selected_user, emoji_df):
    positive_df = emoji_df['emoji'][emoji_df['value'] == 1]
    p_count = 0
    arr = []
    num = []
    string = ''
    x = min(3, int(positive_df.shape[0]))
    count = 0
    for i in positive_df:
        if count == x:
            break
        af = emoji_df[emoji_df['emoji'] == i]
        p_count += int(af['number'])
        string += i
        count += 1
    arr.append(string)
    num.append(p_count)
    negitive_df = emoji_df['emoji'][emoji_df['value'] == -1]
    string = ''
    x = min(3, int(negitive_df.shape[0]))
    n_count = 0
    count = 0
    for i in negitive_df:
        if count == x:
            break
        string += i
        af = emoji_df[emoji_df['emoji'] == i]
        n_count += int(af['number'])
        count += 1
    arr.append(string)
    num.append(n_count)
    neutral_df = emoji_df['emoji'][emoji_df['value'] == 0]
    string = ''
    x = min(3, int(neutral_df.shape[0]))
    nu_count = 0
    count = 0
    for i in neutral_df:
        if count == x:
            break
        af = emoji_df[emoji_df['emoji'] == i]
        nu_count += int(af['number'])
        string += i
        count += 1
    arr.append(string)
    num.append(nu_count)
    df = pd.DataFrame({'emoji': arr, 'count': num})
    return df, arr, num
def day_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        #df.head(200)
#def num_of_userss(df):
    #for i in df["user"]:
        #unique_counts = df["user"].value_counts()
    #return unique_counts

    #   timeline2=df[]

 #   timeline2=df["message"]/len(df)*100
    #a=df["D"].unique()[:100]
    #timeline = df.groupby("D")["message"].count().reset_index()
    #timeline=df["D"].unique()[:40]
    #timeline=df.groupby(df["D"].unique()[:50]).size().reset_index(name="MessageCount")
    #timeline = ((df.groupby(['a']).count()['message'])/len(df)*100).reset_index()
    #timeline=df['D'].value_counts().head(10)['message'])/len(df)*100).reset_index()
    #timeline = ((df['D'].value_counts().head(10)['message'] / len(df) * 100).reset_index())
    first_50_dates = df["D"].unique()[:5]
    filtered_df = df[df["D"].isin(first_50_dates)]
    timeline = filtered_df.groupby("D")["message"].count().reset_index()
    #timeline = ((df.groupby(['D'])count()['message']) / len(df) * 100).reset_index()
  #  timeline=df.head(1000).groupby('D').count()['message'].reset_index()
    #timeline=df.groupby('D')['message'].unique()
    return timeline

def summ(df, selected_user):
    df = df[df['user'] == selected_user]
    freqTable = dict()
    for i in df['message']:
        # print(i)
        i = i.split()
        for word in i:
            word = word.lower()
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
    if 'media' in freqTable:
        freqTable['media'] = 0
    if 'omitted' in freqTable:
        freqTable['omitted'] = 0
    sentenceValue = dict()
    for i in df['message']:
        for word, freq in freqTable.items():
            if word in i.lower():
                if i in sentenceValue:
                    sentenceValue[i] += freq
                else:
                    sentenceValue[i] = freq
    sumValues = 0
    for i in sentenceValue:
        sumValues += sentenceValue[i]
    summary = ''
    average = 0
    try:
        average += int(sumValues / len(sentenceValue))
    except:
        pass
    for i in df['message']:    
        if i in sentenceValue and sentenceValue[i] > 3 * average and len(i) > 20:
            summary += ' ' + i
    return summary