# services/users/project/tests/test_users.py

import json
import unittest

from project.tests.base import BaseTestCase
# from project import db
# from project.api.models import User
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Pruebas para el servicio de usuarios."""

    def test_users(self):
        """Asegúrese de que la ruta /ping se comporte correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    # POST (ADD A USER)

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jhordy.huaman',
                    'email': 'jhordy.h@upeu.edu.pe',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('jhordy.h@upeu.edu.pe was added!',
                          data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Asegúrese de que se produzca un error si el
        objeto JSON está vacío."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Asegúrese de que se produzca un error si el objeto
        JSON no tiene una clave
        de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'jhordy.h@upeu.edu.pe',
                    'password': 'password',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """ Asegúrese de que se arroje un error si el
        correo electrónico ya existe."""

        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jhordy.huaman',
                    'email': 'jhordy.h@upeu.edu.pe',
                    'password': 'greaterthaneight'}),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jhordy.huaman',
                    'email': 'jhordy.h@upeu.edu.pe',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. Email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('jhordy.huaman',
                        'jhordy.h@upeu.edu.pe',
                        'greaterthaneight')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('jhordy.huaman', data['data']['username'])
            self.assertIn('jhordy.h@upeu.edu.pe',
                          data['data']['email'])
            self.assertIn('success', data['status'])

    # GET USER BY ID

    def test_single_user_no_id(self):
        """Asegúrese de que se produzca un error si no se proporciona un id."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Asegúrese de que se produzca un error si el id no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    # GET ALL USERS
    def test_all_users(self):
        """Asegúrese de que todos los usuarios se
        comporten correctamente."""

        add_user('jhordy.huaman',
                 'jhordy.h@upeu.edu.pe',
                 'greaterthaneight')
        add_user('jhordy.ho', 'jhordy.ho@gmail.com',
                 'greaterthaneight')
        add_user('jhordy.aho', 'jhordy.aho@gmail.com',
                 'greaterthaneight')
        add_user('jhordyrx', 'jhordyrx@gmail.com',
                 'greaterthaneight')
        add_user('jhordya', 'm.jhordya@gmail.com',
                 'greaterthaneight')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 5)
            self.assertIn('jhordy.huaman',
                          data['data']['users'][0]['username'])
            self.assertIn('jhordy.h@upeu.edu.pe',
                          data['data']['users'][0]['email'])
            self.assertIn('jhordy.ho',
                          data['data']['users'][1]['username'])
            self.assertIn('jhordy.ho@gmail.com',
                          data['data']['users'][1]['email'])
            self.assertIn('jhordy.aho',
                          data['data']['users'][2]['username'])
            self.assertIn('jhordy.aho@gmail.com',
                          data['data']['users'][2]['email'])
            self.assertIn('jhordyrx',
                          data['data']['users'][3]['username'])
            self.assertIn('jhordyrx@gmail.com',
                          data['data']['users'][3]['email'])
            self.assertIn('jhordya',
                          data['data']['users'][4]['username'])
            self.assertIn('m.jhordya@gmail.com',
                          data['data']['users'][4]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Asegurando que la ruta principal se comporte correctamente
        cuando no se
        hayan agregado usuarios a la base de datos."""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Asegurando que la ruta principal se comporte
        correctamente cuando se
        hayan agregado usuarios a la base de datos."""

        add_user('lucas.rafa', 'lucas.rafa@upeu.edu.pe', 'greaterthaneight')
        add_user('lucas', 'lucas@gmail.com', 'greaterthaneight')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'lucas.rafa', response.data)
            self.assertIn(b'lucas', response.data)

    def test_main_add_user(self):
        """ Asegurando que se pueda agregar un nuevo usuario
        a la base de datos mediante
           una solicitud POST """
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    username='harold.new',
                    email='harold.new@test.com',
                    password='greaterthaneight'), follow_redirects=True
                )
            self.assertEqual(response.status_code, 200)

    def test_add_user_invalid_json_keys_no_password(self):
        """
        asegúrese de que se produzca un error si
        el objeto JSON no tiene una clave y password.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='freddy',
                    email='freddy@reallynotreal.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])


if __name__ == '__main__':
    unittest.main()
