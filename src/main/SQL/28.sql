WITH total_attack_stats AS (SELECT COUNT(*)                                        AS total_attacks,
                                   COUNT(DISTINCT creature_id)                     AS unique_attackers,
                                   SUM(CASE WHEN casualties = 0 THEN 1 ELSE 0 END) AS successful_defenses
                            FROM creature_attacks),
     defense_rate AS (SELECT EXTRACT(YEAR FROM c_a.date)                         AS year,
                             COUNT(c_a.attack_id)                                AS total_attacks,
                             SUM(CASE WHEN c_a.casualties = 0 THEN 1 ELSE 0 END) AS successful_defenses,
                             ROUND(SUM(CASE WHEN c_a.casualties = 0 THEN 1 ELSE 0 END)::numeric /
                                   COUNT(*) * 100,
                                   2)                                            AS defense_success_rate,
                             SUM(casualties)                                     AS casualties
                      FROM creature_attacks c_a
                      GROUP BY year
                      ORDER BY year),
     security_evolution AS (SELECT d_r.*,
                                   ROUND(d_r.defense_success_rate -
                                         LAG(d_r.defense_success_rate) OVER (ORDER BY d_r.year),
                                         2) AS year_over_year_improvement
                            FROM defense_rate d_r),
     active_threats AS (SELECT c.type                            AS creature_type,
                               c.threat_level,
                               MAX(c_s.date)                     AS last_sighting_date,
                               AVG(c_t.area)                     AS territory_proximity,
                               COUNT(DISTINCT c.creature_id)     AS estimated_numbers,
                               ARRAY_AGG(DISTINCT c.creature_id) AS creature_ids
                        FROM creatures c
                                 JOIN creature_sightings c_s ON c.creature_id = c_s.creature_id
                                 JOIN creature_territories c_t ON c.creature_id = c_t.creature_id
                        WHERE c.threat_level >= 3
                        GROUP BY c.type, c.threat_level),
     vulnerability_analysis AS (SELECT p_z.zone_id,
                                       p_z.area AS zone_name, -- непонятно, так ли это?
                                       -- непонятно, как связать project_zones с squad_operations (у операций не нашел привязок к зонам)
                                       -- непонятно, как связать project_zones с fortresses (непонятно, как связать area и location)
                                       -- далее подсчет всех метрик рассыпается
                                    ...
                                    FROM project_zones p_z),
     defense_structures AS (-- как будто нет таблиц и связей для понятия structure
     ),
     military_readiness AS (SELECT m_s.squad_id,
                                   m_s.name                      AS squad_name,
                                   COUNT(DISTINCT s_m.dwarf_id)  AS active_members,
                                   ROUND(AVG(d_s.level), 2)      AS avg_combat_skill,
                                   COUNT(DISTINCT s_b.report_id) AS total_battles,
                                   ROUND(
                                           CASE
                                               WHEN COUNT(DISTINCT s_b.report_id) = 0 THEN NULL
                                               ELSE SUM(CASE WHEN s_b.outcome = 'victory' THEN 1 ELSE 0 END)::numeric /
                                                    COUNT(DISTINCT s_b.report_id)
                                               END,
                                           2)                    AS combat_effectiveness
                            -- непонятно, как считать readiness_score
                            -- непонятно, как squad с локациями
                            FROM military_squads m_s
                                     LEFT JOIN squad_members s_m ON s_m.squad_id = m_s.squad_id
                                     LEFT JOIN dwarf_skills d_s ON d_s.dwarf_id = s_m.dwarf_id
                                     LEFT JOIN skills s ON s.skill_id = d_s.skill_id AND s.category = 'combat'
                                     LEFT JOIN squad_battles s_b ON s_b.squad_id = m_s.squad_id
                            GROUP BY m_s.squad_id)
SELECT json_build_object(
               'total_recorded_attacks', (SELECT total_attacks FROM total_attack_stats),
               'unique_attackers', (SELECT unique_attackers FROM total_attack_stats),
               'overall_defense_success_rate', (SELECT defense_success_rate FROM defense_rate),
               'security_analysis', jsonb_build_object(
                       'threat_assessment', jsonb_build_object(
                        'active_threats', (SELECT jsonb_agg(jsonb_build_object(
                                'creature_type', creature_type,
                                'threat_level', threat_level,
                                'last_sighting_date', last_sighting_date,
                                'territory_proximity', territory_proximity,
                                'estimated_numbers', estimated_numbers,
                                'creature_ids', creature_ids
                                                            ))
                                           FROM active_threats)
                                            ),
                       'military_readiness_assessment', (SELECT jsonb_agg(jsonb_build_object(
                        'squad_id', squad_id,
                        'squad_name', squad_name,
                        'active_members', active_members,
                        'avg_combat_skill', avg_combat_skill,
                        'combat_effectiveness', combat_effectiveness,
                        'total_battles', total_battles
                                                                          ))
                                                         FROM military_readiness),
                       'security_evolution', (SELECT jsonb_agg(jsonb_build_object(
                        'year', year,
                        'defense_success_rate', defense_success_rate,
                        'total_attacks', total_attacks,
                        'casualties', casualties,
                        'year_over_year_improvement', year_over_year_improvement
                                                               ))
                                              FROM security_evolution)
                                    )
       ) AS fortress_security_report;