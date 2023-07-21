--Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT d.teacher_id,
       t.fullname teacher_name,
       ROUND(AVG(g.grade),2) avg_grade
FROM teachers t
JOIN disciplines d ON d.teacher_id  = t.id 
JOIN grades g ON g.discipline_id = d.id 
WHERE 1=1
  AND t.id = :TEACHER_ID               -- код викладача
GROUP BY d.teacher_id, t.id 
ORDER BY d.teacher_id, d.id;
