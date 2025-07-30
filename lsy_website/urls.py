"""
URL configuration for lsy_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import accueil.views
import administration.views
import authentication.views
import student.views
import teacher.views
import messagerie.views
import admin_teacher.views
import admin_student.views
import admin_parent.views
import parent.views
import admin_website.views


urlpatterns = [
    path('admin/', admin.site.urls),
    #--------------------------------------------------------------------------------------------------------------------------
    path('', accueil.views.home, name='accueil'),
    path('accueil/director-speech/', accueil.views.director_speech, name='director-speech'),
    path('lycee/histoire/', accueil.views.lycee_histoire, name='lycee-histoire'),
    path('lycee/mission-vision/', accueil.views.lycee_mission_vision, name='lycee-mission-vision'),
    path('foundation-and-vision/', accueil.views.foundation_and_vision, name='foundation-and-vision'),
    path('excellence-education/', accueil.views.excellence_education, name='excellence-education'),
    path('lycee/administration/', accueil.views.lycee_administration, name='administration'),
    path('lycee/infrastructures-equipements/', accueil.views.lycee_infras_equipements, name='infras-equipements'),
    path('ressources/reglements/', accueil.views.reglements_interieurs, name='reglements-interieurs'),
    path('ressources/admission/', accueil.views.admission, name='admission'),
    path('ressources/admission/criteres-admission/', accueil.views.criteres_admission, name='criteres-admission'),
    path('ressources/admission/procedure-candidature/', accueil.views.procedure_candidature,
         name='procedure-candidature'),
    path('ressources/annales/', accueil.views.annales_list, name='annales-list'),
    path('alumni/network/', accueil.views.alumni_network, name='alumni-network'),
    path('alumni/activties/', accueil.views.alumni_activities, name='alumni-activities'),
    path('actualites/', accueil.views.news, name='news'),
    path('actualite/<int:pk>/', accueil.views.news_detail, name='news-detail'),
    path('evenements/', accueil.views.events, name='events'),
    path('evenement/<int:pk>/', accueil.views.event_detail, name='event-detail'),
    path('temoignages/', accueil.views.temoignage_list, name='temoignages'),
    path('temoignages/<int:pk>/', accueil.views.temoignage_detail, name='temoignage-detail'),
    path('galerie/', accueil.views.galerie, name='gallerie'),
    path('confirmation/', accueil.views.confirmation_view, name='confirmation'),
    path('contact/', accueil.views.contact_view, name='contact'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('portail/', authentication.views.welcome, name='welcome'),
    path('login/', authentication.views.LoginPage.as_view(), name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('password-reset-request/',  authentication.views.password_reset_request_view, name='password-reset-request'),
    path('password_reset/', authentication.views.custom_password_reset_request_view, name='password_reset'),
    path('password_reset/done/', authentication.views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', authentication.views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', authentication.views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-reset-request/confirmation/',  authentication.views.confirmation_password, name='confirmation-password-request'),
    path('register/student/', authentication.views.student_register, name='student_register'),
    path('register/student/pdf/<str:username>/<str:full_name>/<str:classe>/<str:password>/',
         authentication.views.generate_pdf_student, name='generate-pdf-student'),
    path('register/teacher/', authentication.views.teacher_register, name='teacher_register'),
    path('register/teacher/pdf/<str:username>/<str:full_name>/<str:matiere>/<str:classes>/<str:password>/',
         authentication.views.generate_pdf_teacher, name='generate-pdf-teacher'),
    path('register/parent/', authentication.views.parent_register, name='parent_register'),
    path('register/parent/pdf/<str:username>/<str:full_name>/<str:password>/', authentication.views.generate_pdf_parent,
         name='generate-pdf-parent'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('student-profile/', student.views.student_profile, name='student-profile'),
    path('student/absences/', student.views.student_absences, name='student-absences'),
    path('student/notifications/', student.views.student_notifications, name='student-notifications'),
    path('student/notifications/unread/', student.views.unread_notifications_count_student,
         name='unread-notifications-count-student'),
    path('student/<int:student_id>/notes/', student.views.student_notes, name='student-notes'),
    path('student/schedule/', student.views.student_schedule, name='student-schedule'),
    path('student/change-password/', student.views.student_change_password, name='student-change-password'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('teacher/profile/', teacher.views.teacher_profile, name='teacher-profile'),
    path('teacher/change-password/', teacher.views.teacher_change_password, name='teacher-change-password'),
    path('teacher/schedule/', teacher.views.teacher_schedule, name='teacher-schedule'),
    path('teacher/notifications/', teacher.views.teacher_notifications, name='teacher-notifications'),
    path('teacher/notifications/unread/', teacher.views.unread_notifications_count_teacher,
         name='unread-notifications-count-teacher'),
    path('teacher/sent-messages/', teacher.views.teacher_sent_messages, name='teacher-sent-messages'),
    path('teacher/classes/', teacher.views.teacher_classes_view, name='teacher-classes'),
    path('teacher/classes/<int:class_id>/students/', teacher.views.class_students_view, name='teacher-class-students'),
    path('teacher/note/add/<int:student_id>/<int:subject_id>/', teacher.views.add_note_view, name='teacher-add-note'),
    path('teacher/note/edit/<int:note_id>/', teacher.views.edit_note_view, name='teacher-edit-note'),
    path('teacher/note/delete/<int:note_id>/', teacher.views.delete_note_view, name='teacher-delete-note'),
    path('teacher/add-absence/<int:student_id>/', teacher.views.add_absence_view, name='teacher-add-absence'),
    path('add-notes/<int:class_id>/', teacher.views.add_notes_class, name='add-notes-class'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('parent-dashboard/', parent.views.parent_dashboard, name='parent-dashboard'),
    path('parent/change-password/', parent.views.parent_change_password, name='parent-change-password'),
    path('parent/notifications/', parent.views.parent_notifications, name='parent-notifications'),
    path('parent/notifications/unread/', parent.views.unread_notifications_count_parent,
         name='unread-notifications-count-parent'),
    path('parent/children-details/', parent.views.children_details, name='children-details'),
    path('parent/children-details/schedule/', parent.views.children_schedule, name='children-schedule'),
    path('parent/children-details/performance/', parent.views.children_performance, name='children-performance'),
    path('parent/prendre-rendez-vous/motif/', parent.views.choisir_motif, name='choisir-motif'),
    path('parent/prendre-rendez-vous/creneau/', parent.views.choisir_creneau, name='choisir-creneau'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('admin-profile/', administration.views.admin_dashboard, name='admin-profile'),
    path('admin-profile/notifications/', administration.views.admin_notifications, name='admin-notifications'),
    path('admin-profile/notifications/unread/', administration.views.unread_notifications_count,
         name='unread-notifications-count'),
    path('admin-profile/sent-messages/', administration.views.admin_sent_messages, name='admin-sent-messages'),
    path('admin-profile/change-password/', administration.views.admin_change_password, name='admin-change-password'),
    path('admin-profile/configuration/', administration.views.configuration, name='configuration'),
    path('admin-profile/configuration/coefficients-matieres/', administration.views.coefficients_matieres,
         name='coefficients-matieres'),
    path('admin-profile/edit_coefficients/<int:coefficient_id>/', administration.views.edit_coefficients,
         name='edit-coefficients'),
    path('admin-profile/configuration/<int:class_id>/', administration.views.manage_coefficients,
         name='manage-coefficients'),
    path('admin-profile/list-subjects/', administration.views.list_subjects, name='list-subjects'),
    path('admin-profile/classes/', administration.views.list_classes, name='list-classes'),
    path('admin-profile/configuration/list-classes', administration.views.schedule_class_list,
         name='schedule-class-list'),
    path('admin-profile/configuration/list-classes/<int:class_id>/schedule-students/',
         administration.views.schedule_students_view, name='schedule-students-view'),
    path('admin-profile/configuration/list-classes/<int:class_id>/schedule-students/add/',
         administration.views.schedule_students_create, name='schedule-students-create'),
    path('admin-profile/configuration/list-classes/<int:schedule_id>/schedule-students/edit/',
         administration.views.schedule_students_edit, name='schedule-students-edit'),
    path('admin-profile/configuration/schedule/teachers/', administration.views.schedule_teacher_list,
         name='schedule-teacher-list'),
    path('admin-profile/configuration/schedule/teacher/<int:teacher_id>/', administration.views.schedule_teacher_view,
         name='schedule-teacher-view'),
    path('admin-profile/configuration/schedule/teacher/<int:teacher_id>/add/',
         administration.views.schedule_teacher_create, name='schedule-teacher-create'),
    path('admin-profile/configuration/schedule/teacher/edit/<int:schedule_id>/',
         administration.views.schedule_teacher_edit, name='schedule-teacher-edit'),
    path('admin-profile/configuration/list-classes-subjects/', administration.views.list_classes_subjects,
         name='list-classes-subjects'),
    path('admin-profile/configuration/list-classes-subjects/add-class/', administration.views.add_class,
         name='add-class'),
    path('admin-profile/configuration/list-classes-subjects/add-subject/', administration.views.add_subject,
         name='add-subject'),
    path('admin-profile/configuration/delete-class/<int:id>/', administration.views.delete_class, name='delete-class'),
    path('admin-profile/configuration/delete-subject/<int:id>/', administration.views.delete_subject,
         name='delete-subject'),
    path('admin-profile/configuration/informations/', administration.views.information_list, name='information-list'),
    path('admin-profile/configuration/informations/add/', administration.views.information_add, name='information-add'),
    path('admin-profile/configuration/informations/edit/<int:pk>/', administration.views.information_edit,
         name='information-edit'),
    path('admin-profile/configuration/informations/delete/<int:pk>/', administration.views.information_delete,
         name='information-delete'),
    path('admin_profile/configuration/ai-suggestions/', administration.views.ai_suggestions, name='ai-suggestions'),
    path('admin_profile/configuration/get-ai_suggestions/', administration.views.get_ai_suggestions, name='ai-api_suggestions'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('admin-profile/configuration/actualites/', admin_website.views.actualites, name='actualites'),
    path('admin-profile/configuration/actualites/<int:pk>/', admin_website.views.actualite_detail,
         name='actualite-detail'),
    path('admin-profile/configuration/ajouter_actualite/', admin_website.views.ajouter_actualite,
         name='ajouter-actualite'),
    path('admin-profile/configuration/modifier_actualite/<int:pk>/', admin_website.views.modifier_actualite,
         name='modifier-actualite'),
    path('admin-profile/configuration/supprimer_actualite/<int:pk>/', admin_website.views.supprimer_actualite,
         name='supprimer-actualite'),
    path('admin-profile/configuration/evenements/', admin_website.views.evenements, name='evenements'),
    path('admin-profile/configuration/evenements/<int:pk>/', admin_website.views.evenement_detail,
         name='evenement-detail'),
    path('admin-profile/configuration/ajouter_evenement/', admin_website.views.ajouter_evenement,
         name='ajouter-evenement'),
    path('admin-profile/configuration/modifier_evenement/<int:pk>/', admin_website.views.modifier_evenement,
         name='modifier-evenement'),
    path('admin-profile/configuration/supprimer_evenement/<int:pk>/', admin_website.views.supprimer_evenement,
         name='supprimer-evenement'),
    path('admin-profile/configuration/annales-add/', admin_website.views.add_annale, name='add-annale'),
    path('admin-profile/configuration/annales-manage/', admin_website.views.admin_annales_manage,
         name='admin-annales-manage'),
    path('admin-profile/configuration/annales-manage/delete/<int:annale_id>/', admin_website.views.delete_annale,
         name='delete-annale'),
    path('admin-profile/configuration/testimonials/', admin_website.views.testimonials, name='testimonials'),
    path('admin-profile/configuration/testimonials/<int:pk>/', admin_website.views.testimonial_detail,
         name='testimonial-detail'),
    path('admin-profile/configuration/testimonials/add/', admin_website.views.add_testimonial, name='add-testimonial'),
    path('admin-profile/configuration/testimonials/edit/<int:pk>/', admin_website.views.edit_testimonial,
         name='edit-testimonial'),
    path('admin-profile/configuration/testimonials/delete/<int:pk>/', admin_website.views.delete_testimonial,
         name='delete-testimonial'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('admin-profile/classes/<int:class_id>/students/', admin_student.views.list_students_by_class,
         name='students-by-class'),
    path('admin-profile/student/<int:student_id>/', admin_student.views.student_details, name='student-details'),
    path('admin-profile/student/<int:student_id>/delete/', admin_student.views.delete_confirm_student,
         name='delete-confirm-student'),
    path('admin-profile/student/<int:student_id>/delete-confirm/', admin_student.views.delete_student,
         name='delete-student'),
    path('admin-profile/student/<int:student_id>/notes-add/', admin_student.views.add_note, name='add-note'),
    path('admin-profile/student/note/edit/<int:note_id>/', admin_student.views.edit_note, name='edit-note'),
    path('admin-profile/student/note/delete-confirm/<int:note_id>/', admin_student.views.delete_note,
         name='delete-note'),
    path('admin-profile/manage-students/', admin_student.views.manage_students, name='manage-students'),
    path('admin-profile/search-students/', admin_student.views.search_students, name='search-students'),
    path('admin-profile/student/<int:student_id>/add-absence/', admin_student.views.add_absence, name='add-absence'),
    path('admin-profile/student/absence/<int:absence_id>/delete/', admin_student.views.delete_absence,
         name='delete-absence'),
    path('admin-profile/student/notes-classes/', admin_student.views.notes_classes, name='notes-classes'),
    path('admin-profile/student/notes-classes/s/<int:class_id>/add-notes/', admin_student.views.add_notes_to_class, name='add-notes-to-class'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('admin-profile/manage-teachers/', admin_teacher.views.manage_teachers, name='manage-teachers'),
    path('admin-profile/search-teachers/', admin_teacher.views.search_teachers, name='search-teachers'),
    path('admin-profile/teacher/<int:teacher_id>/delete/', admin_teacher.views.delete_confirm_teacher,
         name='delete-confirm-teacher'),
    path('admin-profile/teacher/<int:teacher_id>/delete-confirm/', admin_teacher.views.delete_teacher,
         name='delete-teacher'),
    path('admin-profile/teachers-by-subject/<int:subject_id>/', admin_teacher.views.teachers_by_subject,
         name='teachers-by-subject'),
    path('admin-profile/teacher/<int:teacher_id>/', admin_teacher.views.teacher_details, name='teacher-details'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('admin-profile/manage-parents/', admin_parent.views.manage_parents, name='manage-parents'),
    path('admin-profile/search-parents/', admin_parent.views.search_parents, name='search-parents'),
    path('admin-profile/manage-parents/list-parents', admin_parent.views.list_parents, name='list-parents'),
    path('admin-profile/parent/<int:parent_id>/', admin_parent.views.parent_details, name='parent-details'),
    path('admin-profile/parent/<int:parent_id>/delete/', admin_parent.views.delete_confirm_parent,
         name='delete-confirm-parent'),
    path('admin-profile/parent/<int:parent_id>/delete-confirm/', admin_parent.views.delete_parent,
         name='delete-parent'),
    path('admin-profile/manage-parents/admin/creneaux/', admin_parent.views.gestion_creneaux, name='gestion-creneaux'),
    path('admin-profile/manage-parents/admin/creneaux/ajouter/', admin_parent.views.ajouter_creneau,
         name='ajouter-creneau'),
    path('admin-profile/manage-parents/admin/creneaux/supprimer/<int:creneau_id>/',
         admin_parent.views.supprimer_creneau, name='supprimer-creneau'),
    path('admin-profile/manage-parents/rendezvous/', admin_parent.views.rendezvous_list, name='appointments'),
    #--------------------------------------------------------------------------------------------------------------------------
    path('messages/admin-student/<int:student_id>/send-message/', messagerie.views.admin_to_unique_student,
         name='admin-to-unique-student'),
    path('messages/student-admin/send-message/', messagerie.views.student_to_admin, name='student-to-admin'),
    path('messages/admin-classe/<int:class_id>/send-message/', messagerie.views.admin_to_students_by_class,
         name='admin-to-class'),
    path('messages/admin-students/send-message/', messagerie.views.admin_to_all_students, name='admin-to-all-students'),
    path('messages/admin-teacher/<int:teacher_id>/send-message/', messagerie.views.admin_to_unique_teacher,
         name='admin-to-unique-teacher'),
    path('messages/teacher-admin/send-message/', messagerie.views.teacher_to_admin, name='teacher-to-admin'),
    path('messages/subjects/', messagerie.views.message_subjects_classes, name='message-subjects'),
    path('messages/admin-teachers/send-message/', messagerie.views.admin_to_all_teachers, name='admin-to-all-teachers'),
    path('messages/teacher-class/<int:class_id>/send-message/', messagerie.views.teacher_to_class_students,
         name='teacher-to-class-students'),
    path('messages/admin-teachers-subject/<int:subject_id>/', messagerie.views.admin_to_teachers_by_subject,
         name='admin-teachers-subject'),
    path('messages/admin-teachers-classe/<int:classe_id>/', messagerie.views.admin_to_teachers_by_classe,
         name='admin-teachers-classe'),
    path('messages/parent-admin/send-message/', messagerie.views.parent_to_admin, name='parent-to-admin'),
    path('messages/admin-parent/<int:parent_id>/send-message/', messagerie.views.admin_to_unique_parent,
         name='admin-to-unique-parent'),
    path('messages/admin-parents/send-message/', messagerie.views.admin_to_all_parents, name='admin-to-all-parents'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
handler404 = 'authentication.views.custom_404_view'
handler500 = 'authentication.views.custom_500_view'
"""