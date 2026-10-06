
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


st.set_page_config(
    page_title="Student Analytics",
    page_icon="📊",
    layout="wide"
)


# Database configuration

try:
    DB_USER = st.secrets["DB_USER"]
    DB_PASSWORD = st.secrets["DB_PASSWORD"]
    DB_HOST = st.secrets["DB_HOST"]
    DB_PORT = st.secrets.get("DB_PORT", "3306")
    DB_NAME = st.secrets["DB_NAME"]
    DB_CA = st.secrets.get("DB_CA", "")

except Exception:
    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")
    DB_CA = os.getenv("DB_CA", "")


# Database connection

connection_url = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

connect_args = {}

if DB_CA:
    connect_args["ssl"] = {
        "ca": DB_CA
    }

engine = create_engine(
    connection_url,
    connect_args=connect_args
)


# Load data

students_df = pd.read_sql(
    "SELECT * FROM students",
    engine
)

placements_df = pd.read_sql(
    "SELECT * FROM placements",
    engine
)

skills_df = pd.read_sql(
    "SELECT * FROM skills",
    engine
)

academics_df = pd.read_sql(
    "SELECT * FROM academics",
    engine
)


# Merge student and placement data

data = pd.merge(
    students_df,
    placements_df,
    on="student_id",
    how="left"
)


# Calculate academic average

academic_avg = (
    academics_df
    .groupby("student_id")["marks"]
    .mean()
    .round(2)
    .reset_index(name="academic_average")
)


data = pd.merge(
    data,
    academic_avg,
    on="student_id",
    how="left"
)


# Placement eligibility

data["eligibility"] = data.apply(
    lambda row: "Eligible"
    if row["cgpa"] >= 7.0 and row["attendance"] >= 75
    else "Not Eligible",
    axis=1
)


# Custom styling

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 34px;
        font-weight: 700;
        color: #172554;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #172554;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar

st.sidebar.title("📊 Analytics")

st.sidebar.markdown("### Filters")


branch_options = ["All"] + sorted(
    data["branch"].dropna().unique().tolist()
)

selected_branch = st.sidebar.selectbox(
    "Branch",
    branch_options
)


status_options = [
    "All",
    "Placed",
    "Not Placed"
]

selected_status = st.sidebar.selectbox(
    "Placement Status",
    status_options
)


min_cgpa = st.sidebar.slider(
    "Minimum CGPA",
    min_value=float(data["cgpa"].min()),
    max_value=float(data["cgpa"].max()),
    value=float(data["cgpa"].min()),
    step=0.1
)


# Apply filters

filtered_data = data.copy()

if selected_branch != "All":
    filtered_data = filtered_data[
        filtered_data["branch"] == selected_branch
    ]

if selected_status != "All":
    filtered_data = filtered_data[
        filtered_data["placement_status"] == selected_status
    ]

filtered_data = filtered_data[
    filtered_data["cgpa"] >= min_cgpa
]


# Header

st.markdown(
    '<div class="dashboard-title">'
    'Student Performance & Placement Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Analyze academic performance, attendance, skills and placement outcomes.'
    '</div>',
    unsafe_allow_html=True
)


# KPI calculations

total_students = len(filtered_data)

placed_students = (
    filtered_data["placement_status"] == "Placed"
).sum()

placement_rate = (
    placed_students / total_students * 100
    if total_students > 0
    else 0
)

average_cgpa = (
    filtered_data["cgpa"].mean()
    if total_students > 0
    else 0
)

average_attendance = (
    filtered_data["attendance"].mean()
    if total_students > 0
    else 0
)

average_marks = (
    filtered_data["academic_average"].mean()
    if total_students > 0
    else 0
)

placed_data = filtered_data[
    filtered_data["placement_status"] == "Placed"
]

average_package = (
    placed_data["package_lpa"].mean()
    if len(placed_data) > 0
    else 0
)


# KPI cards

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    "Total Students",
    total_students
)

col2.metric(
    "Placement Rate",
    f"{placement_rate:.1f}%"
)

col3.metric(
    "Average CGPA",
    f"{average_cgpa:.2f}"
)

col4.metric(
    "Attendance",
    f"{average_attendance:.1f}%"
)

col5.metric(
    "Average Package",
    f"{average_package:.2f} LPA"
)

col6.metric(
    "Average Marks",
    f"{average_marks:.1f}"
)


st.divider()


# Placement overview

st.markdown(
    '<div class="section-title">Placement Overview</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Placement Status")

    placement_counts = (
        filtered_data["placement_status"]
        .value_counts()
    )

    st.bar_chart(
        placement_counts
    )


with col2:

    st.subheader("Placement by Branch")

    branch_placement = (
        filtered_data
        .groupby("branch")["placement_status"]
        .apply(
            lambda x:
            (x == "Placed").mean() * 100
        )
        .round(2)
    )

    st.bar_chart(
        branch_placement
    )


# Academic analysis

st.markdown(
    '<div class="section-title">Academic Performance</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Average CGPA by Branch")

    branch_cgpa = (
        filtered_data
        .groupby("branch")["cgpa"]
        .mean()
        .round(2)
    )

    st.bar_chart(
        branch_cgpa
    )


with col2:

    st.subheader("Top Academic Performers")

    academic_data = (
        filtered_data[
            [
                "name",
                "academic_average"
            ]
        ]
        .set_index("name")
        .sort_values(
            "academic_average",
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        academic_data
    )


st.subheader(
    "Subject-wise Average Marks"
)

subject_average = (
    academics_df
    .groupby("subject")["marks"]
    .mean()
    .round(2)
)

st.bar_chart(
    subject_average
)


# Company analysis

st.markdown(
    '<div class="section-title">Placement Companies</div>',
    unsafe_allow_html=True
)

company_data = filtered_data[
    filtered_data["placement_status"] == "Placed"
]

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Students Placed by Company"
    )

    company_counts = (
        company_data["company_name"]
        .value_counts()
    )

    st.bar_chart(
        company_counts
    )


with col2:

    st.subheader(
        "Average Package by Company"
    )

    company_package = (
        company_data
        .groupby("company_name")["package_lpa"]
        .mean()
        .round(2)
    )

    st.bar_chart(
        company_package
    )


# Skills analysis

st.markdown(
    '<div class="section-title">Skills Analysis</div>',
    unsafe_allow_html=True
)

skill_counts = (
    skills_df["skill_name"]
    .value_counts()
)

st.bar_chart(
    skill_counts
)


# Skill gap analysis

st.markdown(
    '<div class="section-title">Skill Gap Analysis</div>',
    unsafe_allow_html=True
)

not_placed_students = filtered_data[
    filtered_data["placement_status"] == "Not Placed"
]

not_placed_ids = (
    not_placed_students["student_id"]
    .tolist()
)

not_placed_skills = skills_df[
    skills_df["student_id"].isin(
        not_placed_ids
    )
]

skill_gap_counts = (
    not_placed_skills["skill_name"]
    .value_counts()
)

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Skills Among Not Placed Students"
    )

    st.bar_chart(
        skill_gap_counts
    )


with col2:

    st.subheader(
        "Students Needing Skill Development"
    )

    if len(not_placed_students) > 0:

        skill_development = not_placed_students[
            [
                "name",
                "branch",
                "cgpa",
                "academic_average",
                "attendance"
            ]
        ].copy()

        skill_development[
            "status"
        ] = "Needs Skill Development"

        st.dataframe(
            skill_development,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No unplaced students found for the selected filters."
        )


# Eligibility analysis

st.markdown(
    '<div class="section-title">Placement Eligibility</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    eligibility_counts = (
        filtered_data["eligibility"]
        .value_counts()
    )

    st.bar_chart(
        eligibility_counts
    )


with col2:

    eligible_unplaced = filtered_data[
        (filtered_data["eligibility"] == "Eligible") &
        (
            filtered_data["placement_status"]
            == "Not Placed"
        )
    ]

    st.metric(
        "Eligible but Not Placed",
        len(eligible_unplaced)
    )

    if len(eligible_unplaced) > 0:

        st.dataframe(
            eligible_unplaced[
                [
                    "name",
                    "branch",
                    "cgpa",
                    "academic_average",
                    "attendance"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# Student search

st.markdown(
    '<div class="section-title">Student Search</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search student by name"
)

student_table = filtered_data.copy()

if search:

    student_table = student_table[
        student_table["name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

display_columns = [
    "student_id",
    "name",
    "branch",
    "cgpa",
    "academic_average",
    "attendance",
    "eligibility",
    "company_name",
    "package_lpa",
    "placement_status"
]

st.dataframe(
    student_table[
        display_columns
    ],
    use_container_width=True,
    hide_index=True
)


# Top performers

st.markdown(
    '<div class="section-title">Top Performing Students</div>',
    unsafe_allow_html=True
)

top_students = (
    data[
        [
            "student_id",
            "name",
            "branch",
            "cgpa",
            "academic_average",
            "attendance"
        ]
    ]
    .sort_values(
        [
            "academic_average",
            "cgpa"
        ],
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_students,
    use_container_width=True,
    hide_index=True
)


st.divider()

st.caption(
    "Student Performance & Placement Analytics | "
    "Python • MySQL • Pandas • Streamlit"
)
