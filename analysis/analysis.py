import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

print("Database connected successfully!")

# Load students
students_df = pd.read_sql(
    "SELECT * FROM students",
    engine
)

print("\nTotal Students:", len(students_df))

# Basic student analysis
average_cgpa = students_df["cgpa"].mean()
average_attendance = students_df["attendance"].mean()
highest_cgpa = students_df["cgpa"].max()
lowest_cgpa = students_df["cgpa"].min()

print("\nAverage CGPA:", round(average_cgpa, 2))
print("Average Attendance:", round(average_attendance, 2))
print("Highest CGPA:", highest_cgpa)
print("Lowest CGPA:", lowest_cgpa)

# Placement eligibility
students_df["eligibility"] = students_df.apply(
    lambda row: "Eligible"
    if row["cgpa"] >= 7.0 and row["attendance"] >= 75
    else "Not Eligible",
    axis=1
)

print("\nEligibility Summary:")
print(students_df["eligibility"].value_counts())

# Branch-wise CGPA
branch_cgpa = (
    students_df
    .groupby("branch")["cgpa"]
    .mean()
    .round(2)
)

print("\nBranch-wise Average CGPA:")
print(branch_cgpa)

# Students by branch
branch_count = students_df["branch"].value_counts()

print("\nStudents by Branch:")
print(branch_count)

# Load placements
placements_df = pd.read_sql(
    "SELECT * FROM placements",
    engine
)

print("\nPlacement Summary:")
print(placements_df["placement_status"].value_counts())

# Placement rate
placed_students = (
    placements_df["placement_status"] == "Placed"
).sum()

total_students = len(students_df)

placement_rate = (
    placed_students / total_students
) * 100

print("\nPlacement Rate:", round(placement_rate, 2), "%")

# Average package
placed_data = placements_df[
    placements_df["placement_status"] == "Placed"
]

average_package = placed_data["package_lpa"].mean()

print("Average Package:", round(average_package, 2), "LPA")

# Highest package
highest_package = placed_data["package_lpa"].max()

print("Highest Package:", highest_package, "LPA")

# Company-wise placement
company_placements = (
    placed_data["company_name"]
    .value_counts()
)

print("\nCompany-wise Placements:")
print(company_placements)

# Merge student and placement data
student_placement_df = pd.merge(
    students_df,
    placements_df,
    on="student_id",
    how="left"
)

print("\nStudent Placement Data:")

print(
    student_placement_df[
        [
            "name",
            "branch",
            "cgpa",
            "attendance",
            "eligibility",
            "company_name",
            "package_lpa",
            "placement_status"
        ]
    ].to_string(index=False)
)

# Eligible but not placed students
eligible_unplaced = student_placement_df[
    (student_placement_df["eligibility"] == "Eligible") &
    (student_placement_df["placement_status"] == "Not Placed")
]

print("\nEligible but Not Placed Students:")

print(
    eligible_unplaced[
        [
            "student_id",
            "name",
            "branch",
            "cgpa",
            "attendance"
        ]
    ].to_string(index=False)
)

# Branch-wise placement rate
branch_placement = (
    student_placement_df
    .groupby("branch")
    .agg(
        total_students=("student_id", "count"),
        placed_students=(
            "placement_status",
            lambda x: (x == "Placed").sum()
        )
    )
)

branch_placement["placement_rate"] = (
    branch_placement["placed_students"]
    / branch_placement["total_students"]
    * 100
).round(2)

print("\nBranch-wise Placement Analysis:")
print(branch_placement)

# Load academics
academics_df = pd.read_sql(
    "SELECT * FROM academics",
    engine
)

# Academic performance
academic_average = (
    academics_df
    .groupby("student_id")["marks"]
    .mean()
    .round(2)
)

print("\nAcademic Performance:")
print(academic_average)

# Subject-wise performance
subject_average = (
    academics_df
    .groupby("subject")["marks"]
    .mean()
    .round(2)
)

print("\nSubject-wise Average Marks:")
print(subject_average)

print("\nAnalysis completed successfully!")