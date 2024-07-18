import streamlit as st
import pandas as pd
import boto3

st.title("Sample App")

user_input = st.text_input(label='User ID', placeholder="Enter User ID")

personalize_runtime = boto3.client('personalize-runtime')
campaign_arn = 'arn:aws:personalize:us-east-2:654654468950:campaign/crs-campaign'
user_interactions_file = './Dataset/user_interactions(new).csv'  # Update this path
users_file = './Dataset/users.csv'

if user_input:
    try:
        user_interactions_df = pd.read_csv(user_interactions_file)
        users_df = pd.read_csv(users_file)
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        user_interactions_df = pd.DataFrame()  # Create an empty DataFrame in case of error
        users_df = pd.DataFrame()  # Create an empty DataFrame in case of error
    except pd.errors.EmptyDataError as e:
        st.error(f"No data: {e}")
        user_interactions_df = pd.DataFrame()  # Create an empty DataFrame in case of error
        users_df = pd.DataFrame()  # Create an empty DataFrame in case of error
    except pd.errors.ParserError as e:
        st.error(f"Parse error: {e}")
        user_interactions_df = pd.DataFrame()  # Create an empty DataFrame in case of error
        users_df = pd.DataFrame()  # Create an empty DataFrame in case of error
    except Exception as e:
        st.error(f"Error loading CSV files: {e}")
        user_interactions_df = pd.DataFrame()  # Create an empty DataFrame in case of error
        users_df = pd.DataFrame()
        
    response = personalize_runtime.get_recommendations(
        campaignArn=campaign_arn,
        userId=user_input,
        numResults=10
    )

    recommendations = response['itemList']
    recommended_items = [{'ITEM_ID': item['itemId'], 'SCORE': item['score']} for item in recommendations]

    recommendations_df = pd.DataFrame(recommended_items)

    # Add USER_ID column to recommendations DataFrame for merging
    recommendations_df['USER_ID'] = user_input

    # Merge recommendations with user details
    merged_df = pd.merge(recommendations_df, users_df, on='USER_ID', how='left')

    # Merge with user interactions to include EVENT_TYPE and LOCATION
    final_df = pd.merge(merged_df, user_interactions_df[['USER_ID', 'ITEM_ID', 'EVENT_TYPE', 'LOCATION']], on=['USER_ID', 'ITEM_ID'], how='left')

    # Selecting and st.erroring the desired columns
    if not final_df.empty:
        result_df = final_df[['USER_ID', 'AGE', 'GENDER', 'JOB_PREFERENCES', 'MEMBERSHIP_LEVEL', 'PREFERRED_JOB_LOCATIONS', 'ITEM_ID', 'SCORE', 'EVENT_TYPE', 'LOCATION']]
        limited_result_df = result_df.head(5)  # Limit to top 5 rows
        st.dataframe(limited_result_df)     
    else:
        st.error("No matching data found in the merged DataFrame.")