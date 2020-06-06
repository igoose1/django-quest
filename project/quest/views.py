from django.http import HttpRequest
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db import transaction

from quest.models import Level, Code


def load(request: HttpRequest, depth: int, signature: str):
    level = Level.objects.filter(depth=depth)
    if not level.exists():
        return HttpResponseNotFound()

    if level.get().is_signature_wrong(signature):
        return HttpResponseForbidden('Bad signature.')

    request.session['depth'] = depth
    return redirect(f'/view/{depth}')


def view(request: HttpRequest, depth:int):
    if request.method == 'POST':
        for code in list(Code.objects.filter(level__depth=depth)):
            if code.is_match(request.POST['code']):
                request.session['depth'] = depth
                return redirect(f'/view/{depth}')
            return redirect(f'/view/{depth - 1}')

    if request.session.get('depth', 0) < depth and request.user.is_anonymous:
        return HttpResponseForbidden('No rights to view this level.')

    is_code_showing = request.session.get('depth', 0) > depth
    is_code_showing |= request.user.is_authenticated
    is_code_showing &= Level.objects.order_by('depth').last().depth > depth
    with transaction.atomic():
        level = Level.objects.get(depth=depth)
        code = Code.objects.filter(
            level__depth=depth + 1
        ).first().string if is_code_showing else ''
        content = level.content
        progress = Level.objects.filter(
            depth__lte=request.session.get('depth', 0)
        ).order_by('depth').values_list('title', flat=True)
        loadlink = reverse(
            load,
            kwargs={
                'depth': request.session.get('depth', 0),
                'signature': level.generate_signature()
            }
        )
        title = level.title

    context = {
        'code': code,
        'content': content,
        'progress': progress,
        'loadlink': loadlink,
        'title': title,
        'depth': depth
    }
        
    return render(request, 'view.html', context)

