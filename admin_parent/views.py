from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import Parent, User
from django.contrib import messages
from django.db import models



@staff_member_required
def manage_parents(request):
    user = request.user
    return render(request, 'admin_parent/manage_parents.html',{'user': user})
@staff_member_required
def list_parents(request):
    parents = Parent.objects.all()
    return render(request, 'admin_parent/list_parents.html', {'parents': parents})
@staff_member_required
def parent_details(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    return render(request, 'admin_parent/parent_details.html', {'parent': parent})
@staff_member_required
def parent_details2(request, parent_id):
    user = get_object_or_404(User, id=parent_id, is_parent=True)
    parent = get_object_or_404(Parent, user=user)
    return render(request, 'admin_parent/parent_details.html', {'parent': parent})

@staff_member_required
def delete_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    user = parent.user
    if request.method == "POST":
        user.delete()
        messages.success(request, 'L\'étudiant a été supprimé avec succès.')
        return redirect('list-parents')
    return redirect('parent-details', parent_id=parent_id)

@staff_member_required
def delete_confirm_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    return render(request, 'admin_parent/delete_confirm_parent.html', {'parent': parent})

@staff_member_required
def search_parents(request):
    parents= User.objects.filter(is_parent=True)
    if request.method == "GET":
        name = request.GET.get('recherche')
        if name:
            parents = parents.filter(
                models.Q(first_name__icontains=name) | models.Q(last_name__icontains=name))
    return render(request, 'admin_parent/manage_parents.html', {'parents': parents})


