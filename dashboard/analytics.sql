SELECT COUNT(*) AS total_students
FROM students;

SELECT ROUND(AVG(cgpa), 2) AS average_cgpa
FROM students;

SELECT ROUND(AVG(attendance), 2) AS average_attendance
FROM students;

SELECT
    placement_status,
    COUNT(*) AS total_students
FROM placements
GROUP BY placement_status;

SELECT
    ROUND(
        SUM(placement_status = 'Placed') * 100.0 / COUNT(*),
        2
    ) AS placement_rate
FROM placements;

SELECT
    ROUND(AVG(package_lpa), 2) AS average_package_lpa
FROM placements
WHERE placement_status = 'Placed';

SELECT
    MAX(package_lpa) AS highest_package_lpa
FROM placements
WHERE placement_status = 'Placed';

SELECT
    company_name,
    COUNT(*) AS students_placed
FROM placements
WHERE placement_status = 'Placed'
GROUP BY company_name
ORDER BY students_placed DESC;

SELECT
    s.branch,
    COUNT(*) AS total_students,
    SUM(p.placement_status = 'Placed') AS placed_students,
    ROUND(
        SUM(p.placement_status = 'Placed') * 100.0 / COUNT(*),
        2
    ) AS placement_rate
FROM students s
JOIN placements p
    ON s.student_id = p.student_id
GROUP BY s.branch
ORDER BY placement_rate DESC;

SELECT
    student_id,
    name,
    branch,
    cgpa,
    attendance
FROM students
ORDER BY cgpa DESC
LIMIT 10;

SELECT
    student_id,
    name,
    branch,
    cgpa,
    attendance
FROM students
WHERE cgpa < 7.0
   OR attendance < 75
ORDER BY cgpa;

SELECT
    skill_name,
    COUNT(*) AS student_count
FROM skills
GROUP BY skill_name
ORDER BY student_count DESC;

SELECT
    skill_name,
    COUNT(*) AS advanced_students
FROM skills
WHERE skill_level = 'Advanced'
GROUP BY skill_name
ORDER BY advanced_students DESC;

SELECT
    p.placement_status,
    ROUND(AVG(s.cgpa), 2) AS average_cgpa
FROM students s
JOIN placements p
    ON s.student_id = p.student_id
GROUP BY p.placement_status;

SELECT
    s.student_id,
    s.name,
    s.branch,
    s.cgpa,
    s.attendance,
    p.company_name,
    p.package_lpa,
    p.placement_status
FROM students s
LEFT JOIN placements p
    ON s.student_id = p.student_id
ORDER BY s.cgpa DESC;