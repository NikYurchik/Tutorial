--Знайти список курсів, які відвідує студент.
SELECT DISTINCT
       g.student_id,
       s.fullname,
       d.name discipline_name
FROM students s  
JOIN grades g ON g.student_id = s.id 
JOIN disciplines d ON d.id = g.discipline_id 
WHERE 1=1
  AND s.id = :STUDENT_ID              -- код студента
ORDER BY s.id, d.id;
