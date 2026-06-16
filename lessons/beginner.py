BEGINNER_LESSONS = [
    {
        "id": "beg_l01",
        "difficulty": "beginner",
        "order": 1,
        "title": "What is SQL?",
        "icon": "🗃️",
        "tagline": "The language that talks to databases",
        "concept": "Understanding what SQL does and why it matters",
        "explanation": (
            "SQL (Structured Query Language) is the language you use to communicate with a database. "
            "Think of a database as a collection of organized spreadsheets called tables. "
            "SQL lets you ask questions like 'give me all the sales from last month' or "
            "'which customers spent the most money?' — and get exact answers instantly, even from millions of rows.\n\n"
            "Every major company uses SQL. Whether you're at a startup or a Fortune 500, "
            "data lives in databases, and analysts use SQL every day to pull insights from that data."
        ),
        "syntax_template": "SELECT columns\nFROM table_name;",
        "annotated_example": {
            "query": "SELECT first_name, last_name\nFROM employees;",
            "lines": [
                {"line": "SELECT first_name, last_name", "note": "List the columns you want to see"},
                {"line": "FROM employees;", "note": "Name the table where those columns live"},
            ],
        },
        "key_points": [
            "SQL is not case-sensitive for keywords (select = SELECT), but it's conventional to capitalize them.",
            "A semicolon ; ends a SQL statement (optional in most single-query tools).",
            "Columns are separated by commas.",
        ],
        "try_challenge_id": "beg_001",
    },
    {
        "id": "beg_l02",
        "difficulty": "beginner",
        "order": 2,
        "title": "SELECT — Choosing What to See",
        "icon": "👁️",
        "tagline": "Tell SQL exactly which columns you want",
        "concept": "Selecting specific columns vs all columns",
        "explanation": (
            "SELECT is the most fundamental SQL command. It tells the database which columns of data "
            "you want returned. You can select specific columns by naming them, or use * to get everything.\n\n"
            "In practice, always prefer naming specific columns — it makes your query faster and clearer. "
            "SELECT * is great for exploration but not for production reports."
        ),
        "syntax_template": "-- Specific columns:\nSELECT column1, column2\nFROM table_name\n\n-- All columns:\nSELECT *\nFROM table_name",
        "annotated_example": {
            "query": "SELECT first_name, salary\nFROM employees;",
            "lines": [
                {"line": "SELECT first_name, salary", "note": "Only return these two columns (not all 8 in the table)"},
                {"line": "FROM employees;", "note": "Look in the employees table"},
            ],
        },
        "key_points": [
            "* means 'all columns' — handy for exploration.",
            "Naming columns is faster and self-documenting.",
            "You can rename columns using AS: SELECT salary AS monthly_pay",
        ],
        "try_challenge_id": "beg_002",
    },
    {
        "id": "beg_l03",
        "difficulty": "beginner",
        "order": 3,
        "title": "WHERE — Filtering Rows",
        "icon": "🔍",
        "tagline": "Only return rows that match your conditions",
        "concept": "Filtering data with WHERE",
        "explanation": (
            "WHERE is how you filter rows. Without it, your query returns everything in the table. "
            "With it, you only get the rows that match your condition.\n\n"
            "WHERE works with comparison operators: = (equal), != (not equal), > (greater than), "
            "< (less than), >= (greater than or equal), <= (less than or equal).\n\n"
            "Text values must be wrapped in single quotes. Numbers don't need quotes."
        ),
        "syntax_template": "SELECT columns\nFROM table_name\nWHERE condition;",
        "annotated_example": {
            "query": "SELECT first_name, salary\nFROM employees\nWHERE salary > 80000;",
            "lines": [
                {"line": "SELECT first_name, salary", "note": "Columns to return"},
                {"line": "FROM employees", "note": "Table to search"},
                {"line": "WHERE salary > 80000;", "note": "Only rows where salary exceeds 80,000"},
            ],
        },
        "key_points": [
            "Text needs single quotes: WHERE status = 'active'",
            "Numbers don't: WHERE salary > 80000",
            "NULL values need special handling: WHERE manager_id IS NULL (not = NULL)",
        ],
        "try_challenge_id": "beg_012",
    },
    {
        "id": "beg_l04",
        "difficulty": "beginner",
        "order": 4,
        "title": "AND, OR, NOT — Combining Conditions",
        "icon": "🔗",
        "tagline": "Filter with multiple rules at once",
        "concept": "Combining WHERE conditions",
        "explanation": (
            "Real queries rarely filter on just one thing. AND requires both conditions to be true. "
            "OR requires at least one to be true. NOT inverts a condition.\n\n"
            "Use parentheses to control evaluation order — just like math. "
            "AND is evaluated before OR, so parentheses prevent surprises."
        ),
        "syntax_template": "WHERE condition1 AND condition2\nWHERE condition1 OR condition2\nWHERE NOT condition",
        "annotated_example": {
            "query": "SELECT first_name, salary, is_active\nFROM employees\nWHERE is_active = 1 AND salary > 60000;",
            "lines": [
                {"line": "WHERE is_active = 1 AND salary > 60000;", "note": "Both conditions must be true"},
            ],
        },
        "key_points": [
            "AND: both sides must be true",
            "OR: at least one side must be true",
            "IN ('a','b','c') is cleaner than OR when checking many values",
            "BETWEEN 50000 AND 75000 is inclusive of both endpoints",
        ],
        "try_challenge_id": "beg_019",
    },
    {
        "id": "beg_l05",
        "difficulty": "beginner",
        "order": 5,
        "title": "ORDER BY — Sorting Results",
        "icon": "📊",
        "tagline": "Control the order rows come back in",
        "concept": "Sorting with ORDER BY",
        "explanation": (
            "Without ORDER BY, SQL returns rows in no guaranteed order. "
            "ORDER BY lets you sort the results by one or more columns.\n\n"
            "ASC (ascending) is the default — smallest to largest, A to Z, oldest to newest. "
            "DESC (descending) reverses it — largest to smallest, Z to A, newest to oldest."
        ),
        "syntax_template": "SELECT columns\nFROM table_name\nORDER BY column1 ASC, column2 DESC;",
        "annotated_example": {
            "query": "SELECT first_name, last_name, salary\nFROM employees\nORDER BY salary DESC;",
            "lines": [
                {"line": "ORDER BY salary DESC;", "note": "Sort by salary, highest first (descending)"},
            ],
        },
        "key_points": [
            "ASC is default — you don't have to write it, but it's clearer when you do.",
            "You can sort by multiple columns: ORDER BY dept_id, salary DESC",
            "ORDER BY comes after WHERE in clause order.",
        ],
        "try_challenge_id": "beg_030",
    },
    {
        "id": "beg_l06",
        "difficulty": "beginner",
        "order": 6,
        "title": "LIMIT — Capping Results",
        "icon": "✂️",
        "tagline": "Only return a set number of rows",
        "concept": "Using LIMIT and OFFSET",
        "explanation": (
            "LIMIT caps how many rows are returned. This is essential for previewing data "
            "and for 'top N' questions like 'show me the top 5 customers'.\n\n"
            "OFFSET lets you skip rows — useful for pagination. "
            "LIMIT 10 OFFSET 20 means 'skip 20 rows, then give me the next 10'."
        ),
        "syntax_template": "SELECT columns\nFROM table_name\nORDER BY column\nLIMIT 10;\n\n-- With pagination:\nLIMIT 10 OFFSET 20;",
        "annotated_example": {
            "query": "SELECT first_name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT 5;",
            "lines": [
                {"line": "ORDER BY salary DESC", "note": "Sort highest salary first"},
                {"line": "LIMIT 5;", "note": "Only return the top 5 rows"},
            ],
        },
        "key_points": [
            "LIMIT comes last in a query.",
            "Always pair LIMIT with ORDER BY if row order matters.",
            "LIMIT 1 gives you a single row — useful for 'the highest X'.",
        ],
        "try_challenge_id": "beg_009",
    },
    {
        "id": "beg_l07",
        "difficulty": "beginner",
        "order": 7,
        "title": "DISTINCT — Removing Duplicates",
        "icon": "🎯",
        "tagline": "See unique values only",
        "concept": "Filtering duplicate values with DISTINCT",
        "explanation": (
            "DISTINCT removes duplicate rows from your results. "
            "It's useful when you want to know what unique values exist in a column — "
            "like all the different product categories, order statuses, or states customers live in."
        ),
        "syntax_template": "SELECT DISTINCT column\nFROM table_name;",
        "annotated_example": {
            "query": "SELECT DISTINCT category\nFROM products;",
            "lines": [
                {"line": "SELECT DISTINCT category", "note": "Return each category only once"},
                {"line": "FROM products;", "note": "From the products table"},
            ],
        },
        "key_points": [
            "DISTINCT applies to all selected columns together.",
            "It's placed right after SELECT.",
            "Useful for data exploration: what values exist in this column?",
        ],
        "try_challenge_id": "beg_006",
    },
    {
        "id": "beg_l08",
        "difficulty": "beginner",
        "order": 8,
        "title": "SQL Clause Order",
        "icon": "📋",
        "tagline": "The rules about what comes in what order",
        "concept": "Correct SQL clause ordering",
        "explanation": (
            "SQL has a fixed order for clauses. Write them out of order and you'll get a syntax error. "
            "Memorize this sequence:\n\n"
            "1. SELECT — what columns\n"
            "2. FROM — which table\n"
            "3. JOIN — connect other tables (learned next level)\n"
            "4. WHERE — filter rows\n"
            "5. GROUP BY — group rows (intermediate)\n"
            "6. HAVING — filter groups (intermediate)\n"
            "7. ORDER BY — sort results\n"
            "8. LIMIT — cap the count\n\n"
            "A helpful memory trick: Silly Frogs Jump When Groups Have Order Limits."
        ),
        "syntax_template": "SELECT columns\nFROM table\nWHERE condition\nORDER BY column\nLIMIT n;",
        "annotated_example": {
            "query": "SELECT first_name, salary\nFROM employees\nWHERE is_active = 1\nORDER BY salary DESC\nLIMIT 10;",
            "lines": [
                {"line": "SELECT first_name, salary", "note": "1. What to show"},
                {"line": "FROM employees", "note": "2. Where to look"},
                {"line": "WHERE is_active = 1", "note": "4. Filter rows"},
                {"line": "ORDER BY salary DESC", "note": "7. Sort"},
                {"line": "LIMIT 10;", "note": "8. Cap to 10 rows"},
            ],
        },
        "key_points": [
            "SELECT-FROM-WHERE-ORDER BY-LIMIT is the beginner core.",
            "Putting ORDER BY before WHERE is a syntax error.",
            "GROUP BY and HAVING are the next concepts to learn.",
        ],
        "try_challenge_id": "beg_034",
    },
]
