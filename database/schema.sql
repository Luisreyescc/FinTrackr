CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT,
);

CREATE TABLE incomes (
    income_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount DOUBLE,
    description TEXT,
    date TEXT,
    source TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
);

CREATE TABLE expenses (
    expense_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount DOUBLE,
    description TEXT,
    date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE expense_categories (
    expense_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (expense_id, category_id),
    FOREIGN KEY (expense_id) REFERENCES expenses(expense_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
);

CREATE TABLE debts (
    debt_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    debtor_name TEXT,
    amount DOUBLE,
    description TEXT,
    date TEXT,
    categories TEXT,
    is_payed BOOLEAN
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE debt_categories (
    debt_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (debt_id, category_id),
    FOREIGN KEY (debt_id) REFERENCES debts(debt_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
