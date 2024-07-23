from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def manage_parents(request):
    user = request.user
    return render(request, 'admin_parent/manage_parents.html',{'user': user})