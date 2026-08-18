import importlib.util
from pathlib import Path

from werkzeug.security import generate_password_hash

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / 'app.py'


def load_app_module():
    spec = importlib.util.spec_from_file_location('diabetes_app', APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_app_exists_and_has_flask_app():
    module = load_app_module()
    assert APP_PATH.exists(), 'app.py should exist in the project root'
    assert hasattr(module, 'app'), 'Expected a Flask app instance named app'
    assert hasattr(module, 'init_db'), 'Expected a database initialization function'


def test_required_feature_routes_exist():
    module = load_app_module()
    routes = {rule.rule for rule in module.app.url_map.iter_rules()}
    required = {
        '/login',
        '/signup',
        '/dashboard',
        '/predict',
        '/analytics',
        '/reminders',
        '/history',
        '/about',
        '/profile',
        '/settings',
        '/reports',
    }
    missing = sorted(required - routes)
    assert not missing, f'Missing expected routes: {missing}'


def test_saved_user_theme_is_reflected_in_global_layout():
    module = load_app_module()
    with module.app.app_context():
        db = module.get_db()
        db.execute('DELETE FROM users WHERE email = ?', ('themecheck@example.com',))
        db.execute(
            'INSERT INTO users (full_name, email, password_hash, theme) VALUES (?, ?, ?, ?)',
            ('Theme Check', 'themecheck@example.com', generate_password_hash('Password123'), 'dark'),
        )
        db.commit()

        with module.app.test_client() as client:
            client.post('/login', data={'email': 'themecheck@example.com', 'password': 'Password123'}, follow_redirects=False)
            response = client.get('/dashboard')

    assert response.status_code == 200
    assert 'data-theme="dark"' in response.get_data(as_text=True)


def test_history_search_and_risk_filter_are_applied_per_user():
    module = load_app_module()
    with module.app.app_context():
        db = module.get_db()
        db.execute('DELETE FROM predictions WHERE user_id IN (SELECT id FROM users WHERE email IN (?, ?))', ('historysearch@example.com', 'historyother@example.com'))
        db.execute('DELETE FROM users WHERE email IN (?, ?)', ('historysearch@example.com', 'historyother@example.com'))
        db.execute(
            'INSERT INTO users (full_name, email, password_hash, theme) VALUES (?, ?, ?, ?)',
            ('History Searcher', 'historysearch@example.com', generate_password_hash('Password123'), 'light'),
        )
        db.execute(
            'INSERT INTO users (full_name, email, password_hash, theme) VALUES (?, ?, ?, ?)',
            ('Other User', 'historyother@example.com', generate_password_hash('Password123'), 'light'),
        )
        db.commit()

        user_id = db.execute('SELECT id FROM users WHERE email = ?', ('historysearch@example.com',)).fetchone()['id']
        other_user_id = db.execute('SELECT id FROM users WHERE email = ?', ('historyother@example.com',)).fetchone()['id']

        db.execute(
            'INSERT INTO predictions (user_id, created_at, glucose, blood_pressure, bmi, age, insulin, risk_score, risk_category, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (user_id, '2026-08-15 10:30:00', 120.0, 80.0, 25.0, 45, 100.0, 75.0, 'HIGH', 'match me'),
        )
        db.execute(
            'INSERT INTO predictions (user_id, created_at, glucose, blood_pressure, bmi, age, insulin, risk_score, risk_category, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (user_id, '2026-08-16 11:30:00', 110.0, 70.0, 22.0, 40, 90.0, 35.0, 'LOW', 'another match'),
        )
        db.execute(
            'INSERT INTO predictions (user_id, created_at, glucose, blood_pressure, bmi, age, insulin, risk_score, risk_category, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (other_user_id, '2026-08-15 12:00:00', 120.0, 80.0, 25.0, 45, 100.0, 75.0, 'HIGH', 'other user data'),
        )
        db.commit()

        with module.app.test_client() as client:
            client.post('/login', data={'email': 'historysearch@example.com', 'password': 'Password123'}, follow_redirects=False)
            response = client.get('/history?search=120&risk=HIGH')

    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert 'match me' in text or 'HIGH' in text
    assert 'other user data' not in text
