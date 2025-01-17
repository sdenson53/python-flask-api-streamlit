import streamlit as st
import requests
import pandas as pd


API_URL = "http://127.0.0.1:5000"

# Functions
def get_users():
    response = requests.get(f"{API_URL}/users")
    return response.json()


def create_user(name, dob):
    dob_str = dob.strftime('%Y-%m-%d')  # Convert date to string in 'YYYY-MM-DD' format
    payload = {"name": name, "dob": dob_str}
    response = requests.post(f"{API_URL}/user", json=payload)
    return response.json()


def update_user(identifier, is_id, new_name, new_dob):
    new_dob_str = new_dob.strftime('%Y-%m-%d')
    payload = {"name": new_name, "dob": new_dob_str}
    response = requests.put(f"{API_URL}/user/{identifier}", json=payload)
    return response.json()


def delete_user(identifier, is_id):
    try:
        response = requests.delete(f"{API_URL}/user/{identifier}")
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        else:
            return {"message": "Unexpected response from the server."}

    except requests.exceptions.RequestException as e:
        return {"message": f"Error: {str(e)}"}
    except ValueError:
        return {"message": "Received invalid JSON from the server."}

# UI
st.title("User Management System")

# Add user
st.header("Add New User")
with st.form(key="add_user"):
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    submit_button = st.form_submit_button("Add User")

    if submit_button:
        result = create_user(name, dob)
        st.success(result["message"])

st.divider()
# View users
st.header("Users List")
users = get_users()
df = pd.DataFrame(users)
if not df.empty:
    st.dataframe(df)

if st.button("Refresh Table"):
    users = get_users()
    df = pd.DataFrame(users)
    st.rerun()

st.divider()

# Update User
st.header("Update User")
update_search_criterion = st.selectbox("Search for User to Update by", ["ID", "Name"])

if update_search_criterion == "ID":
    user_ids = [user['id'] for user in users]
    selected_id = st.selectbox("Select User ID to Update", user_ids)

    if selected_id:
        with st.form(key="update_user"):
            new_name = st.text_input("New Name")
            new_dob = st.date_input("New Date of Birth")
            submit_button = st.form_submit_button("Update User")

            if submit_button:
                result = update_user(selected_id, True, new_name, new_dob)
                st.success(result["message"])

elif update_search_criterion == "Name":
    user_names = [user['name'] for user in users]
    selected_name = st.selectbox("Select User Name to Update", user_names)

    if selected_name:
        with st.form(key="update_user_by_name"):
            new_name = st.text_input("New Name", value=selected_name)
            new_dob = st.date_input("New Date of Birth")
            submit_button = st.form_submit_button("Update User")

            if submit_button:
                result = update_user(selected_name, False, new_name, new_dob)
                st.success(result["message"])

st.divider()

# Delete User
st.header("Delete User")
delete_search_criterion = st.selectbox("Search for User to Delete by", ["ID", "Name"])

if delete_search_criterion == "ID":
    user_ids = [user['id'] for user in users]
    selected_id_for_delete = st.selectbox("Select User ID to Delete", user_ids)

    if selected_id_for_delete:
        if st.button("Delete User"):
            result = delete_user(selected_id_for_delete, True)
            st.success(result["message"])


elif delete_search_criterion == "Name":
    user_names = [user['name'] for user in users]
    selected_name_for_delete = st.selectbox("Select User Name to Delete", user_names)

    if selected_name_for_delete:
        if st.button("Delete User"):
            result = delete_user(selected_name_for_delete, False)
            st.success(result["message"])
