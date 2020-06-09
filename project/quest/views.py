from django.http import HttpRequest
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.db import transaction

import random

from quest.models import Level, Code


def start(request: HttpRequest):
    context = {
        'loadlink': Level.objects.first().loadlink
    }
    return render(request, 'start.html', context)


def end(request: HttpRequest):
    if request.session.get('depth', 0) < Level.objects.last().depth:
        return HttpResponseForbidden('You haven\'t solved quest yet.')
    EMOJIS = '🥳🎂🎉🎊 '
    context = {
        'emojis': ''.join(
            [random.choice(EMOJIS) for _ in range(random.randint(100, 5000))]
        )
    }
    return render(request, 'end.html', context=context)


def load(request: HttpRequest, depth: int, signature: str):
    level = Level.objects.filter(depth=depth)
    if not level.exists():
        return HttpResponseNotFound()

    if level.get().is_signature_wrong(signature):
        return HttpResponseForbidden('Bad signature.')

    request.session['depth'] = depth
    return redirect(f'/view/{depth}/')


def view(request: HttpRequest, depth:int):
    user_input, is_user_wrong = None, False
    try:
        level = Level.objects.get(depth=depth)
    except Level.DoesNotExist:
        return HttpResponseNotFound()
    if request.method == 'POST':
        user_input = request.POST.get('code', '')
        if level.is_passed(user_input):
            depth += 1
            request.session['depth'] = depth
            if depth > Level.objects.last().depth:
                return redirect('/end/')
            print(depth, Level.objects.last().depth)
            level = Level.objects.get(depth=depth)
        else:
            is_user_wrong = True

    if request.session.get('depth', 0) < depth and request.user.is_anonymous:
        return HttpResponseForbidden('No rights to view this level.')

    is_code_showing = request.session.get('depth', 0) > depth
    is_code_showing |= request.user.is_authenticated
    with transaction.atomic():
        code = Code.objects.filter(
            level=level
        ).first().string if is_code_showing else ''
        content = level.content
        progress = Level.objects.filter(
            depth__lte=request.session.get('depth', 0)
        ).order_by('depth').values_list('title', flat=True)
        loadlink = Level.objects.get(
            depth=min(
                request.session.get('depth', 0), Level.objects.last().depth
            )
        ).loadlink

        title = level.title

    context = {
        'code': code,
        'content': content,
        'progress': progress,
        'loadlink': loadlink,
        'title': title,
        'depth': depth,
        'user_input': user_input,
        'is_user_wrong': is_user_wrong
    }
        
    return render(request, 'view.html', context)

