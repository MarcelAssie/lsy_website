from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Message
from authentication.models import Student, User, Teacher
from administration.models import Class, Subject
from .forms import MessageForm
from django.contrib.auth.decorators import login_required

#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------- MESSAGES ELEVES ----------------------------------------------------------------
@login_required
def student_to_admin(request):
    sent_messages = Message.objects.filter(sender=request.user, recipients__is_superuser=True).order_by('-timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            admin_user = User.objects.filter(is_superuser=True).first()  # Récupère le premier utilisateur administrateur
            message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
            message.recipients.add(admin_user)
            message.save()
            return redirect('student-profile')
    else:
        form = MessageForm()
    return render(request, 'messagerie/student_to_admin.html', {'form': form, 'sent_messages': sent_messages})

@staff_member_required
def message_classes(request):
    classes = Class.objects.all()
    return render(request, 'messagerie/message_classes.html', {'classes': classes})

@staff_member_required
def admin_to_unique_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
            message.recipients.add(student.user)  # Ajouter l'utilisateur de l'étudiant comme destinataire
            message.save()
            return redirect('student-details', student_id=student.id)
    else:
        form = MessageForm()
    return render(request, 'messagerie/admin_to_unique_student.html', {'form': form, 'student': student})

@staff_member_required
def admin_to_students_by_class(request, class_id):
    classe = Class.objects.get(id=class_id)
    students = classe.student_set.all()  # Récupère tous les étudiants de la classe
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
            message.recipients.add(*[student.user for student in students])  # Ajoute tous les étudiants comme destinataires
            message.save()
            return redirect('manage-students')  # Redirection après envoi du message
    else:
        form = MessageForm()
    return render(request, 'messagerie/admin_to_class_students.html', {'form': form, 'class_instance': classe})

@staff_member_required
def admin_to_all_students(request):
    all_students = Student.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            for student in all_students:
                message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
                message.recipients.add(student.user)
                message.save()
            return redirect('manage-students')  # Rediriger vers la page d'accueil de l'administrateur ou une autre vue
    else:
        form = MessageForm()

    return render(request, 'messagerie/admin_to_all_students.html', {'form': form})

#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------- MESSAGES ENSEIGNANTS ----------------------------------------------------------------


@staff_member_required
def message_subjects_classes(request):
    subjects = Subject.objects.all()
    classes = Class.objects.all()
    return render(request, 'messagerie/message_subjects_classes.html', {'subjects': subjects, 'classes': classes})

@login_required
def teacher_to_admin(request):
    sent_messages = Message.objects.filter(sender=request.user, recipients__is_superuser=True).order_by('-timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            admin_user = User.objects.filter(is_superuser=True).first()
            message = Message.objects.create(sender=sender, subject=subject, body=body,file=file)
            message.recipients.add(admin_user)
            message.save()
            return redirect('teacher-profile')
    else:
        form = MessageForm()
    return render(request, 'messagerie/teacher_to_admin.html', {'form': form, 'sent_messages': sent_messages})

@staff_member_required
def admin_to_unique_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
            message.recipients.add(teacher.user)
            message.save()
            return redirect('teacher-details', teacher_id=teacher.id)
    else:
        form = MessageForm()
    return render(request, 'messagerie/admin_to_unique_teacher.html', {'form': form, 'teacher': teacher})


@staff_member_required
def admin_to_all_teachers(request):
    all_teachers = Teacher.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            for teacher in all_teachers:
                message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
                message.recipients.add(teacher.user)
                message.save()
            return redirect('manage-teachers')
    else:
        form = MessageForm()

    return render(request, 'messagerie/admin_to_all_teachers.html', {'form': form})

@staff_member_required
def admin_to_teachers_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    teachers = Teacher.objects.filter(matiere=subject)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            for teacher in teachers:
                message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
                message.recipients.add(teacher.user)
                message.save()
            return redirect('manage-teachers')
    else:
        form = MessageForm()

    return render(request, 'messagerie/admin_to_subject_teachers.html', {'form': form, 'target': subject, 'type': 'subject'})

@staff_member_required
def admin_to_teachers_by_classe(request, classe_id):
    classe = get_object_or_404(Class, id=classe_id)
    teachers = classe.teachers.all()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            for teacher in teachers:
                message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
                message.recipients.add(teacher.user)
                message.save()
            return redirect('manage-teachers')
    else:
        form = MessageForm()

    return render(request, 'messagerie/admin_to_class_teachers.html', {'form': form, 'target': classe, 'type': 'classe'})


@login_required
def teacher_to_class_students(request, class_id):

    classe = get_object_or_404(Class, id=class_id)
    teacher = get_object_or_404(Teacher, user=request.user)
    # Vérifiez que l'enseignant enseigne cette classe
    if not classe in teacher.classes.all():
        return redirect('teacher-profile')  # Redirigez vers la page d'accueil ou une autre page si l'enseignant n'enseigne pas cette classe
    students = Student.objects.filter(classe=classe)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            sender = request.user
            for student in students:
                message = Message.objects.create(sender=sender, subject=subject, body=body, file=file)
                message.recipients.add(student.user)
                message.save()
            return redirect('teacher-profile')  # Rediriger vers une page de confirmation ou de détails de la classe
    else:
        form = MessageForm()
    return render(request, 'messagerie/teacher_to_class_students.html', {'form': form, 'classe': classe})









