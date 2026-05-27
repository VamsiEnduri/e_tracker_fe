import streamlit as st
import requests
import pandas as pd

server = "https://your-backend-url.onrender.com"

st.title("Expense Tracker App")

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Add Expense",
        "View Expenses"
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

        response = requests.post(f"{server}/add_expense",json=payload)

        st.write(response.status_code)
        st.write(response.text)

        if response.status_code == 200:

            st.success(
                response.json()["message"]
            )

        else:

            st.error("Failed To Add Expense")

# ======================================================
# VIEW EXPENSES
# ======================================================
elif menu == "View Expenses":

    st.header("All Expenses")

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