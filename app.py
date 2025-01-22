import  streamlit as st
import preprocessor,helper
import  matplotlib.pyplot as plt


st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file=st.sidebar.file_uploader('Choose file')

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)

    users=df['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0,'Overall')
    selected_user=st.sidebar.selectbox('choose user',users)

    if st.sidebar.button('Show Analysis'):
         st.title('Top Statistics')
         num_messages,num_words,num_media_msg,num_url_msg=helper.fetch_status(selected_user,df)
         col1,col2,col3,col4=st.columns(4)

         with col1:
             st.header('Text messages')
             st.title(num_messages)

         with col2:
             st.header('No of Words')
             st.title(num_words)

         with col3:
             st.header('No of Media')
             st.title(num_media_msg)

         with col4:
             st.header('No of Urls')
             st.title(num_url_msg)

         # monthly timeline
         st.title('Monthly Timeline')
         timeline=helper.monthly_timeline(selected_user,df)

         fig,ax=plt.subplots(figsize=(6, 4))

         ax.plot(timeline['time'],timeline['message'],color='green')
         plt.xticks(rotation='vertical')
         st.pyplot(fig)

         # daily timeline

         st.title('Daily Timeline')
         daily_timelines=helper.daily_timeline(selected_user,df)
         fig,ax=plt.subplots()
         ax.plot(daily_timelines['date_only'],daily_timelines['message'],color='black')
         plt.xticks(rotation='vertical')
         st.pyplot(fig)

         # activity map

         st.title('Activity Map')
         col1,col2=st.columns(2)

         with col1:
             st.header('Most busy day')
             busy_day=helper.weekly_activity(selected_user,df)
             fig,ax=plt.subplots()
             ax.bar(busy_day.index,busy_day.values,color='orange')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)

         with col2:
             st.header('Most busy month')
             busy_month=helper.monthly_activity(selected_user,df)
             fig,ax=plt.subplots()
             ax.bar(busy_month.index,busy_month.values,color='green')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)



         # find the busiest member
         if selected_user=='Overall':
             st.title("Most Busy User")
             X,new_df=helper.fetch_busy_user(df)
             fig,ax=plt.subplots()


             col5,col6=st.columns(2)

             with col5:
                 ax.bar(X.index, X.values)
                 plt.xticks(rotation='vertical')
                 st.pyplot(fig)

             with col6:
                 st.dataframe(new_df)

         # WordCloud
         st.title('WordCloud')
         df_wc=helper.crearte_word_cloud(selected_user,df)
         fig,ax=plt.subplots()
         ax.imshow(df_wc)
         st.pyplot(fig)

         # Most common words
         most_common_df=helper.most_common_word(selected_user,df)

         fig,ax=plt.subplots()
         ax.bar(most_common_df[0],most_common_df[1])
         plt.xticks(rotation='vertical')
         st.title('Most Common Words')
         st.pyplot(fig)

         # Emoji analysis
         emoji_df=helper.fetch_emoji(selected_user,df)
         st.title('Emoji Analysis')
         col1,col2=st.columns(2)
         with col1:
            st.dataframe(emoji_df)

         with col2:
             fig,ax=plt.subplots()
             ax.pie(emoji_df['count'].head(),labels=emoji_df['emoji'].head(),autopct='%1.1f%%')
             st.pyplot(fig)


