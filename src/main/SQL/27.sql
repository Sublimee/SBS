WITH caravan_trade AS (SELECT c.caravan_id,
                              c.civilization_type,
                              SUM(ABS(t_t.value)) AS trade_value,
                              SUM(t_t.value)      AS trade_balance
                       FROM caravans c
                                LEFT JOIN trade_transactions t_t ON c.caravan_id = t_t.caravan_id
                       GROUP BY c.caravan_id),
     caravan_diplomacy AS (SELECT d_e.caravan_id,
                                  AVG(CASE d_e.outcome
                                          WHEN 'positive' THEN 1
                                          WHEN 'neutral' THEN 0
                                          WHEN 'negative' THEN -1
                                          ELSE NULL
                                      END) AS diplomatic_score
                           FROM diplomatic_events d_e
                           GROUP BY d_e.caravan_id),
     civilization_summary AS (SELECT c_t.civilization_type,
                                     COUNT(DISTINCT c_t.caravan_id)     AS total_caravans,
                                     ARRAY_AGG(DISTINCT c_t.caravan_id) AS caravan_ids,
                                     SUM(c_t.trade_value)               AS total_trade_value,
                                     SUM(c_t.trade_balance)             AS trade_balance,
                                     COALESCE(CORR(
                                                      (c_t.trade_balance)::float,
                                                      c_d.diplomatic_score
                                              ), 0.0)                   AS diplomatic_correlation
                              FROM caravan_trade c_t
                                       LEFT JOIN caravan_diplomacy c_d ON c_t.caravan_id = c_d.caravan_id
                              GROUP BY c_t.civilization_type),


     civilization_trade_data AS (SELECT c_s.civilization_type,
                                        c_s.total_caravans,
                                        c_s.total_trade_value,
                                        c_s.trade_balance,
                                        CASE
                                            WHEN c_s.diplomatic_correlation >= 0.5 THEN 'Favorable'
                                            WHEN c_s.diplomatic_correlation <= -0.5 THEN 'Unfavorable'
                                            ELSE 'Neutral'
                                            END AS trade_relationship,
                                        c_s.diplomatic_correlation,
                                        c_s.caravan_ids
                                 FROM civilization_summary c_s),

     resource_dependency
         AS (SELECT r.type                                    AS resource_type, -- material_type в образце (между материалом и ресурсом нет связей)
                    SUM(s_c.quantity)                         AS total_imported,
                    COUNT(DISTINCT r.resource_id)             AS import_diversity,
                    ARRAY_AGG(DISTINCT r.resource_id)         AS resource_ids,
                    SUM(s_c.quantity * COALESCE(r.rarity, 0)) AS dependency_score
             FROM stockpile_contents s_c
                      JOIN resources r ON r.resource_id = s_c.resource_id
             WHERE s_c.is_imported = TRUE -- добавил, так как иначе не понял, как посчитать; возможно, надо как-то опираться на FORTRESS_RESOURCES и EXTRACTION_SITES
             GROUP BY r.type
             ORDER BY dependency_score DESC
             LIMIT 2),
     -- goods_id не связан ни с product_id, ни с resource_id, которые в свою очередь не понятно как увязать с caravan_items и fortress_items
     -- в таком случае непонятно, как посчитать export_ratio, а также наценку avg_markup
     export_effectiveness AS (...),
     trade_timeline AS (SELECT EXTRACT(YEAR FROM t_t.date)::int    AS year,
                               EXTRACT(QUARTER FROM t_t.date)::int AS quarter,
                               SUM(ABS(t_t.value))                 AS quarterly_value,
                               SUM(t_t.value)                      AS quarterly_balance,
                               COUNT(DISTINCT c.civilization_type) AS trade_diversity
                        FROM trade_transactions t_t
                                 JOIN caravans c ON c.caravan_id = t_t.caravan_id
                        GROUP BY year, quarter
                        ORDER BY year, quarter)
SELECT COUNT(DISTINCT с_s.civilization_type) FILTER (WHERE с_s.total_trade_value > 0) AS total_trading_partners,
       SUM(с_s.total_trade_value)                                                     AS all_time_trade_value,
       SUM(с_s.trade_balance)                                                         AS all_time_trade_balance,
       JSON_AGG(civilization_trade_data)                                              AS civilization_data,
       JSON_AGG(resource_dependency)                                                  AS critical_import_dependencies,
       JSON_AGG(export_effectiveness)                                                 AS export_effectiveness,
       JSON_AGG(trade_timeline)                                                       AS trade_timeline
FROM civilization_summary с_s
         JOIN resource_dependency ON true
         JOIN export_effectiveness ON true
         JOIN trade_timeline ON true;
