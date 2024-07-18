import streamlit as st
import pandas as pd
import boto3

st.title("Content Recommendation App")

user_input = st.text_input(label='User ID', placeholder="Enter User ID")


personalize_runtime = boto3.client('personalize-runtime',region_name='us-east-2')
campaign_arn = 'arn:aws:personalize:us-east-2:654654468950:campaign/crs-campaign'


user_interactions_file = './Dataset/user_interactions(new).csv'  
users_file = './Dataset/users.csv' 

if user_input:
    try:
        
        user_interactions_df = pd.read_csv(user_interactions_file)
        users_df = pd.read_csv(users_file)
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        user_interactions_df = pd.DataFrame()  
        users_df = pd.DataFrame() 
    except pd.errors.EmptyDataError as e:
        st.error(f"No data: {e}")
        user_interactions_df = pd.DataFrame() 
        users_df = pd.DataFrame() 
    except pd.errors.ParserError as e:
        st.error(f"Parse error: {e}")
        user_interactions_df = pd.DataFrame()  
        users_df = pd.DataFrame() 
    except Exception as e:
        st.error(f"Error loading CSV files: {e}")
        user_interactions_df = pd.DataFrame()  
        users_df = pd.DataFrame() 

   
    response = personalize_runtime.get_recommendations(
        campaignArn=campaign_arn,
        userId=user_input,
        numResults=10
    )

    recommendations = response['itemList']
    recommended_items = [{'ITEM_ID': item['itemId'], 'SCORE': item['score']} for item in recommendations]

    recommendations_df = pd.DataFrame(recommended_items)
    recommendations_df['USER_ID'] = user_input

    merged_df = pd.merge(recommendations_df, users_df, on='USER_ID', how='left')

   
    user_info = users_df[users_df['USER_ID'] == user_input]
    st.subheader("User Information")
    st.dataframe(user_info)

    
    if not recommendations_df.empty:
        limited_recommendations_df = recommendations_df.head(5)  
        st.subheader("Personalized Recommendations")
        st.dataframe(limited_recommendations_df[['USER_ID', 'ITEM_ID', 'SCORE']])
    else:
        st.error("No recommendations found.")
