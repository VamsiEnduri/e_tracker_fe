import streamlit as st
import requests
import pandas as pd

# ======================================================
# BACKEND SERVER URL
# ======================================================
server = st.secrets["be_server_url"]

# ======================================================
# PAGE TITLE
# ======================================================
st.title("Expense Tracker App")

# ======================================================
# SIDEBAR MENU
# ======================================================
menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Add Expense",
        "View Expenses",
        "Update Expense",
        "Delete Expense",
        "Expense Summary"
    ]
)

# ======================================================
# ADD EXPENSE
# ======================================================
if menu == "Add Expense":

    st.header("Add Expense")

    title = st.text_input("Title")

    amount = st.number_input(
        "Amount",
        min_value=1.0
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Cash",
            "UPI",
            "Card",
            "Net Banking"
        ]
    )

    expense_date = st.date_input("Expense Date")

    description = st.text_area("Description")

    if st.button("Add Expense"):

        payload = {
            "title": title,
            "amount": amount,
            "category": category,
            "payment_method": payment_method,
            "expense_date": str(expense_date),
            "description": description
        }

        try:

            response = requests.post(
                f"{server}/add_expense",
                json=payload
            )

            st.write("Status Code :", response.status_code)

            if response.status_code == 200:

                st.success(
                    "added"
                )

            else:

                st.error(
                    response.text
                )

        except Exception as e:

            st.error(str(e))

# ======================================================
# VIEW EXPENSES
# ======================================================
elif menu == "View Expenses":

    st.header("All Expenses")

    try:

        response = requests.get(
            f"{server}/get_expenses"
        )

        data = response.json()["expenses"]

        if data:

            df = pd.DataFrame(data)

            st.dataframe(df)

            total = df["amount"].sum()

            st.subheader(
                f"Total Expense : ₹ {total}"
            )

        else:

            st.warning("No Expenses Found")

    except Exception as e:

        st.error(str(e))

# ======================================================
# UPDATE EXPENSE
# ======================================================
elif menu == "Update Expense":

    st.header("Update Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1,
        step=1
    )

    # --------------------------------------------------
    # FETCH EXPENSE
    # --------------------------------------------------
    if st.button("Fetch Expense"):

        try:

            response = requests.get(
                f"{server}/get_single_expense/{expense_id}"
            )

            if response.status_code == 200:

                data = response.json()["expense"]

                st.session_state["expense_data"] = data

            else:

                st.error("Expense Not Found")

        except Exception as e:

            st.error(str(e))

    # --------------------------------------------------
    # UPDATE FORM
    # --------------------------------------------------
    if "expense_data" in st.session_state:

        data = st.session_state["expense_data"]

        title = st.text_input(
            "Title",
            value=data["title"]
        )

        amount = st.number_input(
            "Amount",
            value=float(data["amount"])
        )

        category = st.text_input(
            "Category",
            value=data["category"]
        )

        payment_method = st.text_input(
            "Payment Method",
            value=data["payment_method"]
        )

        expense_date = st.text_input(
            "Expense Date",
            value=str(data["expense_date"])
        )

        description = st.text_area(
            "Description",
            value=data["description"]
        )

        if st.button("Update Now"):

            payload = {
                "title": title,
                "amount": amount,
                "category": category,
                "payment_method": payment_method,
                "expense_date": expense_date,
                "description": description
            }

            try:

                response = requests.put(
                    f"{server}/update_expense/{expense_id}",
                    json=payload
                )

                if response.status_code == 200:

                    st.success(
                        response.json()["message"]
                    )

                else:

                    st.error("Update Failed")

            except Exception as e:

                st.error(str(e))

# ======================================================
# DELETE EXPENSE
# ======================================================
elif menu == "Delete Expense":

    st.header("Delete Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Expense"):

        try:

            response = requests.delete(
                f"{server}/delete_expense/{expense_id}"
            )

            if response.status_code == 200:

                st.success(
                    response.json()["message"]
                )

            else:

                st.error("Delete Failed")

        except Exception as e:

            st.error(str(e))

# ======================================================
# EXPENSE SUMMARY
# ======================================================
elif menu == "Expense Summary":

    st.header("Expense Summary By Category")

    try:

        response = requests.get(
            f"{server}/expense_summary"
        )

        data = response.json()["summary"]

        if data:

            df = pd.DataFrame(data)

            st.dataframe(df)

            st.bar_chart(
                df.set_index("category")
            )

        else:

            st.warning("No Data Found")

    except Exception as e:

        st.error(str(e))