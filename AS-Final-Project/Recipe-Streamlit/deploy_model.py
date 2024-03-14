###############################
# This program lets you       #
# - Create a dashboard        #
# - Evevry dashboard page is  #
# created in a separate file  #
###############################

# Python libraries
import streamlit as st
from PIL import Image

# User module files
from ml import suggest_recipes

def main():

    #############
    # Main page #
    #############
    st.markdown(
        """
    <style>
    
    .block-container {
        background-color: #901e13;
    }
    .st-header 
        background-color: #901e13;
    }
    
    </style>
    """,
        unsafe_allow_html=True,
    )

    options = ['Home','About','Prediction','Stop']
    choice = st.sidebar.selectbox("Menu",options, key = '1')

    if ( choice == 'Home' ):
        st.title("So you think you can cook ?!")
        st.image('./images/mariopizza.jpg')
        st.write("Real cooks can make delicious meals out of everything. Everything? ")
        st.write("\nLet me tell you -No ingredient can resist me! Pick anything in your pantry and I'll make a meraviglia out of it!")
        st.write("## Let's-a-go!!")
    

    elif ( choice == 'About' ):
        st.title("this is the best recipe recommender. period.")
        st.write("Get ready for this flavourful journey, based on the ingredients in your fridge and a bit of audacity...")
        st.image('./images/mariopan.png')
    

    elif ( choice == 'Prediction' ):
        st.title("Recipe Recommender")
        st.write("### What's in your fridge ?")
        st.image('./images/mario-onion.jpg')
        suggest_recipes()
        st.write("Who's the best ?")
        st.image('./images/marioproud.png')
    
    else:
      st.stop()


main()
