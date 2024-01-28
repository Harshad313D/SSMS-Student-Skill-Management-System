import random
import smtplib

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError
import socket

from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import User


def custom_login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            if user.student_obj:
                return redirect('student_dashboard')  # Redirect to the student dashboard
            if user.teacher_obj:
                return redirect('teacher_dashboard')  # Redirect to the student dashboard
        else:
            # Authentication failed
            context['error'] = "WRONG USERNAME OR PASSWORD"
            return render(request, 'account/login.html', context)  # Render the login form template

    return render(request, 'account/login.html')  # Render the login form template


def forgot_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'account/forgot_password.html', {'error': 'User does not exist.'})

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        print("otp : ", otp)

        # Attempt to send OTP to user's email
        try:

            email_subject = 'OTP Request for password reset.'
            email_body = render_to_string('email/otp.html', {'otp': otp})
            text_content = strip_tags(email_body)

            email = EmailMultiAlternatives(email_subject, text_content, settings.EMAIL_HOST_USER, [user.email])

            email.attach_alternative(email_body, "text/html")
            email.send()

        except BadHeaderError:
            return render(request, 'account/forgot_password.html', {'error': 'Invalid email header.'})
        except smtplib.SMTPException as e:
            # Handle SMTP exceptions here
            print(f"Failed to send email: {str(e)}")
            return render(request, 'account/forgot_password.html',
                          {'error': 'Failed to send email. Please try again later.'})
        except socket.gaierror as e:
            # Handle gaierror exceptions here
            print(f"Failed to resolve domain name: {str(e)}")
            error_message = 'Failed to resolve domain name. Check your internet connection.'
            return render(request, 'account/forgot_password.html', {'error': error_message})

        # Store the OTP in the session
        request.session['otp'] = otp
        request.session['user_id'] = user.id

        return redirect('confirm_otp')  # Replace 'confirm_otp' with your desired URL
    else:
        return render(request, 'account/forgot_password.html')


def confirm_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        re_new_password = request.POST.get('re_new_password')

        # Retrieve OTP and user ID from the session
        stored_otp = request.session.get('otp')
        user_id = request.session.get('user_id')
        user_email = User.objects.get(id=user_id).email

        if new_password == re_new_password:
            if otp == stored_otp:
                # Reset the user's password
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return render(request, 'account/confirm_otp.html', {'error': 'User does not exist.'})

                user.set_password(new_password)
                user.save()

                # Check if the user exists

                email_subject = 'Password Changed'
                email_body = 'Your password has been changed successfully.'
                from_email = settings.EMAIL_HOST_USER  # Use the sender email from settings
                recipient_list = [user_email]

                email = EmailMessage(email_subject, email_body, from_email, recipient_list)
                email.send()

                # Clear the session
                del request.session['otp']
                del request.session['user_id']

                return redirect('change_success')  # Replace 'login' with your desired URL
            else:
                return render(request, 'account/confirm_otp.html', {'error': 'Invalid OTP.'})
        else:
            return render(request, 'account/confirm_otp.html', {'error': 'Passwords do not match.'})
    else:
        return render(request, 'account/confirm_otp.html')


def change_success(request):
    return render(request, 'account/change_success.html',)


def logout_view(request):
    logout(request)
    return redirect("login")


# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)