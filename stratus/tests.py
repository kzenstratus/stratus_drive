from django.test import TestCase
from django.core.urlresolvers import resolve
from stratus.views import login
from django.http import HttpRequest

class SmokeTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func,home)

	# def test_home_page_returns_correct_html(self):
	# 	request = HttpRequest()
	# 	response = home(request)

	# 	self.assertTrue(response.content.strip().startswith(b'<html>'))
	# 	self.assertIn(b'<title> Stratus </title>', response.content)
	# 	self.assertTrue(response.content.strip().endswith(b'</html>'))