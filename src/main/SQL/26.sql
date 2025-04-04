WITH battle_stats AS (SELECT s_b.squad_id,
                             COUNT(*)                                                   AS total_battles,
                             COUNT(CASE WHEN s_b.outcome = 'Victory' THEN 1 ELSE 0 END) AS victories,
                             SUM(s_b.casualties)                                        AS squad_casualties,
                             ARRAY_AGG(DISTINCT s_b.battle_id)                          AS battle_report_ids
                      FROM squad_battles s_b
                      GROUP BY s_b.squad_id),
     member_stats AS (SELECT s_m.squad_id,
                             COUNT(DISTINCT s_m.dwarf_id)                                 AS total_members_ever,
                             COUNT(DISTINCT CASE WHEN e_m.survived THEN e_m.dwarf_id END) AS current_members,
                             ARRAY_AGG(DISTINCT s_m.dwarf_id)                             AS member_ids
                      FROM squad_members s_m
                               LEFT JOIN expedition_members e_m ON s_m.dwarf_id = e_m.dwarf_id
                      GROUP BY s_m.squad_id),
     equipment_stats AS (SELECT s_e.squad_id,
                                ROUND(SUM(e.quality * s_e.quantity)::float / NULLIF(SUM(s_e.quantity), 0), 2) AS avg_equipment_quality,
                                ARRAY_AGG(DISTINCT s_e.equipment_id) AS equipment_ids,
                         FROM squad_equipment s_e
                                  JOIN equipment e ON s_e.equipment_id = e.equipment_id
                         GROUP BY s_e.squad_id),
     training_stats AS (SELECT s_t.squad_id,
                               -- не совсем понятно, как считать статистику по тренировкам с учетом того, что присутствует частота тренировок frequency,
                               -- но отсутствуют даты начала и конца расписания для каждого schedule_id. В данном случае беру среднее от частоты, что покажет
                               -- насколько часто были тренировки по каждому из расписаний
                               SUM(s_t.frequency) AS sum_training_frequency,
                               COUNT(*) AS total_training_sessions, -- исходя из соображений по sum_training_frequency этот подсчет числа тренировок считаю некорректным, но буду использовать его
                               ARRAY_AGG(DISTINCT st.schedule_id) AS training_ids
                        FROM squad_training s_t
                        GROUP BY s_t.squad_id),
  -- skill_improvement AS (...), опять не понимаю, как посчитать прогресс, так как у нас есть только текущий уровень (из DWARF_SKILLS) не привязанный ко времени
     squad_info AS (SELECT m_s.squad_id,
                           m_s.name AS squad_name,
                           m_s.formation_type,
                           d.name   AS leader_name
                    FROM military_squads m_s
                             JOIN dwarves d ON d.dwarf_id = m_s.leader_id)
SELECT s_i.squad_id,
       s_i.squad_name,
       s_i.formation_type,
       s_i.leader_name,
       b_s.total_battles,
       b_s.victories,
       ROUND(100.0 * b_s.victories / NULLIF(b_s.total_battles, 0), 2)             AS victory_percentage,
       ROUND(100.0 * b_s.squad_casualties / NULLIF(m_s.total_members_ever, 0), 2) AS casualty_rate, -- так как непонятно, сколько было участников на момент битвы (есть данные когда дварф вступил в отряд, но нет информации когда умер, то считаю по общему количеству)
       ROUND(NULLIF(b_s.victories, 0) * 1.0 / NULLIF(b_s.squad_casualties, 0), 2) AS casualty_exchange_ratio,
       m_s.current_members,
       m_s.total_members_ever,
       ROUND(100.0 * m_s.current_members / NULLIF(m_s.total_members_ever, 0), 2)  AS retention_rate,
       e_s.avg_equipment_quality,
       t_s.total_training_sessions,
       t_s.sum_training_frequency,
       ROUND((
                 0.3 * (b_s.victories::float / NULLIF(b_s.total_battles, 0)) +
                 0.2 * (1.0 - b_s.squad_casualties::float / NULLIF(m_s.total_members_ever, 0)) +
                 0.1 * COALESCE(e_s.avg_equipment_quality, 0) / 5.0 +
                 0.2 * COALESCE(t_s.sum_training_frequency, 0)
            ), 3)                                                            AS overall_effectiveness_score,
       JSON_BUILD_OBJECT(
               'member_ids', m_s.member_ids,
               'equipment_ids', e_s.equipment_ids,
               'battle_report_ids', b_s.battle_report_ids,
               'training_ids', t_s.training_ids
       ) AS related_entities
FROM squad_info s_i
         LEFT JOIN battle_stats b_s ON s_i.squad_id = b_s.squad_id
         LEFT JOIN member_stats m_s ON s_i.squad_id = m_s.squad_id
         LEFT JOIN equipment_stats e_s ON s_i.squad_id = e_s.squad_id
         LEFT JOIN training_stats t_s ON s_i.squad_id = t_s.squad_id;
