# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import zipfile
import json
from tempfile import TemporaryFile
from functools import wraps

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from trojsten.diplomas.generator import DiplomaGenerator
from trojsten.diplomas.forms import DiplomaParametersForm
from trojsten.diplomas.models import DiplomaTemplate

from wiki.decorators import get_article
from .sources import SOURCE_CLASSES


def staff_only(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to access this section")
        return f(request, *args, **kwargs)
    return wrapper


@staff_only
@csrf_exempt
def source_request(request, source_class):
    source_instance = SOURCE_CLASSES[source_class]()
    user_data = source_instance.handle_request(request)
    return JsonResponse(user_data, safe=False)


@staff_only
@login_required
def diploma_sources(request, diploma_id):
    diploma = DiplomaTemplate.objects.get(pk=diploma_id)
    sources = []
    for source in diploma.sources.all():
        src = source.source_class()
        sources.append({'html': src.render(),
                        'name': src.name,
                        'verbose_name': source.name
                        })
    return render(request, 'trojsten/diplomas/sources.html', {'sources': sources})


@staff_only
@login_required
def diploma_preview(request, diploma_id):
    diploma = DiplomaTemplate.objects.get(pk=diploma_id)
    if diploma:
        png = DiplomaGenerator.render_png(diploma.svg)
        return HttpResponse(png, content_type="image/png")
    else:
        return HttpResponseNotFound()


@staff_only
@get_article
@login_required
def view_diplomas(request, article, *args, **kwargs):

    diploma_templates = DiplomaTemplate.objects.get_queryset().order_by('name')
    editable_fields = {}
    svgs = {}
    for d in diploma_templates:
        editable_fields[d.pk] = sorted(d.editable_fields)
        svgs[d.pk] = d.svg

    if request.method == 'POST':
        form = DiplomaParametersForm(diploma_templates, request.POST, request.FILES)
        if form.is_valid():

            participants_data = form.cleaned_data['participants_data']
            print(form.cleaned_data['editor'])
            separate = not form.cleaned_data['join_pdf']
            template_pk = form.cleaned_data['template']
            svg = diploma_templates.filter(pk=template_pk).get().svg

            generator = DiplomaGenerator()
            pdfs = generator.create_diplomas(participants_data, template_svg=svg, separate=separate)

            archive_file = TemporaryFile(mode='w+b')
            with zipfile.ZipFile(archive_file, 'w', zipfile.ZIP_DEFLATED) as archive:
                for name, content in pdfs:
                    archive.writestr(name, content)
            archive_file.seek(0)

            filename = timezone.now().strftime("diplom_{}_%Y_%m_%d_%H:%M:%S.zip".format(request.user.last_name))

            response = HttpResponse()
            response['Content-type'] = 'application/zip'
            response['Content-Description'] = 'File Transfer'
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            response['Content-Transfer-Encoding'] = 'binary'

            response.write(archive_file.read())

            archive_file.close()

            return response

        else:
            for field in form:
                for error in field.errors:
                    messages.add_message(request, messages.ERROR,
                                         '%s: %s' % (field.label, error))
    else:
        form = DiplomaParametersForm(diploma_templates)

    context = {
        'form': form,
        'article': article,
        'template_fields': json.dumps(editable_fields, ensure_ascii=False).encode('utf8')
    }

    return render(
        request, 'trojsten/diplomas/view_diplomas.html', context
    )