--Середній бал, який певний викладач ставить певному студентові.
SELECT t.fullname teacher_name,
       s.fullname,
       ROUND(AVG(g.grade),2) avg_grade
FROM teachers t 
JOIN disciplines d ON d.teacher_id  = t.id
JOIN grades g ON g.discipline_id  = d.id 
JOIN students s ON s.id = g.student_id 
WHERE 1=1
  AND t.id = :TEACHER_ID             -- код викладача
  AND s.id = :STUDENT_ID             -- код студента
GROUP BY t.id, s.id
ORDER BY t.id, s.id
