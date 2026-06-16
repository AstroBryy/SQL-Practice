TABLES = [
    """
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        budget REAL NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        dept_id INTEGER REFERENCES departments(id),
        salary REAL NOT NULL,
        hire_date TEXT NOT NULL,
        manager_id INTEGER REFERENCES employees(id),
        is_active INTEGER NOT NULL DEFAULT 1
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        registration_date TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id),
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        total_amount REAL NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id),
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sales_reps (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER REFERENCES employees(id),
        region TEXT NOT NULL,
        commission_rate REAL NOT NULL,
        ytd_sales REAL NOT NULL
    )
    """,
]

TABLE_NAMES = ["departments", "employees", "products", "customers", "orders", "order_items", "sales_reps"]
