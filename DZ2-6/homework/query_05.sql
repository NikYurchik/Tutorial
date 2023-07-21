--Знайти, які курси читає певний викладач.
SELECT d.teacher_id,
       t.fullname teacher_name,
       d.name discipline_name
FROM teachers t
JOIN disciplines d ON d.teacher_id  = t.id 
WHERE 1=1
  AND t.id = :TEACHER_ID               -- код викладача
ORDER BY d.teacher_id, d.id;
