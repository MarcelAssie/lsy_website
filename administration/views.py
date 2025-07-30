from django.shortcuts import redirect,get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Subject, Coefficient, Class, Schedule,TeacherSchedule, Information
from authentication.models import Student, Parent, Teacher
from messagerie.models import Message
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count
from django.db import connections
from django.http import JsonResponse
import json
import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
from .forms import (CoefficientForm, ClassSelectionForm, ScheduleStudentForm,
                    ScheduleTeacherForm, ClassForm, SubjectForm, InformationForm)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_dashboard(request):
    """
    Affiche le tableau de bord d'administration avec des statistiques sur les élèves, enseignants, et parents.
    """
    # Statistiques sur les élèves par classe
    students_per_class = Student.objects.values('classe__name').annotate(count=Count('id')).order_by('classe__name')

    # Statistiques sur les enseignants par matière
    teachers_per_subject = Teacher.objects.values('matiere__name').annotate(count=Count('id')).order_by('matiere__name')

    # Nombre total d'enseignants
    total_teachers = Teacher.objects.count()

    # Nombre total de parents
    total_parents = Parent.objects.count()

    # Nombre total d'élèves
    total_students = Student.objects.count()

    # Passer les données au template
    context = {
        'students_per_class': students_per_class,
        'teachers_per_subject': teachers_per_subject,
        'total_teachers': total_teachers,
        'total_parents': total_parents,
        'total_students': total_students,
    }
    return render(request, 'administration/admin_dashboard.html', context)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_notifications(request):
    """
    Affiche les notifications reçues par l'utilisateur administrateur et marque les notifications comme lues.
    """
    received_messages = Message.objects.filter(recipients=request.user).order_by('-timestamp')
    unread_notifications_count = received_messages.filter(is_read=False).count()
    received_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'administration/admin_notifications.html', {
        'received_messages': received_messages,
        'unread_notifications_count': unread_notifications_count
    })
@login_required
@user_passes_test(lambda user: user.is_superuser)
def unread_notifications_count(request):
    """
    Renvoie le nombre de notifications non lues en format JSON.
    """
    count = Message.objects.filter(recipients=request.user, is_read=False).count()
    return JsonResponse({'unread_notifications_count': count})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_sent_messages(request):
    """
    Affiche les messages envoyés par l'utilisateur administrateur.
    """
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'administration/admin_sent_messages.html', {'sent_messages': sent_messages})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_change_password(request):
    """
    Permet à l'administrateur de changer son mot de passe.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('admin-change-password')
        else:
            messages.error(request, 'Echec ! Mot de passe inchangé.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'administration/admin_change_password.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_classes_subjects(request):
    """
    Affiche la liste des classes et matières, avec la possibilité de les supprimer.
    """
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        # Handle the deletion confirmation via POST
        if 'delete_class' in request.POST:
            class_id = request.POST.get('delete_class')
            class_to_delete = get_object_or_404(Class, id=class_id)
            class_to_delete.delete()
        elif 'delete_subject' in request.POST:
            subject_id = request.POST.get('delete_subject')
            subject_to_delete = get_object_or_404(Subject, id=subject_id)
            subject_to_delete.delete()
        return redirect('list-classes-subjects')

    return render(request, 'administration/list_classes_subjects.html', {'classes': classes, 'subjects': subjects})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_class(request):
    """
    Permet d'ajouter une nouvelle classe.
    """
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data['name']
            if Class.objects.filter(name=class_name).exists():
                messages.error(request, "Cette classe existe déjà.")
            else:
                form.save()
                messages.success(request, "Classe ajoutée avec succès.")
                return redirect('add-class')
    else:
        form = ClassForm()
    return render(request, 'administration/add_class.html', {'form': form})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_subject(request):
    """
    Permet d'ajouter une nouvelle matière.
    """
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data['name']
            if Subject.objects.filter(name=subject_name).exists():
                messages.error(request, "Cette matière existe déjà.")
            else:
                form.save()
                messages.success(request, "Matière ajoutée avec succès.")
                return redirect('add-subject')
    else:
        form = SubjectForm()
    return render(request, 'administration/add_subject.html', {'form': form})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_class(request, id):
    """
    Supprime une classe après confirmation via POST.
    """
    if request.method == 'POST':
        class_to_delete = get_object_or_404(Class, id=id)
        class_to_delete.delete()
        return redirect('list-classes-subjects')
@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_subject(request, id):
    """
    Supprime une matière après confirmation via POST.
    """
    if request.method == 'POST':
        subject_to_delete = get_object_or_404(Subject, id=id)
        subject_to_delete.delete()
        return redirect('list-classes-subjects')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_classes(request):
    """
    Affiche la liste des classes.
    """
    classes = Class.objects.all()
    return render(request, 'administration/list_classes.html', {'classes': classes})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_subjects(request):
    """
    Affiche la liste des matières.
    """
    matieres = Subject.objects.all()
    return render(request, 'administration/list_subjects.html', {'matieres': matieres})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def configuration(request):
    """
    Affiche la page de configuration.
    """
    return render(request, 'administration/configuration.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def coefficients_matieres(request):
    """
    Permet de sélectionner une classe pour gérer les coefficients des matières.
    """
    if request.method == 'POST':
        form = ClassSelectionForm(request.POST)
        if form.is_valid():
            selected_class = form.cleaned_data['school_class']
            return redirect('manage-coefficients', class_id=selected_class.id)
    else:
        form = ClassSelectionForm()

    return render(request, 'administration/coefficients_matieres.html', {'form': form})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def manage_coefficients(request, class_id):
    """
    Gère les coefficients des matières pour une classe sélectionnée.
    """
    school_class = Class.objects.get(id=class_id)
    subjects = Subject.objects.all()

    if request.method == 'POST':
        form = CoefficientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-coefficients', class_id=class_id)
    else:
        form = CoefficientForm(initial={'school_class': school_class})

    coefficients = Coefficient.objects.filter(school_class=school_class)

    return render(request, 'administration/manage_coefficients.html', {
        'school_class': school_class,
        'subjects': subjects,
        'coefficients': coefficients,
        'form': form
    })
@login_required
@user_passes_test(lambda user: user.is_superuser)
def edit_coefficients(request, coefficient_id):
    """
    Permet de modifier un coefficient spécifique.
    """
    coefficient = get_object_or_404(Coefficient, id=coefficient_id)
    if request.method == 'POST':
        form = CoefficientForm(request.POST, instance=coefficient)
        if form.is_valid():
            form.save()
            return redirect('manage-coefficients', class_id=coefficient.school_class.id)
    else:
        form = CoefficientForm(instance=coefficient)
    return render(request, 'administration/edit_coefficients.html', {
        'form': form,
        'coefficient': coefficient
    })
@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_class_list(request):
    """
    Affiche la liste des classes pour la gestion des emplois du temps.
    """
    classes = Class.objects.all()
    return render(request, 'administration/schedule_list_classes.html', {'classes': classes})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_students_create(request, class_id):
    """
    Permet de créer un emploi du temps pour une classe spécifique.
    """
    class_instance = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        form = ScheduleStudentForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.class_name = class_instance
            schedule.save()
            return redirect('schedule-students-create', class_id=class_instance.id)  # Redirige vers la même page
    else:
        form = ScheduleStudentForm(initial={'class_name': class_instance})
    return render(request, 'administration/students_schedule_form.html', {'form': form, 'class_instance': class_instance})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_students_view(request, class_id):
    """
    Affiche l'emploi du temps d'une classe sous forme de tableau.
    """
    class_instance = get_object_or_404(Class, id=class_id)
    schedules = Schedule.objects.filter(class_name=class_instance).order_by('start_time')

    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    time_slots = sorted(set((s.start_time, s.end_time) for s in schedules))

    # Créer une liste de listes pour stocker les emplois du temps
    schedule_matrix = []
    for start_time, end_time in time_slots:
        row = {'time_slot': f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"}
        for day in days:
            row[day] = None
        schedule_matrix.append(row)

    for schedule in schedules:
        time_slot = f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}"
        for row in schedule_matrix:
            if row['time_slot'] == time_slot:
                row[schedule.day_of_week] = schedule
    context = {
        'class_instance': class_instance,
        'schedule_matrix': schedule_matrix,
        'days': days,
    }
    return render(request, 'administration/students_schedule_view.html', context)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_students_edit(request, schedule_id):
    """
    Permet de modifier un emploi du temps spécifique d'une classe.
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    class_instance = schedule.class_name  # Récupère l'instance de la classe associée
    if request.method == 'POST':
        form = ScheduleStudentForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule-students-edit', schedule_id=schedule.id)  # Redirige vers la même page
    else:
        form = ScheduleStudentForm(instance=schedule)
    return render(request, 'administration/students_schedule_form.html', {'form': form, 'schedule': schedule, 'class_instance': class_instance})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_teacher_list(request):
    """
    Affiche la liste des enseignants pour la gestion de leurs emplois du temps.
    """
    teachers = Teacher.objects.all()
    return render(request, 'administration/schedule_list_teachers.html', {'teachers': teachers})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_teacher_view(request, teacher_id):
    """
    Affiche l'emploi du temps d'un enseignant spécifique sous forme de tableau.
    """
    teacher = get_object_or_404(Teacher, id=teacher_id)
    schedules = TeacherSchedule.objects.filter(teacher=teacher).order_by('start_time')

    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    time_slots = sorted(set((s.start_time, s.end_time) for s in schedules))

    # Créer une liste de listes pour stocker les emplois du temps
    schedule_matrix = []
    for start_time, end_time in time_slots:
        row = {'time_slot': f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"}
        for day in days:
            row[day] = None
        schedule_matrix.append(row)

    for schedule in schedules:
        time_slot = f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}"
        for row in schedule_matrix:
            if row['time_slot'] == time_slot:
                row[schedule.day_of_week] = schedule
    context = {
        'teacher': teacher,
        'schedule_matrix': schedule_matrix,
        'days': days,
    }
    return render(request, 'administration/teacher_schedule_view.html', context)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_teacher_create(request, teacher_id):
    """
    Permet de créer un emploi du temps pour un enseignant spécifique.
    """
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = ScheduleTeacherForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.teacher = teacher
            schedule.save()
            return redirect('schedule-teacher-view', teacher_id=teacher.id)
    else:
        form = ScheduleTeacherForm(initial={'teacher': teacher})
    return render(request, 'administration/teacher_schedule_form.html', {'form': form, 'teacher': teacher})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_teacher_edit(request, schedule_id):
    """
    Permet de modifier un emploi du temps spécifique d'un enseignant.
    """
    schedule = get_object_or_404(TeacherSchedule, id=schedule_id)
    teacher = schedule.teacher
    if request.method == 'POST':
        form = ScheduleTeacherForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule-teacher-view', teacher_id=teacher.id)
    else:
        form = ScheduleTeacherForm(instance=schedule)
    return render(request, 'administration/teacher_schedule_form.html', {'form': form, 'teacher': teacher})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def information_list(request):
    """
    Affiche la liste des informations administratives.
    """
    informations = Information.objects.all().order_by('-created_at')
    return render(request, 'administration/list_informations.html', {'informations': informations})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def information_add(request):
    """
    Permet d'ajouter une nouvelle information administrative.
    """
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('information-list')
    else:
        form = InformationForm()
    return render(request, 'administration/add_information.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def information_edit(request, pk):
    """
    Permet de modifier une information administrative existante.
    """
    information = get_object_or_404(Information, pk=pk)
    if request.method == 'POST':
        form = InformationForm(request.POST, instance=information)
        if form.is_valid():
            form.save()
            return redirect('information-list')
    else:
        form = InformationForm(instance=information)
    return render(request, 'administration/add_information.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def information_delete(request, pk):
    """
    Supprime une information administrative après confirmation via POST.
    """
    information = get_object_or_404(Information, pk=pk)
    if request.method == 'POST':
        information.delete()
        return redirect('information-list')
    return redirect('information-list')


def ai_suggestions(request):
    classes = Class.objects.all()
    return render(request, 'administration/ai_suggestions.html', {'classes': classes})


def students_notes_formated(selected_classes):
    db_connection = connections["default"]
    with db_connection.cursor() as cursor:
        format_strings = ','.join(['%s'] * len(selected_classes))
        query = f"""
            SELECT
                a_s.id_student,
                a_u.first_name AS full_name,
                a_c.name AS class,
                a_su.name AS matiere,
                a_co.coefficient AS coefficient,
                ROUND(AVG(a_n.score), 2) AS moyenne_matiere
            FROM administration_note AS a_n
            JOIN authentication_student AS a_s ON a_n.student_id = a_s.id
            JOIN authentication_user AS a_u ON a_u.id = a_s.user_id
            JOIN administration_class AS a_c ON a_c.id = a_s.classe_id
            JOIN administration_subject AS a_su ON a_su.id = a_n.subject_id
            JOIN administration_coefficient AS a_co
              ON a_co.school_class_id = a_s.classe_id
             AND a_co.subject_id = a_n.subject_id
            WHERE a_c.id IN ({format_strings})
            GROUP BY
                a_s.id_student, a_u.first_name, a_u.last_name,
                a_c.name, a_co.coefficient, a_su.name
            ORDER BY
                full_name, matiere
        """
        cursor.execute(query, selected_classes)
        rows = cursor.fetchall()

    # Structure des résultats par id_student
    grouped_results = {}
    for row in rows:
        id_student, full_name, classe, matiere, coefficient, moyenne = row
        if id_student not in grouped_results:
            grouped_results[id_student] = {
                'id_student': id_student,
                'full_name': full_name,
                'class': classe,
                'notes': []
            }
        grouped_results[id_student]['notes'].append({
            'matiere': matiere,
            'coefficient': coefficient,
            'moyenne_matiere': float(moyenne)
        })
    print(list(grouped_results.values()))
    return list(grouped_results.values())



def get_gemini_connection():
    return genai.Client(api_key=os.getenv("API_KEY"))

def get_ai_response(students_notes, model="gemini-2.5-pro"):
    system_message = """
        
        Tu es un conseiller pédagogique intelligent, bienveillant et expérimenté, spécialisé dans l’analyse personnalisée des résultats scolaires d’élèves de collège et de lycée, en Côte d’Ivoire.
        
        Tu vas recevoir une liste d'élèves, chacun identifié par un identifiant unique (`id_student`), leur classe (ex : 6ème, 5ème, 3ème, Terminale C, etc.), et les détails de leurs résultats scolaires (matières, coefficients, moyennes).
        
        Ta mission est d’aider chaque élève personnellement à progresser dans ses études, en lui parlant directement, comme s’il te lisait. Utilise le tutoiement, sois clair, positif, et encourageant. Chaque élève est unique, et tu t’adresses à lui, pour l’aider à mieux comprendre ses forces et ses axes de progression.
        
        Voici ce que tu dois faire :

        
        1. Analyser les performances de chaque élève, en tenant compte de :
           - L'ensemble de ses matières
           - Les moyennes obtenues dans chaque matière
           - Les coefficients associés à chaque matière (ils indiquent l’importance relative dans l’évaluation globale)
           - Le niveau scolaire et la série (A, C, D) pour un élève de lycée, qui influencent les attentes pédagogiques
        
        2. Identifier les lacunes ou forces de chaque élève, matière par matière.
        
        3. Recommander pour chaque élève :
           - Des ressources pédagogiques pertinentes, spécifiques à ses besoins :
             - Vidéos YouTube éducatives (en français de préférence)
             - Livres ou manuels recommandés
             - Sites web ou plateformes de formation en ligne (gratuits ou réputés)
             - Documents PDF ou supports de révision adaptés
           - Ces recommandations doivent être adaptées au niveau réel de l’élève (pas de ressources universitaires pour un élève de 5ème par exemple).
           - Les ressources doivent être fiables, reconnues et accessibles pour un élève situé en Côte d’Ivoire.
        
        4. Formatez la réponse en JSON structuré, avec une entrée par élève contenant :
           - `id_student` (à conserver tel quel pour assurer le suivi)
           - `class`
           - `summary`: n court texte personnalisé qui s’adresse directement à l’élève. Par exemple :
            > "Tu as de très bons résultats en sciences, bravo ! Il te suffit de revoir un peu l’anglais pour équilibrer ton niveau général. Tu es sur la bonne voie !"
           - `matières`: une liste de ses matières avec :
             - moyenne
             - coefficient
             - recommandations obligatoires (ressources pédagogiques)
           - `recommandations générales`: conseils pédagogiques transversaux (format text brut)
        
        Format de réponse attendu : retourne un tableau JSON (absolument aucun texte en dehors du json, vraiment aucun du tout en dehors du json), avec un objet par élève structuré comme ceci :
        
        ```json
        [
          {
            "id_student": "abc123",
            "class": "Classe de l'élève",
            "summary": "un bref résumé de son profil académique",
            "recommendations": [
              {
                "matiere": "Mathématiques",
                "moyenne": "Moyenne de l'élève",
                "coefficient": "Coefficient de la matière",
                "type_ressource": "vidéo YouTube",
                "titre": "Apprendre les fractions facilement",
                "lien": "https://youtube.com/.../fractions",
                "description": "Description courte et précise de la ressource et pourquoi elle est utile pour cet élève.",
                "motivation": "L’élève a des difficultés en mathématiques (moyenne < 10) sur une matière à fort coefficient. Cette vidéo explique les bases de manière adaptée aux collégiens."
              },
              {
                "matiere": "Mathématiques",
                "moyenne": "Moyenne de l'élève",
                "coefficient": "Coefficient de la matière",
                "type_ressource": "livre",
                "titre": "Physique-Chimie 4ème - Nathan",
                "lien": "https://...",
                "description": "Description courte et précise de la ressource et pourquoi elle est utile pour cet élève.",
                "motivation": "Renforcer les acquis avec un manuel adapté à son niveau."
              }
            ], 
            "recommandations_generales" : "conseils pédagogiques transversaux (format text brut)"
          },
          ...
        ] 
    """
    try:
        client = get_gemini_connection()
        response = client.models.generate_content(
            model=model,
            contents=[str(students_notes)],
            config=genai.types.GenerateContentConfig(
                temperature=0.1,
                system_instruction=system_message
            ),
        )
        students = response.text
        students_performances = students.replace("```", "").replace("json", "")
        cleaned_json = re.sub(r'[\x00-\x1F\x7F]', '', students_performances.strip())
        students_list = json.loads(cleaned_json)
        db_connection = connections["default"]
        with db_connection.cursor() as cursor:
            try:
                # Création de la table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students_performances (
                        id_student TEXT PRIMARY KEY,
                        summary TEXT,
                        recommendations JSONB,
                        recommandations_generales TEXT
                    );
                """)

                # Insertion des données
                for student in students_list:
                    cursor.execute("""
                        INSERT INTO students_performances (id_student, summary, recommendations, recommandations_generales)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id_student) DO UPDATE SET
                            summary = EXCLUDED.summary,
                            recommendations = EXCLUDED.recommendations,
                            recommandations_generales = EXCLUDED.recommandations_generales;
                    """, [
                        student.get("id_student"),
                        student.get("summary"),
                        json.dumps(student.get("recommendations")),
                        student.get("recommandations_generales")
                    ])
            except Exception as e:
                print(f"Erreur dans le stockage des données : {str(e)}")
        return "Données actualisées"
    except Exception as e:
        print(f"Erreur avec Gemini: {str(e)}")
        return None


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_ai_suggestions(request):
    if request.method == "POST":
        data = json.loads(request.body)
        classes = data.get("classes", [])
        if not classes:
            return JsonResponse({"error": "Aucun message reçu"}, status=400)
        students_notes_structured = students_notes_formated(classes)
        success_info = get_ai_response(students_notes_structured)
        return JsonResponse({"message": success_info})


