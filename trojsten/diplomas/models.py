# -*- coding: utf-8 -*-
import re

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .constants import FIELD_SEARCH_PATTERN
from .sources import SOURCE_CHOICES, SOURCE_CLASSES


class DiplomaDataSourceManager(models.Manager):
    def get_queryset(self):
        return super(DiplomaDataSourceManager, self).get_queryset().order_by("-is_default")

    def default(self):
        return self.get_queryset().filter(is_default=True) or []


class DiplomaDataSource(models.Model):
    name = models.CharField(max_length=128, verbose_name=_("Source name"))
    class_name = models.CharField(
        max_length=128, choices=SOURCE_CHOICES, verbose_name=_("Source class")
    )
    is_default = models.BooleanField(default=False, verbose_name=_("Add to default sources"))

    objects = DiplomaDataSourceManager()

    @property
    def source_class(self):
        return SOURCE_CLASSES[self.class_name]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Data source for diplomas")
        verbose_name_plural = _("Data sources for diplomas")


class DiplomaTemplate(models.Model):
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    svg = models.TextField()

    sources = models.ManyToManyField(DiplomaDataSource, blank=True, verbose_name=_("Sources"))

    authorized_groups = models.ManyToManyField(
        Group,
        verbose_name=_("Authorized groups"),
        blank=True,
        help_text=_("The groups that are authorized to use this template."),
    )

    class Meta:
        verbose_name = _("Diploma template")
        verbose_name_plural = _("Diploma templates")

    @property
    def editable_fields(self):
        return re.findall(FIELD_SEARCH_PATTERN, self.svg)

    def __str__(self):
        return self.name
