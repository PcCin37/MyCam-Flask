import json
import unittest
from app import app
from models import *


class LoginTest(unittest.TestCase):
    """ test for login form """

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_empty_email_password(self):
        """ test for empty email and password """

        response = app.test_client().post('/user/login', data={})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Empty email address and password')
        self.assertEqual(json_dict['errcode'], -2, 'statu-code error')

    def test_short_password(self):
        """ test for short password """

        response = app.test_client().post('/user/login', data={'email': '12345@qq.com', 'password': '111111'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Password shorter than 8 characters')
        self.assertEqual(json_dict['errcode'], -3, 'statu-code error')

    def test_long_password(self):
        """ test for long password """

        response = app.test_client().post('/user/login', data={'email': '12345@qq.com',
                                                               'password': '111111111111111111111'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Password longer than 20 characters')
        self.assertEqual(json_dict['errcode'], -4, 'statu-code error')

    def test_error_email_password(self):
        """ test for wrong email or password """

        response = app.test_client().post('/user/login', data={'email': '12345@qq.com', 'password': '12346678'})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('errcode', json_dict, 'Wrong email or password')
        self.assertEqual(json_dict['errcode'], -1, 'statu-code error')


class RegisterTest(unittest.TestCase):
    """ test for register form """

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_empty_email_password(self):
        """ test for empty block """

        response = app.test_client().post('/user/register', data={})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'All the block can not be empty')
        self.assertEqual(json_dict['errcode'], -2, 'statu-code error')

    def test_short_username(self):
        """ test for short username """

        response = app.test_client().post('/user/register', data={'username': 'www', 'email': '12345@qq.com',
                                                                  'password': '12345678', 'verification_code': 'wwww'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Username must be longer than 4 characters')
        self.assertEqual(json_dict['errcode'], -3, 'statu-code error')

    def test_long_username(self):
        """ test for long username """

        response = app.test_client().post('/user/register', data={'username': 'wwwwwwwwwwwwwwwwwwwww',
                                                                  'email': '12345@qq.com',
                                                                  'password': '12345678', 'verification_code': 'wwww'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Username must be shorter than 20 characters')
        self.assertEqual(json_dict['errcode'], -4, 'statu-code error')

    def test_short_password(self):
        """ test for short password """

        response = app.test_client().post('/user/register', data={'username': 'wwww', 'email': '12345@qq.com',
                                                                  'password': '1234', 'verification_code': 'wwww'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Password must be longer than 8 characters')
        self.assertEqual(json_dict['errcode'], -5, 'statu-code error')

    def test_long_password(self):
        """ test for long password """

        response = app.test_client().post('/user/register', data={'username': 'wwww',
                                                                  'email': '12345@qq.com',
                                                                  'password': '123456789123456789123',
                                                                  'verification_code': 'wwww'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Password must be shorter than 20 characters')
        self.assertEqual(json_dict['errcode'], -6, 'statu-code error')

    def test_verification_code_length(self):
        """ test for verification code length """

        response = app.test_client().post('/user/register', data={'username': 'wwww',
                                                                  'email': '12345@qq.com',
                                                                  'password': '12345678',
                                                                  'verification_code': 'www'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Verification code must be 4 characters')
        self.assertEqual(json_dict['errcode'], -7, 'statu-code error')

    def test_error_format(self):
        """ test for wrong confirm password or wrong format """

        response = app.test_client().post('/user/login', data={'username': 'wwww', 'email': '12345@qq.com',
                                                               'password': '12345678', 'confirm_password': '1234',
                                                               'verification_code': 'wwww'})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('errcode', json_dict, 'Confirm password not correct or format of input incorrect')
        self.assertEqual(json_dict['errcode'], -1, 'statu-code error')


class EditInfoTest(unittest.TestCase):
    """ test for edit information form """

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_empty_input(self):
        """ test for empty block """

        response = app.test_client().post('/user/edit_user', data={})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'All the block can not be empty')
        self.assertEqual(json_dict['errcode'], -2, 'statu-code error')

    def test_edit_short_username(self):
        """ test for short username """

        response = app.test_client().post('/user/edit_user', data={'username': 'www', 'email': '12345@qq.com'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Username must be longer than 4 characters')
        self.assertEqual(json_dict['errcode'], -3, 'statu-code error')

    def test_edit_long_username(self):
        """ test for long username """

        response = app.test_client().post('/user/edit_user', data={'username': 'wwwwwwwwwwwwwwwwwwwww',
                                                                   'email': '12345@qq.com'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Username must be shorter than 20 characters')
        self.assertEqual(json_dict['errcode'], -4, 'statu-code error')


class ChangePasswordTest(unittest.TestCase):
    """ test for change password form """

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_empty_input(self):
        """ test for empty block """

        response = app.test_client().post('/user/edit_password', data={})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'All the block can not be empty')
        self.assertEqual(json_dict['errcode'], -2, 'statu-code error')

    def test_short_password(self):
        """ test for short password """

        response = app.test_client().post('/user/edit_password', data={'password': '1111'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Password must be longer than 8 characters')
        self.assertEqual(json_dict['errcode'], -3, 'statu-code error')

    def test_long_password(self):
        """ test for long password """

        response = app.test_client().post('/user/edit_password', data={'password': 'wwwwwwwwwwwwwwwwwwwww'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Password must be shorter than 20 characters')
        self.assertEqual(json_dict['errcode'], -4, 'statu-code error')


class PostTest(unittest.TestCase):
    """ test for post form """

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_empty_input(self):
        """ test for empty block """

        response = app.test_client().post('/post/public', data={})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'All the block can not be empty')
        self.assertEqual(json_dict['errcode'], -2, 'statu-code error')

    def test_short_title(self):
        """ test for short title """

        response = app.test_client().post('/post/public', data={'title': '1', 'category': "Animals",
                                                                'place': 'Chongqing', 'time': '2020',
                                                                'popular': 'pop', 'description': 'wangmou'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Title must be longer than 2 characters')
        self.assertEqual(json_dict['errcode'], -3, 'statu-code error')

    def test_long_title(self):
        """ test for long password """

        response = app.test_client().post('/post/public', data={'title': '11111111111111111111111111111111111111111111',
                                                                'category': "Animals",
                                                                'place': 'Chongqing', 'time': '2020',
                                                                'popular': 'pop', 'description': 'wangwangwang'})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'Password must be shorter than 20 characters')
        self.assertEqual(json_dict['errcode'], -4, 'statu-code error')


class CommentTest(unittest.TestCase):
    """ test for comment form """

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_empty_input(self):
        """ test for empty block """

        response = app.test_client().post('/comment/public', data={})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, 'All the block can not be empty')
        self.assertEqual(json_dict['errcode'], -2, 'statu-code error')


class DatabaseTest(unittest.TestCase):
    """ test for database"""

    def setUp(self):
        self.app = app

    def test_user_append_data(self):
        """ test for UserModel database """

        with app.app_context():
            user = UserModel(username='test', email='123@qq.com', verification_code='wert',
                             password='testpassword')
            db.session.add(user)
            db.session.commit()
            author = UserModel.query.filter_by(username='test').first()
            # judge the data exist
            self.assertIsNotNone(author)
            db.session.delete(author)
            db.session.commit()

    def test_post_append_data(self):
        """ test for PostModel database """

        with app.app_context():
            post = PostModel(title='testpost', pic='1111111', category='Animals',
                             place='Hangzhou', time='2020', popular='pop', description='12345')
            db.session.add(post)
            db.session.commit()
            public = PostModel.query.filter_by(title='testpost').first()
            # judge the data exist
            self.assertIsNotNone(public)
            db.session.delete(public)
            db.session.commit()

    def test_comment_append_data(self):
        """ test for CommentModel database """

        with app.app_context():
            comment = CommentModel(content='testcomment')
            db.session.add(comment)
            db.session.commit()
            public = CommentModel.query.filter_by(content='testcomment').first()
            # judge the data exist
            self.assertIsNotNone(public)
            db.session.delete(public)
            db.session.commit()

    # test for CollectionModel database
    def test_collection_append_data(self):
        """ test for CollectionModel database """

        with app.app_context():
            collection = CollectionModel(id=5, post_id=5, author_id=5)
            db.session.add(collection)
            db.session.commit()
            add = CollectionModel.query.filter_by(id=5).first()
            # judge the data exist
            self.assertIsNotNone(add)
            db.session.delete(add)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()