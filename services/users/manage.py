# services/users/manage.py


import sys
import unittest
import coverage

from flask.cli import FlaskGroup

from project import create_app, db  # nuevo
from project.api.models import User  # nuevo

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()  # nuevo
cli = FlaskGroup(create_app=create_app)  # nuevo


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Ejecutar los tests sin code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)

@cli.command("seed_db")
def seed_db():
    """Sembrar la base de datos"""
    db.session.add(User(               # nuevo
        username='jhordy.huaman',
        email='jhordy.huaman@upeu.edu.pe',
        password='greaterthaneight')
    )
    db.session.add(User(               # nuevo
        username='arnold',
        email='jhordyho@gmail.com',
        password='greaterthaneight')
    )
    db.session.commit()

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con cobertura."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)

if __name__ == "__main__":
    cli()
