ADVANCED_LESSONS = [
    {
        "id": "adv_l01",
        "difficulty": "advanced",
        "order": 17,
        "title": "Window Functions",
        "icon": "🪟",
        "tagline": "Aggregate without collapsing rows",
        "concept": "OVER() — computing rankings and running totals",
        "explanation": (
            "Window functions perform calculations across a 'window' of rows related to the current row, "
            "without collapsing them into a single result like GROUP BY does.\n\n"
            "The key clause is OVER(), which defines the window:\n"
            "• PARTITION BY — like GROUP BY, divides rows into groups\n"
            "• ORDER BY — defines row order within the window\n\n"
            "Common window functions:\n"
            "• ROW_NUMBER() — assigns unique sequential numbers\n"
            "• RANK() — assigns rank with gaps for ties\n"
            "• DENSE_RANK() — assigns rank without gaps\n"
            "• SUM() OVER () — running total\n"
            "• AVG() OVER () — moving average\n"
            "• LAG() / LEAD() — look at previous/next row"
        ),
        "syntax_template": "SELECT first_name, salary,\n  RANK() OVER (ORDER BY salary DESC) AS salary_rank,\n  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank\nFROM employees;",
        "annotated_example": {
            "query": "SELECT first_name, dept_id, salary,\n  ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_salary_rank\nFROM employees;",
            "lines": [
                {"line": "ROW_NUMBER()", "note": "Assigns 1, 2, 3... to each row"},
                {"line": "OVER (", "note": "Opens the window definition"},
                {"line": "PARTITION BY dept_id", "note": "Reset numbering for each department"},
                {"line": "ORDER BY salary DESC)", "note": "Highest salary = row 1 within each dept"},
            ],
        },
        "key_points": [
            "Window functions don't reduce rows — every row still appears.",
            "PARTITION BY in window functions is like GROUP BY for grouping, but you keep all rows.",
            "ROW_NUMBER() gives unique numbers; RANK() can have ties (and gaps); DENSE_RANK() has ties but no gaps.",
        ],
        "try_challenge_id": "adv_001",
    },
    {
        "id": "adv_l02",
        "difficulty": "advanced",
        "order": 18,
        "title": "LAG and LEAD",
        "icon": "↔️",
        "tagline": "Compare a row to the row before or after it",
        "concept": "Accessing adjacent rows with LAG and LEAD",
        "explanation": (
            "LAG(col) gets the value of col from the previous row in the window. "
            "LEAD(col) gets the value from the next row.\n\n"
            "This is essential for:\n"
            "• Month-over-month comparison (revenue this month vs last month)\n"
            "• Days between events (today's order date vs previous order date)\n"
            "• Detecting changes in status or category\n\n"
            "The first row in a LAG window and last row in a LEAD window return NULL "
            "because there's no prior/next row."
        ),
        "syntax_template": "SELECT customer_id, order_date,\n  LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order\nFROM orders;",
        "annotated_example": {
            "query": "SELECT customer_id, order_date,\n  LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order,\n  JULIANDAY(order_date) - JULIANDAY(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS days_since_last\nFROM orders;",
            "lines": [
                {"line": "LAG(order_date) OVER (...)", "note": "Previous order date for this customer"},
                {"line": "PARTITION BY customer_id", "note": "Reset the window per customer"},
                {"line": "JULIANDAY(...) - JULIANDAY(...)", "note": "Calculate days between orders"},
            ],
        },
        "key_points": [
            "LAG(col, n) gets n rows back (default 1).",
            "LEAD(col, n) gets n rows forward (default 1).",
            "LAG/LEAD return NULL at the edges of the window.",
        ],
        "try_challenge_id": "adv_005",
    },
    {
        "id": "adv_l03",
        "difficulty": "advanced",
        "order": 19,
        "title": "CTEs — Common Table Expressions",
        "icon": "📝",
        "tagline": "Name a subquery and reuse it",
        "concept": "WITH clause for readable, reusable query blocks",
        "explanation": (
            "A CTE (Common Table Expression) lets you define a named temporary result set "
            "using the WITH keyword. You can then refer to that name in the main query — "
            "making complex queries much easier to read and write.\n\n"
            "CTEs are also great for multi-step analysis: compute something in step 1, "
            "use it in step 2, and so on. You can chain multiple CTEs."
        ),
        "syntax_template": "WITH cte_name AS (\n  SELECT ...\n  FROM ...\n)\nSELECT *\nFROM cte_name;",
        "annotated_example": {
            "query": "WITH dept_stats AS (\n  SELECT dept_id, AVG(salary) AS avg_sal, COUNT(*) AS headcount\n  FROM employees\n  GROUP BY dept_id\n)\nSELECT d.name, ds.avg_sal, ds.headcount\nFROM dept_stats ds\nJOIN departments d ON ds.dept_id = d.id\nORDER BY ds.avg_sal DESC;",
            "lines": [
                {"line": "WITH dept_stats AS (", "note": "Name this temporary result 'dept_stats'"},
                {"line": "  SELECT dept_id, AVG(salary) ...", "note": "The CTE query — runs first"},
                {"line": ")", "note": "End the CTE definition"},
                {"line": "SELECT ... FROM dept_stats", "note": "Use the CTE like a regular table"},
            ],
        },
        "key_points": [
            "CTEs are like named subqueries at the top of the query.",
            "Multiple CTEs: WITH cte1 AS (...), cte2 AS (...) SELECT ...",
            "CTEs only exist for the duration of that one query.",
        ],
        "try_challenge_id": "adv_008",
    },
    {
        "id": "adv_l04",
        "difficulty": "advanced",
        "order": 20,
        "title": "Self Joins",
        "icon": "🪞",
        "tagline": "Join a table to itself",
        "concept": "Using the same table twice in a JOIN",
        "explanation": (
            "A self join joins a table to itself. "
            "This is necessary when a table has a column that references another row in the same table — "
            "like the manager_id in the employees table that points to another employee's id.\n\n"
            "You must alias the table twice to distinguish the two 'copies'."
        ),
        "syntax_template": "SELECT e.first_name AS employee, m.first_name AS manager\nFROM employees e\nJOIN employees m ON e.manager_id = m.id;",
        "annotated_example": {
            "query": "SELECT\n  e.first_name || ' ' || e.last_name AS employee,\n  m.first_name || ' ' || m.last_name AS manager\nFROM employees e\nJOIN employees m ON e.manager_id = m.id;",
            "lines": [
                {"line": "FROM employees e", "note": "First copy — the employees"},
                {"line": "JOIN employees m ON e.manager_id = m.id;", "note": "Second copy — the managers (same table!)"},
                {"line": "e.first_name ... m.first_name", "note": "Alias prefix tells SQL which copy to read from"},
            ],
        },
        "key_points": [
            "Alias both instances of the table: e for employee, m for manager.",
            "Use INNER JOIN to only show employees who have a manager.",
            "Use LEFT JOIN to also show employees without a manager.",
        ],
        "try_challenge_id": "adv_012",
    },
    {
        "id": "adv_l05",
        "difficulty": "advanced",
        "order": 21,
        "title": "Set Operations: UNION, INTERSECT, EXCEPT",
        "icon": "⭕",
        "tagline": "Combine or compare result sets from different queries",
        "concept": "UNION, INTERSECT, EXCEPT",
        "explanation": (
            "Set operations combine two SELECT results:\n\n"
            "• UNION — all rows from both queries, duplicates removed\n"
            "• UNION ALL — all rows from both queries, duplicates kept\n"
            "• INTERSECT — only rows that appear in both\n"
            "• EXCEPT — rows in the first query but not the second\n\n"
            "Both queries must have the same number of columns with compatible types."
        ),
        "syntax_template": "-- Union:\nSELECT city FROM customers\nUNION\nSELECT location FROM departments;\n\n-- Except (rows in A not in B):\nSELECT id FROM products\nEXCEPT\nSELECT product_id FROM order_items;",
        "annotated_example": {
            "query": "SELECT id FROM products\nEXCEPT\nSELECT product_id FROM order_items;",
            "lines": [
                {"line": "SELECT id FROM products", "note": "All product ids"},
                {"line": "EXCEPT", "note": "Remove any ids that appear in the next query"},
                {"line": "SELECT product_id FROM order_items;", "note": "Product ids that have been ordered"},
            ],
        },
        "key_points": [
            "Both queries must have the same number and compatible types of columns.",
            "UNION removes duplicates; UNION ALL is faster and keeps them.",
            "EXCEPT is the 'A minus B' operation.",
        ],
        "try_challenge_id": "adv_014",
    },
    {
        "id": "adv_l06",
        "difficulty": "advanced",
        "order": 22,
        "title": "EXISTS and Correlated Subqueries",
        "icon": "❓",
        "tagline": "Check if related data exists",
        "concept": "EXISTS, NOT EXISTS, and correlated subqueries",
        "explanation": (
            "EXISTS returns true if the subquery produces any rows at all — it doesn't care what the rows are.\n\n"
            "A correlated subquery references the outer query's current row. "
            "This lets the inner query check something specific to that row.\n\n"
            "Example: 'Find employees whose salary is above their own department's average' "
            "requires looking up the average for that employee's specific department — "
            "a different calculation for each row."
        ),
        "syntax_template": "-- EXISTS:\nSELECT first_name FROM customers\nWHERE EXISTS (\n  SELECT 1 FROM orders\n  WHERE orders.customer_id = customers.id\n);\n\n-- Correlated subquery:\nSELECT first_name, salary FROM employees e\nWHERE salary > (\n  SELECT AVG(salary) FROM employees e2\n  WHERE e2.dept_id = e.dept_id\n);",
        "annotated_example": {
            "query": "SELECT first_name, salary\nFROM employees e\nWHERE salary > (\n  SELECT AVG(salary)\n  FROM employees e2\n  WHERE e2.dept_id = e.dept_id\n);",
            "lines": [
                {"line": "WHERE salary > (SELECT AVG(salary)", "note": "Compare to a computed average"},
                {"line": "FROM employees e2", "note": "Same table, different alias"},
                {"line": "WHERE e2.dept_id = e.dept_id", "note": "Reference the OUTER query's dept_id — this is the correlation"},
            ],
        },
        "key_points": [
            "EXISTS is often faster than IN for large datasets.",
            "SELECT 1 is conventional inside EXISTS — the value doesn't matter, just whether rows exist.",
            "Correlated subqueries reference the outer query and re-run per row.",
        ],
        "try_challenge_id": "adv_017",
    },
]
