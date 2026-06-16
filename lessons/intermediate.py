INTERMEDIATE_LESSONS = [
    {
        "id": "int_l01",
        "difficulty": "intermediate",
        "order": 9,
        "title": "Aggregate Functions",
        "icon": "➕",
        "tagline": "COUNT, SUM, AVG, MIN, MAX",
        "concept": "Computing summary statistics across rows",
        "explanation": (
            "Aggregate functions compute a single value from multiple rows. "
            "They're how you answer questions like 'how many orders were placed?' or 'what's the average salary?'\n\n"
            "The five core aggregates:\n"
            "• COUNT(*) — count rows\n"
            "• SUM(col) — add up values\n"
            "• AVG(col) — compute the average\n"
            "• MIN(col) — find the smallest value\n"
            "• MAX(col) — find the largest value"
        ),
        "syntax_template": "SELECT COUNT(*), SUM(salary), AVG(salary), MIN(salary), MAX(salary)\nFROM employees;",
        "annotated_example": {
            "query": "SELECT\n  COUNT(*) AS total,\n  AVG(salary) AS avg_sal,\n  MAX(salary) AS top_sal\nFROM employees;",
            "lines": [
                {"line": "COUNT(*) AS total", "note": "Total number of rows"},
                {"line": "AVG(salary) AS avg_sal", "note": "Average across all rows"},
                {"line": "MAX(salary) AS top_sal", "note": "Single highest value"},
            ],
        },
        "key_points": [
            "COUNT(*) counts all rows; COUNT(column) skips NULLs.",
            "You can use multiple aggregates in one query.",
            "Aggregate functions collapse all rows into one result row.",
        ],
        "try_challenge_id": "int_001",
    },
    {
        "id": "int_l02",
        "difficulty": "intermediate",
        "order": 10,
        "title": "GROUP BY — Aggregating by Category",
        "icon": "📦",
        "tagline": "Break your aggregates into groups",
        "concept": "Grouping rows before aggregating",
        "explanation": (
            "GROUP BY splits rows into groups based on column values, then applies an aggregate function "
            "to each group separately. This answers questions like 'how many employees are in each department?' "
            "or 'what's the total revenue by product category?'\n\n"
            "The rule: every column in SELECT must either be in GROUP BY or be inside an aggregate function."
        ),
        "syntax_template": "SELECT dept_id, COUNT(*) AS emp_count\nFROM employees\nGROUP BY dept_id;",
        "annotated_example": {
            "query": "SELECT dept_id, COUNT(*) AS emp_count\nFROM employees\nGROUP BY dept_id\nORDER BY emp_count DESC;",
            "lines": [
                {"line": "SELECT dept_id, COUNT(*)", "note": "For each dept, count its rows"},
                {"line": "GROUP BY dept_id", "note": "Create one group per unique dept_id"},
                {"line": "ORDER BY emp_count DESC;", "note": "Biggest departments first"},
            ],
        },
        "key_points": [
            "Every non-aggregate column in SELECT must be in GROUP BY.",
            "GROUP BY can group by multiple columns: GROUP BY dept_id, is_active",
            "You can ORDER BY an aggregate: ORDER BY COUNT(*) DESC",
        ],
        "try_challenge_id": "int_007",
    },
    {
        "id": "int_l03",
        "difficulty": "intermediate",
        "order": 11,
        "title": "HAVING — Filtering Groups",
        "icon": "🚦",
        "tagline": "WHERE for groups, not rows",
        "concept": "Filtering aggregated results",
        "explanation": (
            "WHERE filters rows before grouping. HAVING filters groups after grouping. "
            "You can't use WHERE to filter on aggregate results like COUNT(*) — "
            "that's what HAVING is for.\n\n"
            "Example: 'departments with more than 10 employees' can't be answered with WHERE, "
            "because you need to count first, then filter."
        ),
        "syntax_template": "SELECT dept_id, COUNT(*) AS emp_count\nFROM employees\nGROUP BY dept_id\nHAVING COUNT(*) > 10;",
        "annotated_example": {
            "query": "SELECT status, SUM(total_amount) AS revenue\nFROM orders\nGROUP BY status\nHAVING SUM(total_amount) > 50000;",
            "lines": [
                {"line": "GROUP BY status", "note": "Group rows by order status"},
                {"line": "HAVING SUM(total_amount) > 50000;", "note": "Keep only groups with total > 50k"},
            ],
        },
        "key_points": [
            "HAVING comes after GROUP BY and before ORDER BY.",
            "Use WHERE for row-level filtering, HAVING for group-level filtering.",
            "Both can appear in the same query.",
        ],
        "try_challenge_id": "int_013",
    },
    {
        "id": "int_l04",
        "difficulty": "intermediate",
        "order": 12,
        "title": "INNER JOIN — Connecting Tables",
        "icon": "🔗",
        "tagline": "Combine related data from two tables",
        "concept": "Joining tables on a shared key",
        "explanation": (
            "Most data is spread across multiple tables, linked by keys. "
            "An INNER JOIN combines rows from two tables where a key column matches.\n\n"
            "The pattern: employees have a dept_id; departments have an id. "
            "JOIN on those to get employee rows enriched with department data.\n\n"
            "INNER JOIN only returns rows that have a match in BOTH tables. "
            "If an employee has a dept_id with no matching department, they won't appear."
        ),
        "syntax_template": "SELECT e.first_name, d.name AS dept\nFROM employees e\nJOIN departments d ON e.dept_id = d.id;",
        "annotated_example": {
            "query": "SELECT e.first_name, e.salary, d.name AS dept_name\nFROM employees e\nJOIN departments d ON e.dept_id = d.id;",
            "lines": [
                {"line": "FROM employees e", "note": "Start with employees, alias as 'e'"},
                {"line": "JOIN departments d ON e.dept_id = d.id;", "note": "Match each employee's dept_id to departments.id"},
                {"line": "SELECT e.first_name, d.name", "note": "Columns from both tables, prefixed by alias"},
            ],
        },
        "key_points": [
            "Alias tables (AS e, AS d) to keep queries readable.",
            "Prefix columns with alias when tables share column names: e.id vs d.id",
            "You can JOIN more than two tables by chaining JOIN clauses.",
        ],
        "try_challenge_id": "int_016",
    },
    {
        "id": "int_l05",
        "difficulty": "intermediate",
        "order": 13,
        "title": "LEFT JOIN — Keeping All Left Rows",
        "icon": "⬅️",
        "tagline": "Include rows even when there's no match",
        "concept": "LEFT JOIN vs INNER JOIN",
        "explanation": (
            "LEFT JOIN returns all rows from the left table (the one in FROM), "
            "plus matching rows from the right table. "
            "When there's no match in the right table, those columns come back as NULL.\n\n"
            "Classic use case: 'find customers who have never placed an order.' "
            "LEFT JOIN orders, then filter WHERE orders.id IS NULL — "
            "those are the customers with no matching order."
        ),
        "syntax_template": "SELECT c.first_name, o.id AS order_id\nFROM customers c\nLEFT JOIN orders o ON c.id = o.customer_id;",
        "annotated_example": {
            "query": "SELECT c.first_name, o.id AS order_id\nFROM customers c\nLEFT JOIN orders o ON c.id = o.customer_id\nWHERE o.id IS NULL;",
            "lines": [
                {"line": "FROM customers c", "note": "Left table — ALL customers will appear"},
                {"line": "LEFT JOIN orders o ON c.id = o.customer_id", "note": "Attach orders where they exist"},
                {"line": "WHERE o.id IS NULL;", "note": "Keep only customers with NO matching order"},
            ],
        },
        "key_points": [
            "LEFT JOIN = all left rows + matching right rows (NULL when no match)",
            "INNER JOIN = only rows that match in both tables",
            "The 'find missing' pattern: LEFT JOIN + WHERE right_table.key IS NULL",
        ],
        "try_challenge_id": "int_021",
    },
    {
        "id": "int_l06",
        "difficulty": "intermediate",
        "order": 14,
        "title": "Subqueries",
        "icon": "🪆",
        "tagline": "Queries inside queries",
        "concept": "Using a SELECT result inside another SELECT",
        "explanation": (
            "A subquery is a query nested inside another query. "
            "The inner query runs first and its result is used by the outer query.\n\n"
            "Common uses:\n"
            "• WHERE value > (SELECT AVG(value) FROM table)\n"
            "• WHERE id IN (SELECT id FROM other_table WHERE condition)\n\n"
            "Subqueries in WHERE must return a single value (for comparisons like > or =) "
            "or a list of values (for IN)."
        ),
        "syntax_template": "SELECT *\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);",
        "annotated_example": {
            "query": "SELECT first_name, salary\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);",
            "lines": [
                {"line": "(SELECT AVG(salary) FROM employees)", "note": "Inner query: runs first, returns one number"},
                {"line": "WHERE salary > ...", "note": "Outer query: compares each row's salary to that number"},
            ],
        },
        "key_points": [
            "Subquery in parentheses runs first.",
            "For IN, the subquery can return multiple rows.",
            "For = or >, the subquery must return exactly one value.",
        ],
        "try_challenge_id": "int_023",
    },
    {
        "id": "int_l07",
        "difficulty": "intermediate",
        "order": 15,
        "title": "CASE WHEN — Conditional Logic",
        "icon": "🔀",
        "tagline": "If-then-else logic inside SQL",
        "concept": "Conditional expressions with CASE WHEN",
        "explanation": (
            "CASE WHEN lets you add conditional logic to your SELECT clause — "
            "like an if/else statement that runs per row.\n\n"
            "Use it to create labels ('High', 'Medium', 'Low'), "
            "convert codes to readable values, or create flag columns."
        ),
        "syntax_template": "SELECT name,\n  CASE\n    WHEN price > 500 THEN 'Expensive'\n    WHEN price > 100 THEN 'Mid-range'\n    ELSE 'Budget'\n  END AS price_tier\nFROM products;",
        "annotated_example": {
            "query": "SELECT first_name,\n  CASE\n    WHEN salary > 100000 THEN 'High'\n    WHEN salary > 60000 THEN 'Mid'\n    ELSE 'Low'\n  END AS pay_band\nFROM employees;",
            "lines": [
                {"line": "CASE", "note": "Start the conditional expression"},
                {"line": "WHEN salary > 100000 THEN 'High'", "note": "First condition checked — if true, return 'High'"},
                {"line": "WHEN salary > 60000 THEN 'Mid'", "note": "Only checked if first was false"},
                {"line": "ELSE 'Low'", "note": "Default if no WHEN matched"},
                {"line": "END AS pay_band", "note": "Close with END, give it an alias"},
            ],
        },
        "key_points": [
            "WHEN conditions are checked in order — first match wins.",
            "ELSE is optional; without it, unmatched rows get NULL.",
            "CASE ... END must always be closed with END.",
        ],
        "try_challenge_id": "int_027",
    },
    {
        "id": "int_l08",
        "difficulty": "intermediate",
        "order": 16,
        "title": "Date & String Functions",
        "icon": "📅",
        "tagline": "Manipulate text and dates in SQL",
        "concept": "Built-in functions for string and date operations",
        "explanation": (
            "SQL includes built-in functions to work with text and dates.\n\n"
            "String functions:\n"
            "• UPPER(str) / LOWER(str) — change case\n"
            "• LENGTH(str) — count characters\n"
            "• SUBSTR(str, start, length) — extract a portion\n"
            "• str1 || str2 — concatenate strings (SQLite uses ||)\n\n"
            "Date functions (SQLite):\n"
            "• STRFTIME('%Y', date_col) — extract year\n"
            "• STRFTIME('%Y-%m', date_col) — year-month\n"
            "• JULIANDAY(date) — convert to a float for date math\n"
            "• DATE('now') — today's date"
        ),
        "syntax_template": "-- Concatenate:\nSELECT first_name || ' ' || last_name AS full_name\nFROM employees;\n\n-- Extract year:\nSELECT STRFTIME('%Y', hire_date) AS hire_year\nFROM employees;",
        "annotated_example": {
            "query": "SELECT\n  first_name || ' ' || last_name AS full_name,\n  STRFTIME('%Y', hire_date) AS hire_year\nFROM employees;",
            "lines": [
                {"line": "first_name || ' ' || last_name AS full_name", "note": "Concatenate with a space in between"},
                {"line": "STRFTIME('%Y', hire_date) AS hire_year", "note": "Extract just the year from the date"},
            ],
        },
        "key_points": [
            "|| is the concatenation operator in SQLite (use CONCAT() in MySQL/Postgres).",
            "STRFTIME format codes: %Y=year, %m=month, %d=day, %H=hour.",
            "Date arithmetic: JULIANDAY('2024-01-15') - JULIANDAY(hire_date) = days employed.",
        ],
        "try_challenge_id": "int_030",
    },
]
