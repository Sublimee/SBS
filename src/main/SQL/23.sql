-- Задача 2

SELECT d.dwarf_id,
       d.name,
       d.age,
       d.profession,
       json_build_object(
               'skill_ids', COALESCE(
               (SELECT json_agg(skill_id) -- использование COALESCE -- более взрослый вариант: пустой массив вместо NULL, если сущности не найдены (далее для компактности не использую)
                FROM dwarf_skills ds
                WHERE ds.dwarf_id = d.dwarf_id), '[]'::json),
               'assignment_ids', COALESCE((SELECT json_agg(assignment_id)
                                           FROM dwarf_assignments da
                                           WHERE da.dwarf_id = d.dwarf_id), '[]'::json),
               'squad_ids', COALESCE((SELECT json_agg(squad_id)
                                      FROM squad_members sm
                                      WHERE sm.dwarf_id = d.dwarf_id), '[]'::json),
               'equipment_ids', COALESCE((SELECT json_agg(equipment_id)
                                          FROM dwarf_equipment de
                                          WHERE de.dwarf_id = d.dwarf_id), '[]'::json)
       ) AS related_entities
FROM dwarves d;

-- Задача 3

SELECT w.workshop_id,
       w.name,
       w.type,
       w.quality,
       json_build_object(
               'craftsdwarf_ids', (SELECT json_agg(dwarf_id)
                                   FROM workshop_craftsdwarves wc
                                   WHERE wc.workshop_id = w.workshop_id),
               'project_ids', (SELECT json_agg(project_id)
                               FROM projects p
                               WHERE p.workshop_id = w.workshop_id),
               'input_material_ids', (SELECT json_agg(material_id)
                                      FROM workshop_materials wm
                                      WHERE wm.workshop_id = w.workshop_id),
               'output_product_ids', (SELECT json_agg(product_id)
                                      FROM workshop_products wp
                                      WHERE wp.workshop_id = w.workshop_id)
       ) AS related_entities
FROM workshops w;

-- Задача 4

SELECT s.squad_id,
       s.name,
       s.formation_type,
       s.leader_id,
       json_build_object(
               'member_ids', (SELECT json_agg(dwarf_id)
                              FROM squad_members sm
                              WHERE sm.squad_id = s.squad_id),
               'equipment_ids', (SELECT json_agg(equipment_id)
                                 FROM squad_equipment se
                                 WHERE se.squad_id = s.squad_id),
               'operation_ids', (SELECT json_agg(operation_id)
                                 FROM squad_operations so
                                 WHERE so.squad_id = s.squad_id),
               'training_schedule_ids', (SELECT json_agg(schedule_id)
                                         FROM squad_training st
                                         WHERE st.squad_id = s.squad_id),
               'battle_report_ids', (SELECT json_agg(report_id)
                                     FROM squad_battles sb
                                     WHERE sb.squad_id = s.squad_id)
       ) AS related_entities
FROM military_squads s;