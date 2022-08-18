import streamlit as st
import pandas as pd
import psycopg2
import random


#from .hasher import Hasher
#from .authenticate import Authenticate
#hashed_passwords = stauth.Hasher(['123', '456']).generate()


# Initialize connection.
# Uses st.experimental_singleton to only run once.
#@st.experimental_singleton
#def init_connection():
    #return psycopg2.connect(**st.secrets["postgres"])

#conn = init_connection()
# streamlit_app.py


questions = {
  "1": "2+2=?",
  "2": "√81=?",
  "3": "Quale non è un colore?",
  "4": "la mela ad frutta è come pizza ad?",
  "5": "chi è la mamma di fratello della sorella di tua madre?",
  "6": "1, 4, 9, ?",
  "7": "1, 4, 5, 9, ?",
  "8": "2, 3, 5, 7, 11, ?",
  "9": "quale è il capitale di Italia?",
  "10": "se giusto è sbaglio è sbaglio è sbaglio, che cosa è giusto?"
}





def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    @st.cache(allow_output_mutation=True)
    def get_data():
        return []
    if "rn" not in st.session_state:
        st.session_state["rn"] = random.sample(range(1, 10), 5)
    Nome = st.text_input("Nome:")
    Cognome = st.text_input("Cognome:")
    sodisfazione = st.slider("Sodisfazione", 0, 100)
    Qa=st.text_input(questions[str(st.session_state["rn"][0])])
    Qb=st.text_input(questions[str(st.session_state["rn"][1])])
    Qc=st.text_input(questions[str(st.session_state["rn"][2])])
    Qd=st.text_input(questions[str(st.session_state["rn"][3])])
    Qe=st.text_input(questions[str(st.session_state["rn"][4])])
    if st.button("Submit"):
        get_data().append({"Nome": Nome,"Cognome":Cognome, "Livello sodisfazione": sodisfazione, "q1": Qa, "q2": Qb, "q3": Qc, "q4": Qd, "q5": Qe})
    #
    st.write(pd.DataFrame(get_data()))
    A=pd.DataFrame(get_data())
