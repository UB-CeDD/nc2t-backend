from django.core.mail import send_mail

def send_welcome_email(username, user_email, password):
    login_link = "your_domain_name/login"
    send_mail(
        'Welcome to NCCT',
        f'Your account has been created.\n\nUsername: {username}\nPassword: {password}\nLogin Link: {login_link}',
        'no-reply@ncct.com',
        [user_email],
        fail_silently=False,
    )
