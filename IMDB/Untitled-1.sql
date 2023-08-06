
SELECT primary_title, name,premiered FROM titles INNER JOIN crew ON  titles.title_id = crew.title_id INNER JOIN people ON crew.person_id = people.person_id 
WHERE primary_title = "Oppenheimer" AND crew.category = 'director' ORDER BY premiered DESC;

SELECT primary_title FROM titles INNER JOIN ratings ON titles.title_id = ratings.title_id WHERE titles.title_id IN (SELECT title_id FROM crew WHERE category = 'director' AND person_id = (SELECT person_id FROM people WHERE name = 'Woody Allen' AND born = 1935)) ORDER BY ratings.rating DESC;


SELECT * FROM (SELECT ROW_NUMBER() OVER(ORDER BY ratings.rating * ratings.votes DESC) as id, titles.title_id,primary_title,premiered,ended,type,runtime_minutes,genres,ratings.rating FROM titles INNER JOIN ratings ON titles.title_id = ratings.title_id) WHERE id BETWEEN 20 AND 30;

SELECT id, title_id, type, primary_title, is_adult, premiered, ended, runtime_minutes, genres, rating, votes FROM (SELECT ROW_NUMBER() OVER(ORDER BY ratings.rating * ratings.votes DESC) as id, * FROM titles INNER JOIN ratings ON titles.title_id = ratings.title_id WHERE primary_title LIKE "%?%") WHERE id BETWEEN ? AND ?;
