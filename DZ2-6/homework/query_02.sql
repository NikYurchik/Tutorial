--Знайти студента із найвищим середнім балом з певного предмета.
SELECT g.student_id,
       s.fullname,
       d.name discipline_name,
       ROUND(AVG(g.grade),2) avg_grade
FROM grades g
JOIN students s ON s.id = g.student_id 
JOIN disciplines d ON d.id  = g.discipline_id 
WHERE 1=1
  AND d.id = :DISCIPLINE_ID               -- код предмету
GROUP BY g.student_id, s.fullname, d.name
ORDER BY AVG(g.grade) DESC
LIMIT 1;
