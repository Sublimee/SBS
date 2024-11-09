--1
SELECT * FROM Squads where leader_id IS NULL;

--2
SELECT * FROM Dwarves WHERE age > 150 AND profession = 'Warrior';

--3
SELECT DISTINCT D.dwarf_id FROM Dwarves D
    INNER JOIN Items I ON D.dwarf_id = I.owner_id
        WHERE I.type='weapon';

--4
SELECT assigned_to, status, COUNT(*) AS tasks_count FROM Tasks GROUP BY assigned_to, status;

--5
SELECT T.task_id FROM Tasks T
    INNER JOIN Dwarves D ON T.assigned_to = D.dwarf_id
    INNER JOIN Squads S ON D.squad_id = S.squad_id
        WHERE S.name = 'Guardians';

--6
SELECT D1.name AS dwarf_name, D2.name AS relative_name, R.relationship FROM Relationships R
   INNER JOIN Dwarves D1 ON R.dwarf_id = D1.dwarf_id
   INNER JOIN Dwarves D2 ON R.related_to = D2.dwarf_id;