from mysql.connector import connect, Error
import streamlit as st

st.set_page_config(page_title="My Webpage", page_icon=":dash:", layout="wide")

user = st.secrets['rds']['user']
password = st.secrets['rds']['password']
endpoint = st.secrets['rds']['endpoint']
database = "mydatabase"


def run_sql(query, values=None):
    try:
        with connect(
            host=endpoint,
            user=user,
            password=password,
            database=database,
        ) as connection:
            with connection.cursor() as cursor:
                if values is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, values)
                result = cursor.fetchall()
                connection.commit()
        return result
    except Error as e:
        print(e)
        return None


def update_db(name, message, email, age):
    sql = "INSERT INTO votes (name, options, email, age) VALUES (%s, %s, %s, %s)"
    values = (name, message, email, age)
    res = run_sql(sql, values)
    print("res:", res)  # if success: empty list, else None

    #after submit. update names set
    global names
    names.add(name)
    print("new names:", names)

    return not res is None


def get_names():
    sql = "select name from votes"
    if result := run_sql(sql):
        print("fetched result:", result)
        names = set( n[0] for n in result )
        print("names already present:", names)
        return names
    else:
        raise Error("did not correctly retrieve names from DB")


with st.container():
    st.write("---")
    st.header(":memo: Ask for new features :thought_balloon:")
    st.write("##")

    names = get_names()

    with st.form("form1", clear_on_submit=False):
        name = st.text_input("Enter name:")
        email = st.text_input("Enter email:")
        age = st.slider("Age:", min_value=10, max_value=116)
        message = st.text_area("Please describe your feature request:")

        submit = st.form_submit_button("Submit feature request")
        if submit:
            print(name, email, age, message)
            if name in names:
                st.write(f":red[your name {name} already appears in the database; please provide another name!]")
            elif "" in (name, email, message):
                st.write(":orange[not all textboxes are filled. please try again]")
            elif age==10:
                st.write(":violet[You are probably more than 10 years old. Please update your age]")
            else:
                if update_db(name, message, email, age):
                    st.write(":green[submitted! Thanks for your interest in AirMax! We will have a look at your request as soon as possible!]")
                else:
                    st.write(":red[submission did not work. Please try again later. We apologize for the inconvenience]")
