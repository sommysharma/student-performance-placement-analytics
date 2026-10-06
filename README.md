# Student Performance & Placement Analytics

A data analytics and visualization project that analyzes student academic performance, attendance, skills, and placement outcomes using Python, MySQL, Pandas, and Streamlit.

## Project Overview

The Student Performance & Placement Analytics system stores student-related data in MySQL and uses Python and Pandas to analyze academic performance, attendance, skills, placement eligibility, and placement outcomes.

An interactive Streamlit dashboard provides insights through KPIs, charts, filters, student search, eligibility analysis, and skill-gap analysis.

## Features

- Student academic performance analysis
- Attendance analysis
- Placement rate calculation
- Average and highest placement package analysis
- Company-wise placement analysis
- Branch-wise placement analysis
- Placement eligibility analysis
- Eligible but unplaced student identification
- Skill popularity analysis
- Skill-gap analysis for unplaced students
- Subject-wise academic performance
- Student search and filtering
- Interactive Streamlit dashboard
- Data visualizations and analytical reports

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| MySQL | Database management |
| Pandas | Data manipulation and analysis |
| SQLAlchemy | Database connectivity |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Streamlit | Interactive dashboard |
| Git & GitHub | Version control and project hosting |

## Project Structure

```text
Student-Performance-Placement-Analytics/
│
├── analysis/
│   ├── analysis.py
│   └── visualizations.py
│
├── dashboard/
│   └── app.py
│
├── database/
│   └── analytics.sql
│
├── data/
│
├── reports/
│   ├── placement_status.png
│   ├── branch_placement.png
│   ├── cgpa_distribution.png
│   ├── company_placements.png
│   ├── skill_popularity.png
│   ├── cgpa_vs_package.png
│   ├── subject_average_marks.png
│   └── top_academic_students.png
│
├── .gitignore
├── .env
└── requirements.txt
```

## Database Design

The project uses a MySQL database named:

```text
student_analytics
```

The database contains four main tables:

### Students

Stores:

- Student ID
- Name
- Gender
- Branch
- Semester
- CGPA
- Attendance

### Academics

Stores:

- Student ID
- Subject
- Marks

### Skills

Stores:

- Student ID
- Skill name
- Skill level

### Placements

Stores:

- Student ID
- Company name
- Package
- Placement status
- Placement date

## Analytics Performed

### Student Performance

The project calculates:

- Average CGPA
- Highest CGPA
- Lowest CGPA
- Average attendance
- Subject-wise average marks
- Student-wise academic averages
- Branch-wise CGPA

### Placement Analytics

The system calculates:

- Overall placement rate
- Average package
- Highest package
- Company-wise placements
- Branch-wise placement rate
- Placement status
- Eligible but unplaced students

### Placement Eligibility

Students are classified using:

```text
CGPA >= 7.0
AND
Attendance >= 75%
```

Students meeting both conditions are marked as **Eligible**.

### Skill Gap Analysis

The project analyzes the skills of students who have not been placed to identify areas where additional skill development may be required.

## Dashboard

The Streamlit dashboard provides:

- Interactive branch filtering
- Placement-status filtering
- Minimum CGPA filtering
- KPI cards
- Placement charts
- Academic performance charts
- Company analysis
- Skills analysis
- Skill-gap analysis
- Placement eligibility analysis
- Student search
- Top-performing student analysis

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/student-performance-placement-analytics.git
```

### 2. Open the project

```bash
cd student-performance-placement-analytics
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root:

```env
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_HOST=localhost
DB_NAME=student_analytics
```

Do not upload the `.env` file to GitHub.

### 7. Create the database

Create the MySQL database:

```sql
CREATE DATABASE student_analytics;
```

Then execute the SQL queries in:

```text
database/analytics.sql
```

Make sure the required tables and data are available.

### 8. Run the analysis

```powershell
python analysis/analysis.py
```

### 9. Generate visualizations

```powershell
python analysis/visualizations.py
```

### 10. Launch the dashboard

```powershell
python -m streamlit run dashboard/app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

## Security

Database credentials are stored using environment variables rather than hardcoded directly into Python files.

The `.env` file is excluded from Git using `.gitignore`.

Never commit database passwords or other sensitive credentials to a public repository.

## Future Improvements

- Cloud database integration
- User authentication
- Automated data import
- Advanced placement prediction
- Machine learning-based placement prediction
- Resume skill analysis
- More advanced visualizations
- Deployment with a public URL

## Project Outcome

This project demonstrates practical experience with:

- Relational database design
- SQL queries and joins
- Python data analysis
- Pandas data manipulation
- Data visualization
- Interactive dashboards
- Environment-based configuration
- Git and GitHub workflow

## Author

**Somdutt Sharma**

BE – Computer Science & Engineering

Chandigarh University
