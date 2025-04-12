Вопросы по эталонному решению:

* Не совсем понял, почему trade_year и группировка EXTRACT(YEAR FROM c.arrival_date) в civilization_trade_history считаются именно по году прибытия. Кажется, если караван был в пути долго, то мы это не учтем в статистике торговли по годам. С другой стороны, если не рассматривать промежуточные результаты незавершенных караванов, пока они не вернулись в крепость, то такой подсчет логичен.
* Из таблицы caravan_goods не считывается, что type отвечает за экспорт/импорт.
* Непонятно, как соотносятся value из trade_transactions и value из caravan_goods.
* В caravan_goods нет material_type и price_fluctuation, но используются:
```sql
fortress_resource_dependency AS (
    SELECT 
        cg.material_type,
        ...
        AVG(cg.price_fluctuation) AS avg_price_fluctuation,
```
* material_id нигде не представлен в роли (PK).
* При расчете fortress_resource_dependency опираемся на зависимость от товаров, а не ресурсов. Логично проводить расчет по caravan_goods, но с формальной точки зрения нужно описаться на таблицу resources.
* relationship_change нет в diplomatic_events, но используется:
```sql
diplomatic_trade_correlation AS (
        ...
        CORR(
            de.relationship_change,
```
* В products нет workshop_id и original_product_id, но используются:
```sql
workshop_export_effectiveness AS (
    ...
    JOIN 
        workshops w ON p.workshop_id = w.workshop_id
    LEFT JOIN 
        caravan_goods cg ON p.product_id = cg.original_product_id AND cg.type = 'Export'
```
* В trade_transactions нет balance_direction но используются:
```sql
trade_timeline AS (
    SELECT 
        ...
        SUM(CASE WHEN tt.balance_direction = 'Import' THEN tt.value ELSE 0 END) AS import_value,
        SUM(CASE WHEN tt.balance_direction = 'Export' THEN tt.value ELSE 0 END) AS export_value,
```
* Можно ли считать, что цивилизация участвует в "total_trading_partners", если она не сделала ни одной транзакции?  
```sql
(SELECT COUNT(DISTINCT civilization_type) FROM caravans) AS total_trading_partners,
```
* Эталонное решение содержит гораздо больше информации в выводе, чем в блоке "Возможный вариант выдачи".
