Рефлексия по собственному решению
* Неправильно посчитал total_quantity_produced -> SUM(wp.quantity) AS total_quantity_produced.
* Не учел различные категории навыков WHERE s.category = 'Crafting'.
* Перемудрил с выражениями NULLIF(DATE_PART('day', MAX(w_p.production_date) - MIN(w_p.production_date)) + 1, 0).
* Не использовал avg в CORR.
* ORDER BY d_r.total_quantity_produced DESC не говорит об эффективности.
* Не везде правильно использовал NULLIF.

Вопросы к эталонному решению
* У PRODUCTS нет p.value.
* Тут не нужно +1 добавить MAX(wp.production_date) - MIN(wc.assignment_date)? Если даты совпадают, то должно быть 1, если разница в 1 день, то 2 и т.д.?
* created_by нет в products.
* Не до конца понял, почему так считается total_materials_consumed (не учитывается is_input).