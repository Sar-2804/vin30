import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="School Attendance", layout="centered")

st.title("📘 School Attendance System")

# Initialize session state
if "students" not in st.session_state:
    st.session_state.students = []

if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame(
        columns=["Date", "Student Name", "Status"]
    )

# ---------------------------
# Add Students Section
# ---------------------------
st.header("➕ Add Students")

new_student = st.text_input("Enter student name")

if st.button("Add Student"):
    if new_student:
        if new_student not in st.session_state.students:
            st.session_state.students.append(new_student)
            st.success(f"{new_student} added!")
        else:
            st.warning("Student already exists")
    else:
        st.error("Please enter a name")

# Show student list
if st.session_state.students:
    st.write("### 👨‍🎓 Student List")
    st.write(st.session_state.students)

# ---------------------------
# Mark Attendance Section
# ---------------------------
st.header("📝 Mark Attendance")

selected_date = st.date_input("Select Date", date.today())

if st.session_state.students:
    attendance_data = []

    for student in st.session_state.students:
        status = st.radio(
            f"{student}",
            ("Present", "Absent"),
            key=f"{student}_{selected_date}"
        )
        attendance_data.append([selected_date, student, status])

    if st.button("Submit Attendance"):
        df = pd.DataFrame(
            attendance_data,
            columns=["Date", "Student Name", "Status"]
        )
        st.session_state.attendance = pd.concat(
            [st.session_state.attendance, df],
            ignore_index=True
        )
        st.success("Attendance recorded!")

# ---------------------------
# View Attendance Records
# ---------------------------
st.header("📊 Attendance Records")

if not st.session_state.attendance.empty:
    st.dataframe(st.session_state.attendance)

    # Download option
    csv = st.session_state.attendance.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Attendance CSV",
        data=csv,
        file_name="attendance.csv",
        mime="text/csv"
    )
else:
    st.info("No attendance records yet.")

# ---------------------------
# Clear Data
# ---------------------------
st.header("⚠️ Reset")

if st.button("Clear All Data"):
    st.session_state.students = []
    st.session_state.attendance = pd.DataFrame(
        columns=["Date", "Student Name", "Status"]
    )
    st.success("All data cleared!")
