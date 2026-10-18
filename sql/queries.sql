-- 1. Список категорий (выборка)
SELECT
    id,
    name
FROM categories
ORDER BY name;

-- 2. Список пользователей (выборка)
SELECT
    id,
    name,
    email
FROM users
ORDER BY name;

-- 3. Категория «учеба» (WHERE)
SELECT
    id,
    name
FROM categories
WHERE name = 'учеба';

-- 4. Записи с настроением не ниже 8 (WHERE)
SELECT
    id,
    title,
    mood_score
FROM entries
WHERE mood_score >= 8
ORDER BY mood_score DESC;

-- 5. Публичные записи (WHERE)
SELECT
    id,
    title,
    is_private
FROM entries
WHERE is_private = 0
ORDER BY id;

-- 6. Полная информация о записи (JOIN)
SELECT
    entries.id,
    entries.title,
    entries.mood_score,
    users.name AS user_name,
    categories.name AS category_name,
    dates.value AS entry_date
FROM entries
JOIN users
    ON entries.user_id = users.id
JOIN categories
    ON entries.category_id = categories.id
JOIN dates
    ON entries.date_id = dates.id
ORDER BY dates.value;

-- 7. Публичные записи со связями (JOIN)
SELECT
    entries.id,
    entries.title,
    users.name AS user_name,
    categories.name AS category_name,
    dates.value AS entry_date
FROM entries
JOIN users
    ON entries.user_id = users.id
JOIN categories
    ON entries.category_id = categories.id
JOIN dates
    ON entries.date_id = dates.id
WHERE entries.is_private = 0
ORDER BY dates.value;

-- 8. Количество записей (агрегат)
SELECT
    COUNT(*) AS entries_count
FROM entries;

-- 9. Среднее настроение публичных записей (агрегат)
SELECT
    AVG(mood_score) AS avg_mood
FROM entries
WHERE is_private = 0;

-- 10. Количество записей по категориям (GROUP BY)
SELECT
    categories.name AS category_name,
    COUNT(entries.id) AS entries_count
FROM categories
LEFT JOIN entries
    ON categories.id = entries.category_id
GROUP BY categories.id, categories.name
ORDER BY entries_count DESC;

-- 11. Количество записей по датам (GROUP BY)
SELECT
    dates.value AS entry_date,
    COUNT(entries.id) AS entries_count
FROM dates
LEFT JOIN entries
    ON dates.id = entries.date_id
GROUP BY dates.id, dates.value
ORDER BY entry_date;

-- 12. Категории с более чем одной записью (HAVING)
SELECT
    categories.name AS category_name,
    COUNT(entries.id) AS entries_count
FROM categories
JOIN entries
    ON categories.id = entries.category_id
GROUP BY categories.id, categories.name
HAVING COUNT(entries.id) > 1
ORDER BY entries_count DESC;

-- 13. Записи на выбранную дату (параметр в Django)
SELECT
    entries.id,
    entries.title,
    users.name AS user_name,
    categories.name AS category_name
FROM entries
JOIN dates
    ON entries.date_id = dates.id
JOIN users
    ON entries.user_id = users.id
JOIN categories
    ON entries.category_id = categories.id
WHERE dates.value = '2026-09-08'
ORDER BY entries.title;
