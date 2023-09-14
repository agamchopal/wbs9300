import nltk
nltk.download('punkt')  # For tokenization
nltk.download('stopwords')  # For stopwords
nltk.download('all')

nltk.download('vader_lexicon')
#import os

# Now you can use NLTK's functionalities
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import streamlit as st
import pandas as pd
import preprocessor
import Helper
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu
import spacy
nlp = spacy.load("en_core_web_md")
nltk.downloader.download('vader_lexicon')
st.sidebar.header('Whatsapp Bussiness Visualizer')
#st.sidebar.download_button(label="Download Dataset for testing")#,data=csv,file_name="wbs_data",mime="txt")
#st.sidebar.download_button(label="Download dataset for testing",data="""""",file_name="wbs_data",mime='text/csv')
f = open("wbs_data.txt", "rt",encoding="utf8")
#st.button(label, key=None, help=None, on_click=None, args=None, kwargs=None, *, type="secondary", disabled=False, use_container_width=False)
#if st.button("Download File"):
with open("wbs_data.txt", "r",encoding="utf8") as file:
    file_content = file.read()


def main():
    # Streamlit app title
    #st.title("Download dataset for testing")

    # Add a download button
    st.sidebar.download_button(
        label="Download Dataset for testing",
        data=file_content.encode('utf-8'),  # Encode the file content to bytes
        file_name="wbs_data.txt",  # Name of the downloaded file
        key="download-button"
    )


if __name__ == '__main__':
    main()


#st.download_button(label="Download",data="")

st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 375px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)

selected = option_menu(
    menu_title=None,
    options=["Home", "Dashboard"],
    icons=["house", "bar-chart-line-fill"],
    default_index=0,
    orientation="horizontal",
)
#st.download_button(label="download data set for testing",data="file")
#uploaded_file = st.sidebar.file_uploader("Choose a file")
uploaded_file1=st.sidebar.file_uploader("upload a .txt file",type=["txt"])
if uploaded_file1 is not None:
    if uploaded_file1.type == "text/plain":
        st.sidebar.success("File uploaded successfully")
    else:
        st.sidebar.warning("Upload a .txt file")

#st.sidebar.download_button(label="Download dataset for testing",data="csv",file_name="wbs_data",mime='text/csv')
#st.download_button(label="download data set for testing",data="file")
if selected == "Home":
    with st.sidebar:
        selected = option_menu(menu_title='',
                               options=['User', 'Timeline', 'Types of Words', "Emoji", 'Wordcloud', 'Types of Users'])
    # Main heading
    st.markdown("<h1 style='text-align: center; color: grey;'>Whatsapp Bussiness Visualizer</h1>",
                unsafe_allow_html=True)
    if uploaded_file1 is not None:
        bytes_data = uploaded_file1.getvalue()
        # yeh data byte data ka stream hai isse string mein convert krna pdeega
        data = bytes_data.decode('utf-8')
        # ab file ka data screen pe dikhne lagega
        df = preprocessor.preprocess(data)
        df2 = preprocessor.preprocess2(data)
        df3 = preprocessor.preprocess3(data)
        from nltk.sentiment.vader import SentimentIntensityAnalyzer


        def sentiment(d):
            if d["pos"] >= d["neg"] and d["pos"] >= d["nu"]:
                return 1
            if d["neg"] >= d["pos"] and d["neg"] >= d["nu"]:
                return -1
            if d["nu"] >= d["pos"] and d["nu"] >= d["neg"]:
                return 0


        # Object
        sentiments = SentimentIntensityAnalyzer()
        df["pos"] = [sentiments.polarity_scores(i)["pos"] for i in df["message"]]  # Positive
        df["neg"] = [sentiments.polarity_scores(i)["neg"] for i in df["message"]]  # Negative
        df["nu"] = [sentiments.polarity_scores(i)["neu"] for i in df["message"]]
        df['value'] = df.apply(lambda row: sentiment(row), axis=1)
        st.dataframe(df)

        # fetch unique user
        user_list = df['user'].unique().tolist()
        try:
            user_list.remove('group_notification')
        except:
            pass
        user_list.sort()
        user_list.insert(0, 'Overall')
        selected_user = st.sidebar.selectbox('show analysis wrt', user_list)
        if st.sidebar.button('Show Analysis'):
            num_messages, words, num_media_messages, num_of_links,unique_counts = Helper.fetch_stats(selected_user, df2)
            st.title('Top Statistics')
            col1, col2, col3, col4,col5 = st.columns(5)

            with col1:
                st.markdown("<h5 style='text-align: left; color = #26495C;border-style: solid;'>Total Messages</h5>",
                            unsafe_allow_html=True)
                st.title(num_messages)
            with col2:
                st.markdown("<h5 style='text-align: left; color = #26495C;border-style: solid;'>Total Words</h5>",
                            unsafe_allow_html=True)

                # st.markdown('<p class="big-font">Total  Words </p>', unsafe_allow_html=True)
                st.title(words)
            with col3:

                st.markdown("<h5 style='text-align: left; color = #26495C;border-style: solid;'>Media Messages</h5>",
                            unsafe_allow_html=True)
                st.title(num_media_messages)
            with col4:
                st.markdown("<h5 style='text-align: left; color = #26495C;border-style: solid;'>Links Shared</h5>",
                            unsafe_allow_html=True)
                st.title(num_of_links)
            with col5:
                st.markdown("<h5 style='text-align: left; color = #26495C;border-style: solid;'>Number of users</h5>",
                            unsafe_allow_html=True)
                st.title(unique_counts)

            if selected == 'Timeline':
                col1, = st.columns(1)
                with col1:
                    timeline = Helper.monthly_timeline(selected_user, df)
                    fig = px.line(timeline, x='time', y='message', title='User Activity Monthly',
                                  width=350, height=400)
                    fig.update_layout(
                        title="User Monthwise activity",
                        xaxis_title="Months",
                        yaxis_title="Number of messages",

                    )

                    fig
                # daily
                col1,=st.columns(1)
                with col1:
                    timeline= Helper.day_timeline(selected_user, df)

                    fig = px.bar(timeline, x='D', y='message', title='User Activity DateWise',
                                  width=400, height=400)
                    fig.update_layout(
                        title="User Datewisewise activity",
                        xaxis_title="Dates",
                        yaxis_title="Number of messages",

                    )
                    fig


            # finding the busiest users in the group (Group - level)
            if selected == 'User':
                if selected_user == 'Overall':
                    st.write("<h3 style='text-align: center; font-size: 16px;'>Most Busy Users</h3>", unsafe_allow_html=True)
                    #st.title('Most Busy Users')
                    x, new_df = Helper.most_busy_users(df)
                    fig, ax = plt.subplots()
                    # col1, col2 = st.columns(2)
                    names = new_df['names']
                    percentage = new_df['percentage']
                    fig = px.bar(new_df, x=names, y=percentage, color=names)
                    fig
            if selected == "Names":
                with col1:
                     unique_counts =Helper.name(df)
                     unique_counts
            if selected=="Download Dataset":
                with col1:
                    content=Helper.generate_text_file_content()
                    content


            # WordCloud
            if selected == 'Wordcloud':
                df_wc = Helper.create_wordcloud(selected_user, df)
                fig, ax = plt.subplots()
                plt.imshow(df_wc)
                st.pyplot(fig)
            if selected == "Types of Users":
                # Most Positive, Negitive, Neutral user...
                if selected_user == 'Overall':
                    #    col1, col2, col3 = st.columns(3)
                    #    with col1:
                    st.markdown("<h3 style='text-align: center; color: green;'>Most Positive Users</h3>",
                                unsafe_allow_html=True)
                    af = df['user'][df['value'] == 1]
                    x = af.value_counts()

                    fig = px.bar(af, y=x.values, x=x.index, color=x)
                    fig
                    #    with col2:
                    st.markdown("<h3 style='text-align: center; color: blue;'>Most Neutral Users</h3>",
                                unsafe_allow_html=True)
                    af = df['user'][df['value'] == 0]
                    x = af.value_counts()
                    fig = px.bar(af, y=x.values, x=x.index, color=x)
                    fig
                    #    with col3:
                    st.markdown("<h3 style='text-align: center; color: red;'>Most Negative Users</h3>",
                                unsafe_allow_html=True)
                    af = df['user'][df['value'] == -1]
                    x = af.value_counts()
                    fig = px.bar(af, y=x.values, x=x.index, color=x)
                    fig
            # most common words
            if selected == 'Types of Words':
                # col1, col2, col3 = st.columns(3)

                # with col1:
                try:
                    st.markdown("<h3 style='text-align: center; color: green;'>Most Positive Words</h3>",
                                unsafe_allow_html=True)
                    most_common_df = Helper.most_common_words(selected_user, df3, 1)
                    fig, ax = plt.subplots()
                    word = most_common_df['word']
                    number = most_common_df['number']
                    fig = px.bar(most_common_df, y=number, x=word, color=word)
                    fig
                except:
                    pass
                # with col2:
                try:
                    st.markdown("<h3 style='text-align: center; color: blue;'>Most Neutral words</h3>",
                                unsafe_allow_html=True)
                    most_common_df = Helper.most_common_words(selected_user, df3, 0)
                    word = most_common_df['word']
                    number = most_common_df['number']
                    fig = px.bar(most_common_df, y=number, x=word, color=word)
                    fig
                except:
                    pass
                # with col3:
                try:
                    st.markdown("<h3 style='text-align: center; color: red;'>Most Negative words</h3>",
                                unsafe_allow_html=True)
                    most_common_df = Helper.most_common_words(selected_user, df3, -1)
                    fig, ax = plt.subplots()
                    word = most_common_df['word']
                    number = most_common_df['number']
                    fig = px.bar(most_common_df, y=number, x=word, color=word)
                    fig
                except:
                    pass
            # emoji analysis
            if selected == 'Emoji':
                try:
                    emoji_df, p, neg, nu = Helper.emoji_helper(selected_user, df)
                    st.write(
                        "<h3 style='text-align: left;'>Number of times each emoji used</h3>",
                        # font-size: 16px;'>User 1</h1>",
                        unsafe_allow_html=True)
                    #st.title("Number of times each Emoji used")
                    col1,  = st.columns(1)
                    with col1:
                        try:
                            st.dataframe(emoji_df)
                        except:
                            pass

                    col1,=st.columns(1)
                    with col1:
                        try:
                            st.write("<h3 style='text-align: left;'>Pie chart showing the percentage of positive,neutral and negative sentiments</h3>", #font-size: 16px;'>User 1</h1>",
                                     unsafe_allow_html=True)
                            #st.title("Pie chart showing percentage of positive , negative and neutral sentiments ")
                            top_emoji_df, top_emoji, num = Helper.top_emoji(selected_user, emoji_df)
                            arr = [int((p / (p + neg + nu)) * 100), int((neg / (p + neg + nu)) * 100),
                                   int((nu / (p + neg + nu)) * 100)]
                            af = pd.DataFrame({'sentiment': ['positive', 'negative', 'neutral'], 'percentage': arr,
                                               'top_emoji': top_emoji})
                            fig = px.pie(af, values='percentage', names='sentiment', hover_data=['top_emoji'],
                                         labels={'top_emoji': 'top_emoji'}, color_discrete_sequence=[ '#ff1a1a', '#33cc33', '#4d79ff'])#negative,positive,neutral
                            fig.update_traces(textposition='inside', textinfo='percent', pull=0.1)
                            fig
                        except:
                            try:
                                arr = [int((p / (p + neg + nu)) * 100), int((neg / (p + neg + nu)) * 100),
                                       int((nu / (p + neg + nu)) * 100)]
                                af = pd.DataFrame({'sentiment': ['positive', 'negative', 'neutral'], 'percentage': arr})
                                fig = px.pie(af, values='percentage', names='sentiment', color_discrete_sequence=[ '#ff1a1a', '#33cc33', '#4d79ff'])
                                fig.update_traces(textposition='inside', textinfo='percent', pull=0.1)
                                fig
                            except:
                                pass

                except:
                    pass








if selected == "Dashboard":




    st.write(
        "<h2 style='text-align: center;'>User to User comparision</h2>",
        # font-size: 16px;'>User 1</h1>",
        unsafe_allow_html=True)
    st.write(
        "<h4 style='text-align: center;'>Instructions</h4",
        # font-size: 16px;'>User 1</h1>",
        unsafe_allow_html=True)
    st.write(
        "<h5 style='text-align: left;'>1: Write (name,name of first user,name of second user)for Pie-chart,Scatter plot,Words.</h5",
        # font-size: 16px;'>User 1</h1>",
        unsafe_allow_html=True)
    st.write(
        "<h5 style='text-align: left;'>2: Write (user,name of first user,name of second user) for Similar users and text summary .</h5",

        # font-size: 16px;'>User 1</h1>",
        unsafe_allow_html=True)
    try:

        bytes_data = uploaded_file1.getvalue()
        # yeh data byte data ka stream hai isse string mein convert krna pdeega
        data = bytes_data.decode('utf-8')
        # ab file ka data screen pe dikhne lagega
        df = preprocessor.preprocess(data)
        st.write(
            "<h3 style='text-align: center;'>Available Users</h3>",
            # font-size: 16px;'>User 1</h1>",
            unsafe_allow_html=True)
        # st.title("Available Users")

        col1, col2, col3 = st.columns(3)

        with col1:
            first_one_third = Helper.name(df)
            first_one_third

        with col2:
            middle_one_third = Helper.namee(df)
            middle_one_third
        with col3:
            remaining = Helper.names(df)
            remaining
    except:
        pass






    import openai
    from streamlit_chat import message

    openai.api_key = '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'


    # This function uses the OpenAI Completion API to generate a
    # response based on the given prompt. The temperature parameter controls
    # the randomness of the generated response. A higher temperature will result
    # in more random responses,
    # while a lower temperature will result in more predictable responses.
    def generate_response(prompt):
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = completions.choices[0].text
        return message






    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []


    def get_text():
        input_text = st.text_input("", placeholder="user/name,name of 1st user,name of 2nd user", key="input")
        return input_text


    user_input = get_text()
    if user_input[:4] == 'user':
        try:
            # Main heading
            a, b, c = user_input.split(",")
            selected_user = [b, c]

            if uploaded_file1 is not None:
                bytes_data = uploaded_file1.getvalue()
                # yeh data byte data ka stream hai isse string mein convert krna pdeega
                data = bytes_data.decode('utf-8')
                # ab file ka data screen pe dikhne lagega
                df = preprocessor.preprocess(data)
                from nltk.sentiment.vader import SentimentIntensityAnalyzer




                def sentiment(d):
                    if d["pos"] >= d["neg"] and d["pos"] >= d["nu"]:
                        return 1
                    if d["neg"] >= d["pos"] and d["neg"] >= d["nu"]:
                        return -1
                    if d["nu"] >= d["pos"] and d["nu"] >= d["neg"]:
                        return 0


                # Object
                sentiments = SentimentIntensityAnalyzer()
                df["pos"] = [sentiments.polarity_scores(i)["pos"] for i in df["message"]]  # Positive
                df["neg"] = [sentiments.polarity_scores(i)["neg"] for i in df["message"]]  # Negative
                df["nu"] = [sentiments.polarity_scores(i)["neu"] for i in df["message"]]
                df['value'] = df.apply(lambda row: sentiment(row), axis=1)


                def sentiment2(d):
                    return d["pos"] - d["neg"]


                df['score'] = df.apply(lambda row: sentiment2(row), axis=1)









            if not (df["user"].isin([b, c])).any():
                st.warning("Users not available")
            elif not (df["user"].isin([b])).any():
                st.warning("First user is not available")
            elif not (df["user"].isin([c])).any():
                st.warning("Second user is not available")



            else:
                col1, col2 = st.columns(2)
                st.write(
                    "<h3 style='text-align: center;'>Pie Chart showing the percentage of positive,negative and neutral sentiments</h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)
                with col1:


                    selecte_user = list(df["user"])
                    st.header(selected_user[0])
                    #st.markdown("<h1 style='font-size: 48px;'>(selected_user[0]</h1)>", unsafe_allow_html=True)


                    for i in df["user"].unique():
                        a = df[df['user'] == selected_user[0]]["pos"].sum()
                        b = df[df["user"] == selected_user[0]]["neg"].sum()
                        c = df[df["user"] == selected_user[0]]["nu"].sum()
                        arr = [((a / (a + b + c)) * 100), ((b / (a + b + c)) * 100),
                               ((c / (a + b + c)) * 100)]
                        af = pd.DataFrame({'sentiment': ['positive', 'negative', 'neutral'], 'percentage': arr})
                        if  i == selecte_user[0]:
                            fig = px.pie(af, values='percentage', names='sentiment',
                                         color_discrete_sequence=['#4d79ff', '#33cc33','#ff1a1a' ])
                            #fig.update_traces(textposition='inside', textinfo='percent', pull=0.1)
                            fig.update_layout(legend=dict(orientation='h',x=0,y=0.1))
                            fig.update_traces(domain=dict(x=[0, 0.4]))

                            #st.markdown("""
                                                        #<style>
                                                        #.#chart-container {
                                                            #float: left;
                                                        #}
                                                        #</style>
                                                        #""", unsafe_allow_html=True)
                            #st.plotly_chart(fig, use_container_width=True, key='my_chart', className='chart-container')
                            fig
            #except:
                #pass

                with col2:
                    #st.write(f"#{}")
                    selecte_user = list(df["user"])
                    st.header(selected_user[1])


                    for i in df["user"].unique():
                        a = df[df['user'] ==selected_user[1] ]["pos"].sum()
                        b = df[df["user"] == selected_user[1]]["neg"].sum()
                        c = df[df["user"] == selected_user[1]]["nu"].sum()
                        arr = [((a / (a + b + c)) * 100), ((b / (a + b + c)) * 100),
                               ((c / (a + b + c)) * 100)]
                        af = pd.DataFrame({'sentiment': ['positive', 'negative', 'neutral'], 'percentage': arr})
                        if i == selecte_user[1]:
                            fig = px.pie(af, values='percentage', names='sentiment',
                                         color_discrete_sequence=['#4d79ff', '#33cc33','#ff1a1a' ]);
                            #{}
                            #fig.update_traces(textposition='inside', textinfo='percent', pull=0.1)
                            fig.update_layout(legend=dict(orientation='h', x=0, y=0.1))
                            fig.update_traces(domain=dict(x=[0,0.4]))



                            fig
                col1, col2 = st.columns(2)
                st.write(
                    "<h3 style='text-align: center;'>Scatter Plot shows spread of Positive,Negative,Neutral Words</h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)
                with col1:
                    selecte_user = list(df["user"])
                    st.header(selected_user[0])

                    #df["user"] = selecte_user[0]
                    # selecte_user = df["user"]
                    for i in df["user"].unique():
                        a = df.loc[df['user'] == selected_user[0]]["pos"].tolist()

                        b = df.loc[df["user"] == selected_user[0]]["neg"].tolist()
                        c = df.loc[df["user"] == selected_user[0]]["nu"].tolist()
                        # arr = [((a / (a + b + c)) * 100), ((b / (a + b + c)) * 100),
                        # ((c / (a + b + c)) * 100)]
                        af1 = pd.DataFrame({'Positive': a, 'Neutral': b, 'Negative': c})
                        if i == selecte_user[0]:
                            fig = px.scatter(af1)
                            fig.update_layout(
                                autosize=False,
                                width=500,  # Set the total width of the figure
                                height=400,  # Set the total height of the figure
                                margin=dict(l=0, r=0, t=30, b=0),  # Adjust margins as needed
                                paper_bgcolor='white',  # Set background color
                            )

                            #fig.update_layout(margin=dict(l=-1))
                            #fig.update_traces(domain=dict(x=[0, 0.4]))
                            #fig.update_xaxes(range=[min(x_data),max(x_data)*0.8])
                            # , values='percentage', names='sentiment',
                            # color_discrete_sequence=['#ff1a1a', '#33cc33', '#4d79ff'])
                            # fig.update_traces(textposition='inside', textinfo='percent', pull=0.1)
                            fig
                with col2:
                    selecte_user = list(df["user"])
                    st.header(selected_user[1])
                    #df["user"] = selecte_user[1]
                    # selecte_user = df["user"]
                    for i in df["user"].unique():
                        a3 = df.loc[df['user'] == selected_user[1]]["pos"].tolist()
                        b3 = df.loc[df["user"] == selected_user[1]]["neg"].tolist()
                        c3 = df.loc[df["user"] == selected_user[1]]["nu"].tolist()
                        # arr = [((a / (a + b + c)) * 100), ((b / (a + b + c)) * 100),
                        # ((c / (a + b + c)) * 100)]
                        af2 = pd.DataFrame({'Positive': a3, 'Neutral': b3, 'Negative': c3})
                        if i == selecte_user[1]:
                            fig = px.scatter(af2)
                            fig.update_layout(
                                autosize=False,
                                width=450,  # Set the total width of the figure
                                height=400,  # Set the total height of the figure
                                margin=dict(l=0, r=0, t=30, b=0),  # Adjust margins as needed
                                paper_bgcolor='white',  # Set background color
                            )
                            # , values='percentage', names='sentiment',
                            # color_discrete_sequence=['#ff1a1a', '#33cc33', '#4d79ff'])
                            # fig.update_traces(textposition='inside', textinfo='percent', pull=0.1)
                            fig









                col1, col2 = st.columns(2)

                with col1:
                    selecte_user = list(df["user"])
                    st.header(selected_user[0])
                    df_wc = Helper.create_wordcloud(selecte_user[0], df)
                    fig, ax = plt.subplots()
                    plt.imshow(df_wc)
                    st.pyplot(fig)
                with col2:
                    selecte_user = list(df["user"])
                    st.header(selected_user[1])
                    df_wc = Helper.create_wordcloud(selecte_user[1], df)
                    fig, ax = plt.subplots()
                    plt.imshow(df_wc)
                    st.pyplot(fig)
                st.write(
                    "<h3 style='text-align: center;'>Word Cloud</h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)
                #st.title('Most Positive Words')
                col1, col2 = st.columns(2)
                with col1:
                    selecte_user = list(df["user"])
                    st.header(selected_user[0])
                    try:
                        most_common_df = Helper.most_common_words(selecte_user[0], df, 1)
                        fig, ax = plt.subplots()
                        word = most_common_df['word']
                        number = most_common_df['number']
                        fig = px.bar(most_common_df, y=number, x=word, color=word, width=350,height=350)
                        fig
                    except:
                        pass
                with col2:
                    selecte_user = list(df["user"])
                    st.header(selected_user[1])
                    try:
                        most_common_df = Helper.most_common_words(selecte_user[1], df, 1)
                        word = most_common_df['word']
                        number = most_common_df['number']
                        fig = px.bar(most_common_df, y=number, x=word, color=word, width=350,height=350)
                        fig
                    except:
                        pass
                #st.title('Most Negative Words')
                st.write(
                    "<h3 style='text-align: center;'>Most Positive Words</h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    selecte_user = list(df["user"])
                    st.header(selected_user[0])
                    try:
                        most_common_df = Helper.most_common_words(selecte_user[0], df, -1)
                        fig, ax = plt.subplots()
                        word = most_common_df['word']
                        number = most_common_df['number']
                        fig = px.bar(most_common_df, y=number, x=word, color=word, width=350, height=350)
                        fig
                    except:
                        pass
                with col2:
                    selecte_user = list(df["user"])
                    st.header(selected_user[1])
                    try:
                        most_common_df = Helper.most_common_words(selecte_user[1], df, -1)
                        word = most_common_df['word']
                        number = most_common_df['number']
                        fig = px.bar(most_common_df, y=number, x=word, color=word, width=350, height=350)
                        fig
                    except:
                        pass
                st.write(
                    "<h3 style='text-align: center;'>Most Negative Words</h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)

                #st.write(
                    #"<h3 style='text-align: center;'>Similar Users and Summary</h3>",
                    # font-size: 16px;'>User 1</h1>",
                    #unsafe_allow_html=True)
                #st.title('Similar Users and Text Summary')
                #col1, col2 = st.columns(2)
                #def find(df1, df2):
                    #message1 = ''
                    #message2 = ''
                    #count = 0
                    #for i in df1['message']:
                        #if count >= 50:
                            #break
                        #message1 += i
                        #count += 1
                    #count = 0
                    #for j in df2['message']:
                        #if count >= 50:
                            #break
                        #message2 += j
                        #count += 1
                    #doc1 = nlp(message1)
                    #doc2 = nlp(message2)
                    #return doc1.similarity(doc2)
                #user_ = df.user.unique()

                #with col1:
                    #score = []
                    #this_set = set()
                    #df1 = df[df['user'] == selecte_user[0]]
                    #for j in user_:
                        #if user_[0] != j:
                            #df2 = df[df['user'] == j]
                            #score.append((find(df1, df2), j))
                    #score.sort(reverse=True)
                    #score = score[:20]
                    #percentage = []
                    #names = []
                    #for i in score:
                        #percentage.append(i[0] * 100)
                        #names.append(i[1])
                    #df3 = pd.DataFrame({
                        #'name': names,
                        #'percent': percentage
                    #})
                    #fig = px.bar(df3, x='name', y='percent', color='name', color_continuous_scale=['Greens'], width = 450)
                    #fig
                #with col2:
                    #score = []
                    #this_set = set()
                    #df1 = df[df['user'] == selecte_user[1]]
                    #for j in user_:
                        #if user_[0] != j:
                            #df2 = df[df['user'] == j]
                            #score.append((find(df1, df2), j))
                    #score.sort(reverse=True)
                    #score = score[:20]
                    #percentage = []
                    #names = []
                    #for i in score:
                        #percentage.append(i[0] * 100)
                        #names.append(i[1])
                    #df3 = pd.DataFrame({
                        #'name': names,
                        #'percent': percentage
                    #})
                    #fig = px.bar(df3, x='name', y='percent', color='name', color_continuous_scale=['Greens'], width = 450)
                    #fig

                #with col1:
                    #summary = Helper.summ(df, selecte_user[0])
                    #st.markdown(summary)
                #with col2:
                    #summary = Helper.summ(df, selecte_user[1])
                    #st.markdown(summary)
                #col1,col2=st.columns(2)
                #with col1:
                    #for i in df11[user].unique()[:10]:
                        #a1=df11[df11["user"]==selecte_user[0]]["pos"].values()
                        #b1=df11[df11["user"]==selecte_user[0]]["neg"].values()
                        #c1=df11[df11['user']==selecte_user[0]]["nu"].values()
                        #df101=pd.DataFrame({'c11':a1,'b11':b1,'c3':c1})
                        #fig=px.scatter(df101,x='s',y='w')
            #else:
                #st.warning("Invalid Users")

                #except:
                    #pass
            #try:
             #if b not in df["user"] and c  not in df["user"]:
                 #st.warning("Enter Valid users")
            #except:
                #pass
        #else:
            #else:
                #st.warning("O")
        except:
            pass
    #elif user_input = get_text()
    if  user_input[:4] == 'name':
        try:
            # Main heading
            a, b, c = user_input.split(",")
            selected_user = [b, c]

            if uploaded_file1 is not None:
                bytes_data = uploaded_file1.getvalue()
                # yeh data byte data ka stream hai isse string mein convert krna pdeega
                data = bytes_data.decode('utf-8')
                # ab file ka data screen pe dikhne lagega
                df = preprocessor.preprocess(data)
                from nltk.sentiment.vader import SentimentIntensityAnalyzer


                def sentiment(d):
                    if d["pos"] >= d["neg"] and d["pos"] >= d["nu"]:
                        return 1
                    if d["neg"] >= d["pos"] and d["neg"] >= d["nu"]:
                        return -1
                    if d["nu"] >= d["pos"] and d["nu"] >= d["neg"]:
                        return 0


                # Object
                sentiments = SentimentIntensityAnalyzer()
                df["pos"] = [sentiments.polarity_scores(i)["pos"] for i in df["message"]]  # Positive
                df["neg"] = [sentiments.polarity_scores(i)["neg"] for i in df["message"]]  # Negative
                df["nu"] = [sentiments.polarity_scores(i)["neu"] for i in df["message"]]
                df['value'] = df.apply(lambda row: sentiment(row), axis=1)


                def sentiment2(d):
                    return d["pos"] - d["neg"]


                df['score'] = df.apply(lambda row: sentiment2(row), axis=1)


        except:
            pass






            col1, col2 = st.columns(2)

        try:
            def find(df1, df2):
                message1 = ''
                message2 = ''
                count = 0
                for i in df1['message']:
                    if count >= 50:
                        break
                    message1 += i
                    count += 1
                count = 0
                for j in df2['message']:
                    if count >= 50:
                        break
                    message2 += j
                    count += 1
                doc1 = nlp(message1)
                doc2 = nlp(message2)
                return doc1.similarity(doc2)


            user_ = df.user.unique()
        except:
            pass
        try:

            with col1:
                selecte_user = list(df["user"])
                st.header(selected_user[0])





                score = []
                this_set = set()
                df1 = df[df['user'] == selecte_user[0]]
                for j in user_:
                    if user_[0] != j:
                        df2 = df[df['user'] == j]
                        score.append((find(df1, df2), j))
                score.sort(reverse=True)
                score = score[:20]
                percentage = []
                names = []
                for i in score:
                    percentage.append(i[0] * 100)
                    names.append(i[1])
                df3 = pd.DataFrame({
                    'name': names,
                    'percent': percentage
                })
                fig = px.bar(df3, x='name', y='percent', color='name', color_continuous_scale=['Greens'], width=450)
                fig
                st.write(
                    "<h3 style='text-align: center;'>Similar users </h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)

        except:
            pass
        try:
            with col2:
                selecte_user = list(df["user"])
                st.header(selected_user[1])

                score = []
                this_set = set()
                df1 = df[df['user'] == selecte_user[1]]
                for j in user_:
                    if user_[0] != j:
                        df2 = df[df['user'] == j]
                        score.append((find(df1, df2), j))
                score.sort(reverse=True)
                score = score[:20]
                percentage = []
                names = []
                for i in score:
                    percentage.append(i[0] * 100)
                    names.append(i[1])
                df3 = pd.DataFrame({
                    'name': names,
                    'percent': percentage
                })
                fig = px.bar(df3, x='name', y='percent', color='name', color_continuous_scale=['Greens'], width=450)
                fig
                st.write(
                    "<h3 style='text-align: center;'>Similar users </h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)

            with col1:
                summary = Helper.summ(df, selecte_user[0])
                st.markdown(summary)
                st.write(
                    "<h3 style='text-align: center;'>Summary </h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)

            with col2:
                summary = Helper.summ(df, selecte_user[1])
                st.markdown(summary)
                st.write(
                    "<h3 style='text-align: center;'>Summary </h3>",
                    # font-size: 16px;'>User 1</h1>",
                    unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                for i in df11[user].unique()[:10]:
                    a1 = df11[df11["user"] == selecte_user[0]]["pos"].values()
                    b1 = df11[df11["user"] == selecte_user[0]]["neg"].values()
                    c1 = df11[df11['user'] == selecte_user[0]]["nu"].values()
                    df101 = pd.DataFrame({'c11': a1, 'b11': b1, 'c3': c1})
                    fig = px.scatter(df101, x='s', y='w')
                    fig

        except:
            pass

