from django.test import TestCase
from django.urls import reverse
from GroundsNavigator.views import profile_view, home
from allauth.socialaccount.models import SocialApp


class TestCorrectHomepageStatus(TestCase):
    # checks if homepage URL returns a 200 status code (successful response code)
    def test_homepage_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    # checks if the correct template (home.html) is used to render the homepage
    def test_homepage_template_used(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'home.html')

class TestCorrectLoginPageStatus(TestCase):
    def test_login_status_code(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_template_used(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'account/login.html')

# class TestCorrectGoogleLoginPageStatus(TestCase):
#     def test_login_status_code(self):
#         url = reverse('redirect_login')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

class SignInPageTest(TestCase):
    # checks if sign in button correctly redirects to login.html and returns a 200 status code
    def test_sign_in_button_redirect(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    # # checks if admin button correctly redirects to admin.site.urls and returns a 200 status code 
    # def test_admin_button_redirect(self): # error
    #     url = reverse('admin')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200) 
    #     self.assertTemplateUsed(response, 'siteadmin.html')

# class SignOutPageTest(TestCase): # fails
#     # checks if sign out button correctly redirects to sign out confirmation page and returns a 200 status code 
#     def test_sign_out_button_redirect(self):
#         url = reverse('profile')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'sign_out.html')

class LoginPageContent(TestCase):
    def test_username_password_fields_exist(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input class="input-field" type="text" name="login" placeholder="Username" required>')
        self.assertContains(response, '<input class="input-field" type="password" name="password" placeholder="Password" required>')

    def test_signin_button_exist(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<button class="button" type="submit">Sign In</button>')
 
    def test_remember_me_checkbox_exists(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="checkbox" name="remember"')

class MapFormDisplayTest(TestCase):
    def test_map_click_displays_form(self):
        url = reverse('home')
        response = self.client.post(url, {'map_clicked': 'true'})  
        self.assertContains(response, '<form id="locationForm"')

# class HomePageTest(TestCase): # in the works
#     def test_submit_location(self):
#         data = {
#         'latlong': '0,0',
#         'select_option': 'restroom',  
#         'title': 'Test title',      
#         'description': 'Test description',  
#     }
#         response = self.client.post(reverse('save_location'), data, content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertEqual(response_data['message'], 'Location saved successfully')




