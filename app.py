import  streamlit as st
import preprocessor
st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file=st.sidebar.file_uploader('Choose file')

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    users=df['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0,'Overall')
    st.sidebar.selectbox('choose user',users)

    if st.sidebar.button('Show Analysis'):
         col1,col2,col3,col4=st.columns(4)

         with col1:
             st.header('Text messages')
