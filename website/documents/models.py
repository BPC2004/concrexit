from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from utils.translation import ModelTranslateMeta, MultilingualField
from utils.validators import validate_file_extension


class Document(models.Model, metaclass=ModelTranslateMeta):
    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    DOCUMENT_CATEGORIES = (
        ('annual', _('Annual document')),
        ('association', _('Association document')),
        ('minutes', _('Minutes')),
        ('misc', _('Miscellaneous document')),
    )

    name = MultilingualField(
        models.CharField,
        verbose_name=_('name'),
        max_length=200
    )

    created = models.DateTimeField(
        verbose_name=_('created'),
        auto_now_add=True,
    )

    last_updated = models.DateTimeField(
        verbose_name=_('last updated'),
        auto_now=True
    )

    category = models.CharField(
        max_length=40,
        choices=DOCUMENT_CATEGORIES,
        verbose_name=_('category'),
        default='misc',
    )

    file = MultilingualField(
        models.FileField,
        verbose_name=_('file'),
        upload_to='documents/',
        validators=[validate_file_extension],
    )

    members_only = models.BooleanField(
        verbose_name=_('members only'),
        default=False
    )

    def __str__(self):
        return '%s (%s)' % (self.name, str(self.created.date()))


class AnnualDocument(Document):
    class Meta:
        verbose_name = _('Annual document')
        verbose_name_plural = _('Annual documents')
        unique_together = ('subcategory', 'year')

    SUBCATEGORIES = (
        ('report', _('Annual report')),
        ('financial', _('Financial report')),
        ('policy', _('Policy document')),
    )

    subcategory = models.CharField(
        max_length=40,
        choices=SUBCATEGORIES,
        verbose_name=_('category'),
        default='report',
    )

    year = models.IntegerField(
        verbose_name=_('year'),
        validators=[MinValueValidator(1990)],
    )

    def save(self, *args, **kwargs):
        self.category = 'annual'
        if self.subcategory == 'report':
            self.name_en = 'Annual report %d' % self.year
            self.name_nl = 'Jaarverslag %d' % self.year
        elif self.subcategory == 'financial':
            self.name_en = 'Financial report %d' % self.year
            self.name_nl = 'Financieel jaarverslag %d' % self.year
        else:
            self.name_en = 'Policy document %d' % self.year
            self.name_nl = 'Beleidsdocument %d' % self.year
        super().save(*args, **kwargs)


class AssociationDocumentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category='association')


class AssociationDocument(Document):
    class Meta:
        verbose_name = _('Miscellaneous association document')
        verbose_name_plural = _('Miscellaneous association documents')
        proxy = True

    objects = AssociationDocumentManager()

    def save(self, *args, **kwargs):
        self.category = 'association'
        super().save(*args, **kwargs)


class MiscellaneousDocumentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category='misc')


class MiscellaneousDocument(Document):
    class Meta:
        verbose_name = _('Miscellaneous document')
        verbose_name_plural = _('Miscellaneous documents')
        proxy = True

    objects = MiscellaneousDocumentManager()

    def save(self, *args, **kwargs):
        self.category = 'misc'
        super().save(*args, **kwargs)


class GeneralMeeting(models.Model, metaclass=ModelTranslateMeta):
    class Meta:
        verbose_name = _('General meeting')
        verbose_name_plural = _('General meetings')
        ordering = ['datetime']

    documents = models.ManyToManyField(
        Document,
    )

    datetime = models.DateTimeField(
        verbose_name=_('datetime'),
    )

    location = MultilingualField(
        models.CharField,
        verbose_name=_('location'),
        max_length=200
    )

    def __str__(self):
        return timezone.localtime(self.datetime).strftime('%Y-%m-%d')


class Minutes(Document):
    class Meta:
        verbose_name = _('Minutes')
        verbose_name_plural = _('Minutes')

    meeting = models.OneToOneField(
        GeneralMeeting,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.category = 'minutes'
        self.name_en = 'Minutes %s' % str(self.meeting.datetime.date())
        self.name_nl = 'Notulen %s' % str(self.meeting.datetime.date())
        super().save(*args, **kwargs)
