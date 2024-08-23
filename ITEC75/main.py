from website import create_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)