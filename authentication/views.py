from django.shortcuts import redirect, render, reverse
from django.contrib.auth import login,  logout, authenticate
from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm
from . import forms
from .models import User
from django.urls import reverse_lazy
from django.views.generic import View
from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import user_passes_test, login_required
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.conf import settings
from .forms import PasswordResetRequestForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views import View
from .forms import CustomPasswordResetRequestForm
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView



def welcome(request):
    return render(request, 'authentication/dashboard.html')
@login_required
@user_passes_test(lambda user: user.is_superuser)
def generate_pdf_student(request, username, full_name, classe, password):
    template_path = 'authentication/student_registration_pdf.html'
    context = {
        'username': username,
        'full_name': full_name,
        'classe': classe,
        'password': password,
    }
    # Load template
    template = get_template(template_path)
    html = template.render(context)
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="login_{username}.pdf"'
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response

@login_required
@user_passes_test(lambda user: user.is_superuser)
def student_register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user, password = form.save()  # Récupérer l'utilisateur et le mot de passe généré
            full_name = f"{user.first_name} {user.last_name}"
            classe = form.cleaned_data['classe']
            return render(request, 'authentication/student_register_success.html', {
                'username': user.username,
                'full_name': full_name,
                'classe': classe,
                'password': password,
            })
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = StudentSignUpForm()
    return render(request, 'authentication/student_register.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def generate_pdf_teacher(request, username, full_name, matiere, classes, password):
    template_path = 'authentication/teacher_registration_pdf.html'
    context = {
        'username': username,
        'full_name': full_name,
        'matiere': matiere,
        'classes': classes,
        'password': password,
    }
    # Load template
    template = get_template(template_path)
    html = template.render(context)
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="login_{username}.pdf"'
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response

@login_required
@user_passes_test(lambda user: user.is_superuser)
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user, password = form.save()  # Récupérer l'utilisateur et le mot de passe généré
            full_name = f"{user.first_name} {user.last_name}"
            matiere = form.cleaned_data['matiere']  # Exemple : Obtenez le nom de la matière
            classes = ', '.join([str(c) for c in form.cleaned_data[
                'classes']])  # Exemple : Convertissez les classes en une chaîne de noms

            # Convertir les paramètres en chaînes pour l'URL

            return render(request, 'authentication/teacher_register_success.html', {
                'username': user.username,
                'full_name': full_name,
                'matiere': matiere,
                'classes': classes,
                'password': password,
            })
        else:
            print("Form errors:", form.errors)
    else:
        form = TeacherSignUpForm()
    return render(request, 'authentication/teacher_register.html', {'form': form})

class LoginPage(View):
    template_name = 'authentication/login_user.html'
    login_form = forms.LoginForm
    def get(self, request):
        form = self.login_form()
        message = ''
        return render(request, self.template_name, {'form': form, 'message': message})
    def post(self, request):
        form = self.login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return self.redirect_user(user)
            else:
                message = 'Identifiants invalides.'
        else:
            message = 'Veuillez corriger les erreurs ci-dessous.'

        return render(request, self.template_name, {'form': form, 'message': message})
    def redirect_user(self, user):
        if user.is_superuser:
            return redirect('admin-profile')
        elif user.is_teacher:
            return redirect('teacher-profile')
        elif user.is_student:
            return redirect('student-profile')
        elif user.is_parent:
            return redirect('parent-dashboard')
        else:
            return redirect('welcome')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def generate_pdf_parent(request, username, full_name, password):
    template_path = 'authentication/parent_registration_pdf.html'
    context = {
        'username': username,
        'full_name': full_name,
        'password': password,
    }
    # Load template
    template = get_template(template_path)
    html = template.render(context)
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="login_{username}.pdf"'
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response
@login_required
@user_passes_test(lambda user: user.is_superuser)
def parent_register(request):
    if request.method == 'POST':
        form = ParentSignUpForm(request.POST)
        if form.is_valid():
            user, password = form.save()  # Récupérer l'utilisateur et le mot de passe généré
            full_name = f"{user.first_name} {user.last_name}"
            return render(request, 'authentication/parent_register_success.html', {
                'username': user.username,
                'full_name': full_name,
                'password': password,
            })
        else:
            print("Form errors:", form.errors)
    else:
        form = ParentSignUpForm()
    return render(request, 'authentication/parent_register.html', {'form': form})

def logout_user(request):
    """
    Lancement de la page de deconnexion pour l'utilisateur
    """
    logout(request)
    return redirect('welcome')

def custom_404_view(request, exception=None):
    return render(request, 'authentication/404.html', status=404)
def custom_500_view(request):
    return render(request, 'authentication/500.html', status=500)


# views.py



def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            role = form.cleaned_data['role']
            class_for_student = form.cleaned_data.get('class_for_student', '')
            subject_for_teacher = form.cleaned_data.get('subject_for_teacher', '')
            has_email = form.cleaned_data['has_email']

            # Préparation du contenu de l'e-mail
            to_emails = settings.CONTACT_EMAIL
            subject = f"Demande de réinitialisation de mot de passe de {first_name} {last_name}"
            body = f"""
            <html>
            <head>
                <style>
                    .email-container {{
                        font-family: 'Arial', sans-serif;
                        color: #333;
                        padding: 20px;
                        border: 1px solid #e0e0e0;
                        border-radius: 10px;
                        background: #f9f9f9;
                        max-width: 600px;
                        margin: auto;
                    }}
                    .email-container h2 {{
                        text-align: center;
                        color: #007bff;
                    }}
                    .email-container p {{
                        font-size: 16px;
                        line-height: 1.5;
                    }}
                    .email-container .label {{
                        font-weight: bold;
                        color: #555;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <h2>Demande de réinitialisation de mot de passe</h2>
                    <p><span class="label">Prénom :</span> {first_name}</p>
                    <p><span class="label">Nom :</span> {last_name}</p>
                    <p><span class="label">Rôle :</span> {role.capitalize()}</p>
                    {f"<p><span class='label'>Classe :</span> {class_for_student}</p>" if role == 'student' else ""}
                    {f"<p><span class='label'>Matière :</span> {subject_for_teacher}</p>" if role == 'teacher' else ""}
                </div>
            </body>
            </html>
            """

            # Création du message
            message = MIMEMultipart("alternative")
            message['From'] = settings.EMAIL_HOST_USER
            message['To'] = ', '.join(to_emails)
            message['Subject'] = subject

            message.attach(MIMEText(body, 'html'))

            try:
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                    server.starttls()
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.sendmail(settings.EMAIL_HOST_USER, to_emails, message.as_string())
                print('Email envoyé avec succès!')
            except Exception as e:
                print(f'Une erreur est survenue : {e}')
            if has_email == 'yes':
                return redirect(reverse('password_reset'))  # Redirige vers la page de réinitialisation
            else:
                return redirect(reverse('confirmation-password-request') + f'?first_name={first_name}&last_name={last_name}')  # Change 'confirmation' selon ton URL de confirmation

    else:
        form = PasswordResetRequestForm()

    return render(request, 'authentication/password_reset_request.html', {'form': form})


def confirmation_password(request: HttpRequest):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    context = {'first_name': first_name, 'last_name': last_name}
    return render(request, 'authentication/confirmation_password_request.html', context)


def custom_password_reset_request_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                message = "Cet identifiant n'existe pas."
                return render(request, 'authentication/password_reset_form.html', {'form': form, 'message':message})

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            # Préparation du contenu de l'e-mail
            subject = "Réinitialisation de votre mot de passe"
            body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f0f0;
                    }}
                    .email-container {{
                        font-family: 'Arial', sans-serif;
                        color: #333;
                        padding: 20px;
                        border: 1px solid #e0e0e0;
                        border-radius: 10px;
                        background: #ffffff;
                        max-width: 600px;
                        margin: 20px auto;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    .email-header {{
                        text-align: center;
                        background: #007bff;
                        color: #ffffff;
                        padding: 20px;
                        border-radius: 10px 10px 0 0;
                    }}
                    .email-header h2 {{
                        margin: 0;
                        font-size: 24px;
                        font-weight: 700;
                    }}
                    .email-content {{
                        padding: 20px;
                    }}
                    .email-content p {{
                        font-size: 16px;
                        line-height: 1.5;
                        margin: 0 0 10px;
                    }}
                    .email-content .label {{
                        font-weight: bold;
                        color: #555;
                    }}
                    .email-content a {{
                        color: #007bff;
                        text-decoration: none;
                        font-weight: bold;
                        border: 2px solid #007bff;
                        padding: 10px 15px;
                        border-radius: 5px;
                        display: inline-block;
                        transition: background-color 0.3s, color 0.3s;
                    }}
                    .email-content a:hover {{
                        background-color: #007bff;
                        color: #ffffff;
                    }}
                    .email-footer {{
                        text-align: center;
                        padding: 20px;
                        font-size: 14px;
                        color: #777;
                    }}
                    .email-footer p {{
                        margin: 0;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h2>Réinitialisation de votre mot de passe</h2>
                    </div>
                    <div class="email-content">
                        <p>Bonjour {user.username},</p>
                        <p>Vous avez demandé à réinitialiser votre mot de passe. Pour définir un nouveau mot de passe, veuillez cliquer sur le bouton ci-dessous :</p>
                        <p><a href="{reset_url}">Réinitialiser mon mot de passe</a></p>
                        <p>Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet e-mail.</p>
                    </div>
                    <div class="email-footer">
                        <p>Merci,<br>L'équipe informatique du Lycée Scientifique de Yamoussoukro</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Création du message
            message = MIMEMultipart("alternative")
            message['From'] = settings.EMAIL_HOST_USER
            message['To'] = email
            message['Subject'] = subject

            message.attach(MIMEText(body, 'html'))

            try:
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                    server.starttls()
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.sendmail(settings.EMAIL_HOST_USER, email, message.as_string())
                print('Email envoyé avec succès!')
            except Exception as e:
                print(f'Une erreur est survenue : {e}')

            return redirect(reverse('password_reset_done'))

    else:
        form = CustomPasswordResetRequestForm()


    return render(request, 'authentication/password_reset_form.html', {'form': form})

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')



class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/password_reset_complete.html'
