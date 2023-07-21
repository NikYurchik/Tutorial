--Знайти список студентів у певній групі.
SELECT gr.name group_name,
       s.fullname 
FROM students s 
JOIN groups gr ON gr.id  = s.group_id 
WHERE 1=1
  AND gr.id = :GROUP_ID              -- код групи
ORDER BY gr.name, s.fullname;
