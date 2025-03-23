WITH members_stats AS (SELECT expedition_id,
                              COUNT(*)                         AS total_members,
                              COUNT(*) FILTER (WHERE survived) AS survived_members,
                              ARRAY_AGG(dwarf_id)              AS member_ids
                       FROM expedition_members
                       GROUP BY expedition_id),
     artifacts_stats AS (SELECT expedition_id,
                                SUM(value)             AS total_artifacts_value,
                                ARRAY_AGG(artifact_id) AS artifact_ids
                         FROM expedition_artifacts
                         GROUP BY expedition_id),
     sites_stats AS (SELECT expedition_id,
                            COUNT(DISTINCT site_id)     AS discovered_sites,
                            ARRAY_AGG(DISTINCT site_id) AS site_ids
                     FROM expedition_sites
                     GROUP BY expedition_id),
     encounters_stats AS (SELECT expedition_id,
                                 COUNT(*)                        AS total_encounters,
                                 COUNT(*) FILTER (WHERE outcome) AS successful_encounters
                          FROM expedition_creatures
                          GROUP BY expedition_id),
     processing AS (SELECT exp.expedition_id,
                           exp.destination,
                           exp.status,
                           members_stats.survived_members * 1.0 /
                           COALESCE(members_stats.total_members, 1)           AS survival_rate,
                           COALESCE(artifacts_stats.total_artifacts_value, 0) AS artifacts_value,
                           COALESCE(sites_stats.discovered_sites, 0)          AS discovered_sites,
                           encounters_stats.successful_encounters * 1.0 /
                           COALESCE(encounters_stats.total_encounters, 1)     AS encounter_success_rate,
                           json_build_object(
                                   'member_ids', COALESCE(members_stats.member_ids, '[]'::json),
                                   'artifact_ids', COALESCE(artifacts_stats.artifact_ids, '[]'::json),
                                   'site_ids', COALESCE(sites_stats.site_ids, '[]'::json)
                           )                                                  AS related_entities
                    FROM expeditions exp
                             LEFT JOIN members_stats ON exp.expedition_id = members_stats.expedition_id
                             LEFT JOIN artifacts_stats ON exp.expedition_id = artifacts_stats.expedition_id
                             LEFT JOIN sites_stats ON exp.expedition_id = sites_stats.expedition_id
                             LEFT JOIN encounters_stats ON exp.expedition_id = encounters_stats.expedition_id)

SELECT *,
       ROUND(survival_rate * artifacts_value / 100 * discovered_sites / 10 * encounter_success_rate) AS overall_success_score
FROM processing
ORDER BY overall_success_score DESC;

-- Не понял, как посчитать "Опыт, полученный участниками (сравнение навыков до и после)", так как ни DWARF_SKILLS ни SKILLS не завязаны на даты экспедиции.