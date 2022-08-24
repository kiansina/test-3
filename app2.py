import streamlit as st
import pandas as pd
import random
import time
from google.oauth2 import service_account
from gspread_pandas import Spread,Client
from PIL import Image

img=Image.open('lo.jfif')
st.set_page_config(page_title="Questionnaire", page_icon=img)

hide_menu_style= """
          <style>
          #MainMenu {visibility: hidden; }
          footer {visibility: hidden;}
          </style>
          """
#Image_logo="""
#           <p>
#           <img src="2.PNG" width="200" height="267"/>
#           </p>
#           """

st.markdown(hide_menu_style, unsafe_allow_html=True)
#vst.markdown(Image_logo, unsafe_allow_html=True)

scope=["https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"]
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
)

client=Client(scope=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"], creds=credentials)
spreadsheetname="Questionnaire_test"
#s=Spread(spreadsheetname,client=client)
#sh=client.open(spreadsheetname)

@st.experimental_singleton
def faster():
    return client.open(spreadsheetname),Spread(spreadsheetname,client=client)

sh,s=faster()

df=pd.DataFrame(sh.worksheet('test').get_all_records())

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
  "10": "se giusto è sbaglio e sbaglio è sbaglio, che cosa è giusto?"
}

choices = {
"1": [("4","T"),("8","F"),("0","F")],
"2": [("9","T"),("6","F"),("8","F")],
"3": [("Cielo","T"),("Rosa","F"),("Viola","F")],
"4": [("Cibo","T"),("Pasta","F"),("Coffee","F")],
"5": [("Nonna","T"),("Zia","F"),("Cugina","F")],
"6": [("16","T"),("12","F"),("18","F")],
"7": [("14","T"),("16","F"),("18","F")],
"8": [("13","T"),("16","F"),("14","F")],
"9": [("Roma","T"),("Milano","F"),("Torino","F")],
"10": [("Nulla","T"),("Tutto","F"),("Sbaglio","F")],
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
            #del st.session_state["username"]
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

if "t0" not in st.session_state:
    st.session_state["t0"] = time.time()
if "st" not in st.session_state:
    st.session_state["st"]= True
if "usercheck" not in st.session_state:
    st.session_state['usercheck']=False
if "rn" not in st.session_state:
    st.session_state["rn"] = random.sample(range(1, 10), 5)


@st.experimental_singleton
def ran():
    for i in range(0,len(st.session_state["rn"])):
        st.session_state["ch{}".format(i)]=random.sample(choices[str(st.session_state["rn"][i])],k=len(choices[str(st.session_state["rn"][i])]))
        st.session_state["cho{}".format(i)]=[x[0] for x in st.session_state["ch{}".format(i)]]
        st.session_state["che{}".format(i)]=[x[1] for x in st.session_state["ch{}".format(i)]]
    return st.session_state["ch0"], st.session_state["ch1"] ,st.session_state["ch2"] ,st.session_state["ch3"] ,st.session_state["ch4"] ,st.session_state["cho0"], st.session_state["cho1"] , st.session_state["cho2"] , st.session_state["cho3"] , st.session_state["cho4"] , st.session_state["che0"] , st.session_state["che1"], st.session_state["che2"], st.session_state["che3"], st.session_state["che4"]

st.session_state["ch0"], st.session_state["ch1"] ,st.session_state["ch2"] ,st.session_state["ch3"] ,st.session_state["ch4"] ,st.session_state["cho0"],st.session_state["cho1"] , st.session_state["cho2"] , st.session_state["cho3"] , st.session_state["cho4"] , st.session_state["che0"] , st.session_state["che1"],st.session_state["che2"], st.session_state["che3"], st.session_state["che4"]=ran()


if check_password():
    @st.cache(allow_output_mutation=True)
    def get_data():
        return []
    Username=st.text_input("Username:")
    if st.button("check"):
        if Username in df['Username'].to_list():
            st.session_state['usercheck']=False
            st.write('l\'esame gia registrato 😊.')
        elif Username not in st.secrets['passwords'].keys():
            st.write('😕 User not known')
        else:
            st.session_state['usercheck']=True
            st.session_state['st']=True
    if st.session_state['usercheck']==True:
        if st.session_state["st"]==True:
            Nome = st.text_input("Nome:")
            Cognome = st.text_input("Cognome:")
            sodisfazione = st.slider("Sodisfazione", 0, 100)
            Qa=st.radio("1)    "+questions[str(st.session_state["rn"][0])],st.session_state["cho0"],horizontal=False)
            Qb=st.radio("2)    "+questions[str(st.session_state["rn"][1])],st.session_state["cho1"],horizontal=False)
            Qc=st.radio("3)    "+questions[str(st.session_state["rn"][2])],st.session_state["cho2"],horizontal=False)
            Qd=st.radio("4)    "+questions[str(st.session_state["rn"][3])],st.session_state["cho3"],horizontal=False)
            Qe=st.radio("5)    "+questions[str(st.session_state["rn"][4])],st.session_state["cho4"],horizontal=False)
            if st.button("Submit"):
                get_data().append({"Username":Username,"Nome": Nome,"Cognome":Cognome, "Livello sodisfazione": sodisfazione, "q1": Qa, "q2": Qb, "q3": Qc, "q4": Qd, "q5": Qe, "time":time.time()-st.session_state["t0"]})
                A=pd.DataFrame(get_data())
                st.session_state["B"]=pd.DataFrame({"Username":Username,"Nome": Nome,"Cognome":Cognome, "Livello sodisfazione": sodisfazione, "q1": st.session_state["che0"][st.session_state["cho0"].index(Qa)], "q2": st.session_state["che1"][st.session_state["cho1"].index(Qb)], "q3": st.session_state["che2"][st.session_state["cho2"].index(Qc)], "q4": st.session_state["che3"][st.session_state["cho3"].index(Qd)], "q5": st.session_state["che4"][st.session_state["cho4"].index(Qe)], "time":time.time()-st.session_state["t0"]},index=[0])
                st.write(A)
            st.write('Se Lei è sicuro da chiudere l\'esamae, premi conferma')
            if st.button("Confirm"):
                L=len(pd.DataFrame(get_data()))
                dx=df.append(st.session_state["B"].loc[L-1,:],ignore_index=True)
                s.df_to_sheet(dx,sheet='test',index=False)
                st.title('la sua esame è finito 😊.')
                st.title("Grazie per la collaborazione! 😍")
                st.session_state["st"]=False
        else:
            st.title('l\'esame gia registrato 😊.')
