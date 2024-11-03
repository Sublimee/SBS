-- 1
SELECT D.dwarf_id,
       D.name AS dwarf_name,
       D.age,
       D.profession,
       S.squad_id,
       S.name AS squad_name,
       S.mission
FROM Dwarves D
         INNER JOIN Squads S
                    ON S.squad_id = D.squad_id;

-- 2
SELECT *
FROM Dwarves
WHERE profession = 'miner'
  AND squad_id IS NUll;

--3
SELECT *
FROM Tasks
WHERE status = 'pending'
  AND priority = (SELECT MAX(priority) FROM Tasks WHERE status = 'pending');

--4
SELECT D.dwarf_id,
       D.name,
       D.age,
       D.profession,
       COUNT(*) AS item_count
FROM Dwarves D
         INNER JOIN
     Items I ON I.owner_id = D.dwarf_id
GROUP BY D.dwarf_id, D.name, D.age, D.profession;

--5
SELECT S.squad_id,
       S.name            AS squad_name,
       COUNT(D.dwarf_id) AS dwarf_count
FROM Dwarves D
         RIGHT JOIN
     Squads S ON S.squad_id = D.squad_id
GROUP BY S.squad_id, S.name;

--6
WITH profession_tasks AS (SELECT D.profession,
                                 COUNT(*) AS incomplete_tasks
                          FROM Dwarves D
                                   INNER JOIN
                               Tasks T ON D.dwarf_id = T.assigned_to
                          WHERE T.status = 'pending'
                             OR T.status = 'in_progress'
                          GROUP BY D.profession),
     profession_totals AS (SELECT profession,
                                  SUM(incomplete_tasks) AS total_incomplete_tasks
                           FROM profession_tasks
                           GROUP BY profession)

SELECT profession,
       total_incomplete_tasks
FROM profession_totals
WHERE total_incomplete_tasks = (SELECT MAX(total_incomplete_tasks)
                                FROM profession_totals);

--7
SELECT I.type, AVG(D.age) AS avg_age
FROM Items I
         LEFT JOIN Dwarves D ON I.owner_id = D.dwarf_id OR I.owner_id IS NULL -- потому что предметы без явно указанного владельца принадлежат всем
GROUP BY I.type;

--8
SELECT D.dwarf_id
FROM Dwarves D
         LEFT JOIN Items I ON I.owner_id = D.dwarf_id OR I.owner_id IS NULL
WHERE I.item_id IS NULL AND D.age>(SELECT AVG(Dwarves.age) as age FROM Dwarves);