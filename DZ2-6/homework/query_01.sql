--Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT g.student_id,
       s.fullname,
       ROUND(AVG(g.grade),2) avg_grade
FROM grades g
JOIN students s ON s.id = g.student_id 
GROUP BY g.student_id, s.fullname
ORDER BY AVG(g.grade) DESC
LIMIT 5; 
