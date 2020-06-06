from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect

from quest.models import Level


def load(request: HttpRequest, depth: int, signature: str):
    level = Level.objects.filter(depth=depth)
    if not level.exists():
        return HttpResponseNotFound()

    if level.get().is_signature_wrong(signature):
        return HttpResponseForbidden('Bad signature.')

    request.session['depth'] = depth
    return redirect('view', depth=depth)

