import streamlit as st
import pandas as pd
from src.pd_functions import *
from src.utils import validate_csv_file

# Constants
RESULTS_PATH = 'data/results_housing_class.csv'

def main():

    st.title('🏠 Housing Classification App 🏠' )
    st.markdown('Welcome to the housing classification app. Please enter your first name below, then upload your results file to check your accuracy and see the leaderboard.')
    st.markdown('🤖 Good Luck and remember it is just for fun!! 🤖')
    st.markdown('🏋🏻‍♂️ Remember to fit your model on (X, y) before you predict. 🏋🏻‍♂️')
    participant_name = get_participant_name()

    if participant_name:
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

        if uploaded_file:
            if validate_csv_file(uploaded_file):
                process_uploaded_file(uploaded_file, participant_name)
            else:
                st.error('The uploaded file is not a valid CSV file. Please upload a valid CSV file.')
        else:
            st.warning('Please upload a file.')
    else:
        st.warning('Please enter a participant name.')

    display_leaderboard()

def get_participant_name():
    text_input_container = st.empty()
    participant_name = text_input_container.text_input(
        "Introduce participant name: ",
        key="text_input"
    )
    return participant_name

def process_uploaded_file(uploaded_file, participant_name):
    if validate_csv_file(uploaded_file):
        try:
            uploaded_file.seek(0)  # Reset file pointer to the beginning
            test = get_ready_test(RESULTS_PATH, uploaded_file)
            participant_results = get_accuracy(RESULTS_PATH, test)

            st.success('Dataframe uploaded successfully!')
            display_participant_results(participant_results)
            update_and_plot_submissions(participant_results, participant_name)
        except Exception as e:
            st.error(f'The file could not be processed. Error: {e}')
    else:
        st.error('The file has a wrong format, please, review it and ensure it contains the required columns.')



def display_participant_results(participant_results):
    st.title('Participant results')
    st.dataframe(participant_results)

def update_and_plot_submissions(participant_results, participant_name):
    try:
        update_submissions(participant_results)
        plot_submissions(participant_name)
    except:
        participant_results.to_pickle('files_to_update/submissions.pkl')

def display_leaderboard():
    try:
        show_leaderboard()
    except:
        st.write("There is no submission.")

if __name__ == "__main__":
    main()
