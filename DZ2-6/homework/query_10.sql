--Список курсів, які певному студенту читає певний викладач.
SELECT DISTINCT
       g.student_id,
       s.fullname,
       t.fullname teacher_name,
       d.name discipline_name
FROM students s  
JOIN grades g ON g.student_id = s.id 
JOIN disciplines d ON d.id = g.discipline_id
JOIN teachers t ON t.id = d.teacher_id  
WHERE 1=1
  AND s.id = :STUDENT_ID              -- код студента
  AND t.id = :TEACHER_ID              -- код викладача
ORDER BY s.id, t.id,  d.id;
