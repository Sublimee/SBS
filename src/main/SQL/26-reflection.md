Вопросы по эталонному решению:

* NULLIF(sbs.total_casualties, 1) при расчете casualty_exchange_ratio может привести к делению на 0
* enemy_casualties нет в таблице squad_battles, но используется: SUM(sb.enemy_casualties) AS total_enemy_casualties
* exit_reason и join_date нет в таблице squad_members, но используются:
```sql
squad_member_history AS (
    SELECT 
        sm.squad_id,
        COUNT(DISTINCT sm.dwarf_id) AS total_members_ever,
        COUNT(DISTINCT CASE WHEN sm.exit_reason IS NULL THEN sm.dwarf_id END) AS current_members,
        COUNT(DISTINCT CASE WHEN sm.exit_reason = 'Death' THEN sm.dwarf_id END) AS deaths,
        AVG(EXTRACT(DAY FROM (COALESCE(sm.exit_date, CURRENT_DATE) - sm.join_date))) AS avg_service_days
    FROM 
        squad_members sm
    GROUP BY 
        sm.squad_id
),
```

* кажется, что avg_equipment_quality с учетом того, что рядом есть поле quantity (количество?) нужно считать по формуле: ROUND(SUM(e.quality * s_e.quantity)::float / NULLIF(SUM(s_e.quantity), 0), 2) AS avg_equipment_quality. Иначе если у нас много качественных предметов, то их качество легко разбавить единичными "дешевками" по формуле AVG(e.quality::INTEGER) AS avg_equipment_quality
* effectiveness, duration_hours и date нет в таблице squad_training, но используются: 
```sql
squad_training_effectiveness AS (
    SELECT 
        st.squad_id,
        COUNT(st.schedule_id) AS total_training_sessions,
        AVG(st.effectiveness::DECIMAL) AS avg_training_effectiveness,
        SUM(st.duration_hours) AS total_training_hours,
        CORR(
            st.effectiveness::DECIMAL,
            CASE WHEN sb.outcome = 'Victory' THEN 1 ELSE 0 END
        ) AS training_battle_correlation
    FROM 
        squad_training st
    LEFT JOIN 
        squad_battles sb ON st.squad_id = sb.squad_id AND sb.date > st.date
    GROUP BY 
        st.squad_id
)
```

* level и date нет в DWARF_SKILLS, но используются:
```sql
squad_skill_progression AS (
    SELECT 
        sm.squad_id,
        sm.dwarf_id,
        AVG(ds_current.level - ds_join.level) AS avg_skill_improvement,
        MAX(ds_current.level) AS max_current_skill
    FROM 
        squad_members sm
    JOIN 
        dwarf_skills ds_join ON sm.dwarf_id = ds_join.dwarf_id AND ds_join.date <= sm.join_date
    JOIN 
        dwarf_skills ds_current ON sm.dwarf_id = ds_current.dwarf_id 
        AND ds_current.skill_id = ds_join.skill_id
        AND ds_current.date = (
            SELECT MAX(date) 
            FROM dwarf_skills 
            WHERE dwarf_id = sm.dwarf_id AND skill_id = ds_join.skill_id
        )
    JOIN 
        skills s ON ds_join.skill_id = s.skill_id
    WHERE 
        s.category IN ('Combat', 'Military')
    GROUP BY 
        sm.squad_id, sm.dwarf_id
)
```
