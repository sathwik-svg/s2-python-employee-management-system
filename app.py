import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "employees" not in st.session_state:
    st.session_state.employees = [
        {
            "Employee ID": 1001,
            "Name": "Rahul Kumar",
            "Department": "Engineering",
            "Role": "Software Engineer",
            "Email": "rahul@example.com",
            "Salary": 65000,
            "Joining Date": "2025-06-10"
        },
        {
            "Employee ID": 1002,
            "Name": "Priya Sharma",
            "Department": "HR",
            "Role": "HR Executive",
            "Email": "priya@example.com",
            "Salary": 52000,
            "Joining Date": "2025-08-15"
        },
        {
            "Employee ID": 1003,
            "Name": "Arjun Reddy",
            "Department": "Finance",
            "Role": "Financial Analyst",
            "Email": "arjun@example.com",
            "Salary": 58000,
            "Joining Date": "2026-01-12"
        }
    ]


def employee_dataframe():
    return pd.DataFrame(st.session_state.employees)


# -----------------------------
# Header
# -----------------------------
st.title("👨‍💼 Employee Management System")
st.caption("S2 Python Project 3 — Employee administration dashboard")

st.divider()

# -----------------------------
# Dashboard Metrics
# -----------------------------
df = employee_dataframe()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", len(df))

with col2:
    departments = df["Department"].nunique() if not df.empty else 0
    st.metric("Departments", departments)

with col3:
    average_salary = df["Salary"].mean() if not df.empty else 0
    st.metric("Average Salary", f"₹{average_salary:,.0f}")

with col4:
    total_payroll = df["Salary"].sum() if not df.empty else 0
    st.metric("Total Payroll", f"₹{total_payroll:,.0f}")

st.divider()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Employee Management")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Employee",
        "View Employees",
        "Edit Employee",
        "Delete Employee"
    ]
)

# -----------------------------
# Dashboard
# -----------------------------
if menu == "Dashboard":

    st.header("📊 Dashboard")

    if df.empty:
        st.info("No employees available.")
    else:
        st.subheader("Employees by Department")

        department_counts = df["Department"].value_counts()
        st.bar_chart(department_counts)

        st.subheader("Employee Overview")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# -----------------------------
# Add Employee
# -----------------------------
elif menu == "Add Employee":

    st.header("➕ Add Employee")

    with st.form("add_employee_form"):

        employee_id = st.number_input(
            "Employee ID",
            min_value=1,
            step=1
        )

        name = st.text_input("Full Name")

        department = st.selectbox(
            "Department",
            [
                "Engineering",
                "HR",
                "Finance",
                "Marketing",
                "Sales",
                "Operations"
            ]
        )

        role = st.text_input("Job Role")

        email = st.text_input("Email")

        salary = st.number_input(
            "Annual Salary (₹)",
            min_value=0,
            step=1000
        )

        joining_date = st.date_input(
            "Joining Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Add Employee"
        )

        if submitted:

            existing_ids = [
                employee["Employee ID"]
                for employee in st.session_state.employees
            ]

            if employee_id in existing_ids:
                st.error("Employee ID already exists.")

            elif not name.strip():
                st.error("Please enter the employee name.")

            elif not role.strip():
                st.error("Please enter the job role.")

            elif not email.strip():
                st.error("Please enter the email.")

            else:

                st.session_state.employees.append(
                    {
                        "Employee ID": int(employee_id),
                        "Name": name.strip(),
                        "Department": department,
                        "Role": role.strip(),
                        "Email": email.strip(),
                        "Salary": int(salary),
                        "Joining Date": str(joining_date)
                    }
                )

                st.success(
                    f"Employee {name} added successfully!"
                )


# -----------------------------
# View Employees
# -----------------------------
elif menu == "View Employees":

    st.header("📋 Employee Directory")

    df = employee_dataframe()

    if df.empty:
        st.info("No employees available.")

    else:

        search = st.text_input(
            "🔍 Search employees",
            placeholder="Search by name, department, role or email..."
        )

        if search:

            search_lower = search.lower()

            filtered_df = df[
                df.astype(str)
                .apply(
                    lambda row: row.str.lower().str.contains(
                        search_lower,
                        regex=False
                    ).any(),
                    axis=1
                )
            ]

        else:
            filtered_df = df

        st.write(
            f"Showing **{len(filtered_df)}** employee(s)"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )


# -----------------------------
# Edit Employee
# -----------------------------
elif menu == "Edit Employee":

    st.header("✏️ Edit Employee")

    df = employee_dataframe()

    if df.empty:
        st.info("No employees available.")

    else:

        employee_ids = [
            employee["Employee ID"]
            for employee in st.session_state.employees
        ]

        selected_id = st.selectbox(
            "Select Employee",
            employee_ids
        )

        selected_employee = next(
            employee
            for employee in st.session_state.employees
            if employee["Employee ID"] == selected_id
        )

        with st.form("edit_employee_form"):

            name = st.text_input(
                "Full Name",
                value=selected_employee["Name"]
            )

            department_options = [
                "Engineering",
                "HR",
                "Finance",
                "Marketing",
                "Sales",
                "Operations"
            ]

            current_department = selected_employee["Department"]

            department_index = (
                department_options.index(current_department)
                if current_department in department_options
                else 0
            )

            department = st.selectbox(
                "Department",
                department_options,
                index=department_index
            )

            role = st.text_input(
                "Job Role",
                value=selected_employee["Role"]
            )

            email = st.text_input(
                "Email",
                value=selected_employee["Email"]
            )

            salary = st.number_input(
                "Annual Salary (₹)",
                min_value=0,
                value=int(selected_employee["Salary"]),
                step=1000
            )

            joining_date = st.date_input(
                "Joining Date",
                value=pd.to_datetime(
                    selected_employee["Joining Date"]
                ).date()
            )

            submitted = st.form_submit_button(
                "Update Employee"
            )

            if submitted:

                selected_employee["Name"] = name.strip()
                selected_employee["Department"] = department
                selected_employee["Role"] = role.strip()
                selected_employee["Email"] = email.strip()
                selected_employee["Salary"] = int(salary)
                selected_employee["Joining Date"] = str(joining_date)

                st.success(
                    "Employee updated successfully!"
                )


# -----------------------------
# Delete Employee
# -----------------------------
elif menu == "Delete Employee":

    st.header("🗑️ Delete Employee")

    df = employee_dataframe()

    if df.empty:
        st.info("No employees available.")

    else:

        employee_ids = [
            employee["Employee ID"]
            for employee in st.session_state.employees
        ]

        selected_id = st.selectbox(
            "Select Employee",
            employee_ids
        )

        selected_employee = next(
            employee
            for employee in st.session_state.employees
            if employee["Employee ID"] == selected_id
        )

        st.warning(
            f"Selected employee: "
            f"**{selected_employee['Name']}**"
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this employee."
        )

        if st.button(
            "Delete Employee",
            type="primary",
            disabled=not confirm
        ):

            st.session_state.employees = [
                employee
                for employee in st.session_state.employees
                if employee["Employee ID"] != selected_id
            ]

            st.success(
                "Employee deleted successfully!"
            )

            st.rerun()


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "S2 Python Employee Management System • "
    "Built with Python & Streamlit"
)
