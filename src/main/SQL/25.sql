WITH product_stats AS (SELECT w_p.workshop_id,
                              COUNT(*) AS total_quantity_produced,
                              SUM(p.quality * w_p.quantity) AS total_production_value,
                              MIN(w_p.production_date) AS first_production_date,
                              MAX(w_p.production_date) AS last_production_date,
                              ARRAY_AGG(DISTINCT w_p.product_id) AS product_ids,
                              COUNT(DISTINCT w_p.production_date) AS active_days,
                              NULLIF(DATE_PART('day', MAX(w_p.production_date) - MIN(w_p.production_date)) + 1, 0) AS total_days,
                              ROUND(
                                      COUNT(DISTINCT w_p.production_date) * 100.0 /
                                      NULLIF(DATE_PART('day', MAX(w_p.production_date) - MIN(w_p.production_date)) + 1, 0),
                                      2
                              ) AS workshop_utilization_percent
                       FROM workshop_products w_p
                                JOIN products p ON w_p.product_id = p.product_id
                       GROUP BY w_p.workshop_id),
     material_stats AS (SELECT w_m.workshop_id,
                               SUM(w_m.quantity) FILTER (WHERE w_m.is_input)     AS total_materials_used,
                               SUM(w_m.quantity) FILTER (WHERE NOT w_m.is_input) AS total_materials_output,
                               ARRAY_AGG(DISTINCT w_m.material_id)               AS material_ids
                        FROM workshop_materials w_m
                        GROUP BY w_m.workshop_id),
     crafts_stats AS (SELECT w_cd.workshop_id,
                             COUNT(DISTINCT w_cd.dwarf_id)     AS num_craftsdwarves,
                             ARRAY_AGG(DISTINCT w_cd.dwarf_id) AS craftsdwarf_ids,
                             AVG(ds.level)                     AS average_craftsdwarf_skill
                      FROM workshop_craftsdwarves w_cd
                               JOIN dwarf_skills ds ON ds.dwarf_id = w_cd.dwarf_id
                      GROUP BY w_cd.workshop_id),
     daily_rates AS (SELECT p_s.workshop_id,
                            ROUND((p_s.total_quantity_produced * 1.0) / p_s.total_days, 2) AS daily_production_rate
                     FROM product_stats p_s),
     project_stats AS (SELECT   prj.workshop_id,
                            ARRAY_AGG(DISTINCT prj.project_id) AS project_ids
                          FROM projects prj
                          GROUP BY prj.workshop_id
                        ),
     skill_quality_corr AS (SELECT w_p.workshop_id,
                                   CORR(d_s.level::FLOAT, p.quality::FLOAT) AS skill_quality_correlation
                            FROM workshop_products w_p
                                     JOIN products p ON w_p.product_id = p.product_id
                                     JOIN workshop_craftsdwarves w_cd ON w_cd.workshop_id = w_p.workshop_id
                                     JOIN dwarf_skills d_s ON d_s.dwarf_id = w_cd.dwarf_id
                            GROUP BY w_p.workshop_id)

SELECT w.workshop_id,
       w.name                                                                         AS workshop_name,
       w.type                                                                         AS workshop_type,
       c_s.num_craftsdwarves AS num_craftsdwarves,
       p_s.total_quantity_produced,
       p_s.total_production_value,
       d_r.daily_production_rate,
       ROUND(p_s.total_production_value * 1.0 / NULLIF(m_s.total_materials_used, 0), 2) AS value_per_material_unit,
       p_s.workshop_utilization_percent,
       ROUND(m_s.total_materials_output * 1.0 / NULLIF(m_s.total_materials_used, 1), 2) AS material_conversion_ratio,
       c_s.average_craftsdwarf_skill,
       COALESCE(s_q_c.skill_quality_correlation, 0)                                     AS skill_quality_correlation,
       json_build_object(
               'craftsdwarf_ids', c_s.craftsdwarf_ids,
               'product_ids', p_s.product_ids,
               'material_ids', m_s.material_ids,
               'project_ids', prj_s.project_ids
       )                                                                              AS related_entities

FROM workshops w
         LEFT JOIN product_stats p_s ON w.workshop_id = p_s.workshop_id
         LEFT JOIN material_stats m_s ON w.workshop_id = m_s.workshop_id
         LEFT JOIN crafts_stats c_s ON w.workshop_id = c_s.workshop_id
         LEFT JOIN daily_rates d_r ON w.workshop_id = d_r.workshop_id
         LEFT JOIN skill_quality_corr s_q_c ON w.workshop_id = s_q_c.workshop_id
         LEFT JOIN project_stats prj_s ON w.workshop_id = prj_s.workshop_id
ORDER BY d_r.total_quantity_produced DESC;
