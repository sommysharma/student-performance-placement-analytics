import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

os.makedirs("reports", exist_ok=True)

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

# Placement status
placement_counts = placements_df[
    "placement_status"
].value_counts()

plt.figure(figsize=(7, 5))

placement_counts.plot(
    kind="bar"
)

plt.title("Placement Status")
plt.xlabel("Placement Status")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    "reports/placement_status.png"
)

plt.close()

# Branch placement rate
branch_data = pd.merge(
    students_df,
    placements_df,
    on="student_id"
)

branch_placement = (
    branch_data
    .groupby("branch")["placement_status"]
    .apply(
        lambda x: (x == "Placed").mean() * 100
    )
    .reset_index(
        name="placement_rate"
    )
)

plt.figure(figsize=(8, 5))

sns.barplot(
    data=branch_placement,
    x="branch",
    y="placement_rate"
)

plt.title("Placement Rate by Branch")
plt.xlabel("Branch")
plt.ylabel("Placement Rate (%)")
plt.tight_layout()

plt.savefig(
    "reports/branch_placement.png"
)

plt.close()

# CGPA distribution
plt.figure(figsize=(8, 5))

sns.histplot(
    students_df["cgpa"],
    bins=8,
    kde=True
)

plt.title("CGPA Distribution")
plt.xlabel("CGPA")
plt.ylabel("Number of Students")
plt.tight_layout()

plt.savefig(
    "reports/cgpa_distribution.png"
)

plt.close()

# Company-wise placements
company_data = placements_df[
    placements_df["placement_status"] == "Placed"
]

company_counts = (
    company_data["company_name"]
    .value_counts()
)

plt.figure(figsize=(9, 5))

company_counts.plot(
    kind="bar"
)

plt.title("Company-wise Placements")
plt.xlabel("Company")
plt.ylabel("Students Placed")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/company_placements.png"
)

plt.close()

# Skill popularity
skill_counts = (
    skills_df["skill_name"]
    .value_counts()
)

plt.figure(figsize=(8, 5))

skill_counts.plot(
    kind="bar"
)

plt.title("Most Popular Skills")
plt.xlabel("Skill")
plt.ylabel("Number of Students")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/skill_popularity.png"
)

plt.close()

# CGPA vs package
package_data = pd.merge(
    students_df,
    placements_df,
    on="student_id"
)

package_data = package_data[
    package_data["placement_status"] == "Placed"
]

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=package_data,
    x="cgpa",
    y="package_lpa"
)

plt.title("CGPA vs Placement Package")
plt.xlabel("CGPA")
plt.ylabel("Package (LPA)")
plt.tight_layout()

plt.savefig(
    "reports/cgpa_vs_package.png"
)

plt.close()

# Subject-wise academic performance
subject_average = (
    academics_df
    .groupby("subject")["marks"]
    .mean()
    .round(2)
)

plt.figure(figsize=(8, 5))

subject_average.plot(
    kind="bar"
)

plt.title("Subject-wise Average Marks")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    "reports/subject_average_marks.png"
)

plt.close()

# Student academic performance
student_average = (
    academics_df
    .groupby("student_id")["marks"]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(10)
)

top_student_names = (
    students_df[
        students_df["student_id"].isin(
            student_average.index
        )
    ][
        ["student_id", "name"]
    ]
)

student_average_df = (
    student_average
    .reset_index(
        name="average_marks"
    )
)

student_average_df = pd.merge(
    student_average_df,
    top_student_names,
    on="student_id"
)

student_average_df = (
    student_average_df
    .sort_values(
        "average_marks",
        ascending=False
    )
)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=student_average_df,
    x="name",
    y="average_marks"
)

plt.title("Top Students by Academic Performance")
plt.xlabel("Student")
plt.ylabel("Average Marks")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/top_academic_students.png"
)

plt.close()

print("All visualizations created successfully!")