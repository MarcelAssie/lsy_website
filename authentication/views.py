from django.shortcuts import redirect
from django.contrib.auth import login,  logout, authenticate
from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm
from . import forms
from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from authentication.models import Student

def welcome(request):
    return render(request, 'authentication/dashboard.html')

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

@staff_member_required
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

@staff_member_required
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

@staff_member_required
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

@staff_member_required
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
@staff_member_required
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


