import os

from flask_migrate import Migrate, upgrade

from app import create_app, db

app = create_app()
migrate = Migrate(app, db)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()


if __name__ == "__main__":
    app.run()
