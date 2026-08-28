from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Report

def report_content_view(request):
    if request.method == 'POST':
        content_type = request.POST.get('content_type', 'entity')
        content_id = request.POST.get('content_id')
        reason = request.POST.get('reason', 'other')
        details = request.POST.get('details', '').strip()
        next_url = request.POST.get('next', '/')
        
        if content_id:
            Report.objects.create(
                reported_by=request.user if request.user.is_authenticated else None,
                content_type=content_type,
                content_id=int(content_id),
                reason=reason,
                details=details
            )
            messages.success(request, "Thank you. Your report has been submitted to moderators for review.")
        return redirect(next_url)
    return redirect('home')
