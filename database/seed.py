import random
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

DEPARTMENTS = [
    ("Engineering", "San Francisco", 2500000),
    ("Marketing", "New York", 1200000),
    ("Sales", "Chicago", 1800000),
    ("Finance", "Boston", 950000),
    ("Human Resources", "Austin", 750000),
    ("Product", "San Francisco", 1100000),
    ("Operations", "Denver", 880000),
    ("Customer Success", "Seattle", 720000),
    ("Legal", "New York", 680000),
    ("Data Analytics", "Remote", 930000),
]

PRODUCT_CATEGORIES = ["Electronics", "Office Supplies", "Software", "Furniture", "Services"]
ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]
REGIONS = ["Northeast", "Southeast", "Midwest", "Southwest", "West", "Northwest"]


def seed_database(conn):
    cur = conn.cursor()

    # Departments
    for i, (name, loc, budget) in enumerate(DEPARTMENTS, 1):
        cur.execute(
            "INSERT INTO departments (id, name, location, budget) VALUES (?, ?, ?, ?)",
            (i, name, loc, round(budget + random.uniform(-50000, 50000), 2)),
        )

    # Employees — first pass (no manager_id yet)
    emp_ids = list(range(1, 101))
    dept_ids = list(range(1, 11))
    salaries = []
    for eid in emp_ids:
        dept_id = random.choice(dept_ids)
        salary = round(random.uniform(40000, 150000), 2)
        salaries.append(salary)
        hire_date = fake.date_between(start_date="-10y", end_date="today").isoformat()
        is_active = 1 if random.random() > 0.1 else 0
        cur.execute(
            "INSERT INTO employees (id, first_name, last_name, dept_id, salary, hire_date, manager_id, is_active) "
            "VALUES (?, ?, ?, ?, ?, ?, NULL, ?)",
            (eid, fake.first_name(), fake.last_name(), dept_id, salary, hire_date, is_active),
        )

    # Assign manager_ids (each employee gets a manager from the same dept with higher id, or NULL)
    cur.execute("SELECT id, dept_id FROM employees ORDER BY id")
    emps = cur.fetchall()
    dept_to_emps = {}
    for eid, did in emps:
        dept_to_emps.setdefault(did, []).append(eid)

    for eid, did in emps:
        candidates = [x for x in dept_to_emps[did] if x < eid]
        if candidates:
            mgr = random.choice(candidates[-3:])
            cur.execute("UPDATE employees SET manager_id = ? WHERE id = ?", (mgr, eid))

    # Products
    product_names_used = set()
    for pid in range(1, 51):
        category = random.choice(PRODUCT_CATEGORIES)
        while True:
            name = fake.bs().title()[:40]
            if name not in product_names_used:
                product_names_used.add(name)
                break
        price = round(random.uniform(9.99, 999.99), 2)
        stock = random.randint(0, 500)
        cur.execute(
            "INSERT INTO products (id, name, category, price, stock_quantity) VALUES (?, ?, ?, ?, ?)",
            (pid, name, category, price, stock),
        )

    # Customers
    emails_used = set()
    for cid in range(1, 201):
        while True:
            email = fake.email()
            if email not in emails_used:
                emails_used.add(email)
                break
        reg_date = fake.date_between(start_date="-5y", end_date="today").isoformat()
        cur.execute(
            "INSERT INTO customers (id, first_name, last_name, email, city, state, registration_date) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (cid, fake.first_name(), fake.last_name(), email, fake.city(), fake.state_abbr(), reg_date),
        )

    # Orders
    for oid in range(1, 501):
        cid = random.randint(1, 200)
        order_date = fake.date_between(start_date="-3y", end_date="today").isoformat()
        status = random.choice(ORDER_STATUSES)
        total = round(random.uniform(15.00, 3000.00), 2)
        cur.execute(
            "INSERT INTO orders (id, customer_id, order_date, status, total_amount) VALUES (?, ?, ?, ?, ?)",
            (oid, cid, order_date, status, total),
        )

    # Order items
    item_id = 1
    for oid in range(1, 501):
        n_items = random.randint(1, 5)
        products_in_order = random.sample(range(1, 51), min(n_items, 50))
        for pid in products_in_order:
            qty = random.randint(1, 10)
            unit_price = round(random.uniform(9.99, 499.99), 2)
            cur.execute(
                "INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?, ?)",
                (item_id, oid, pid, qty, unit_price),
            )
            item_id += 1

    # Sales reps — pick 20 employees
    rep_emp_ids = random.sample(emp_ids, 20)
    for rid, eid in enumerate(rep_emp_ids, 1):
        region = random.choice(REGIONS)
        commission = round(random.uniform(0.03, 0.12), 4)
        ytd = round(random.uniform(10000, 500000), 2)
        cur.execute(
            "INSERT INTO sales_reps (id, employee_id, region, commission_rate, ytd_sales) VALUES (?, ?, ?, ?, ?)",
            (rid, eid, region, commission, ytd),
        )

    conn.commit()
