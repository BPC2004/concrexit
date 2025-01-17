"""Registers admin interfaces for the event model."""

from django.contrib import admin, messages
from django.template.defaultfilters import date as _date
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from events import emails, models, services
from events.admin.filters import LectureYearFilter
from events.admin.forms import EventAdminForm, RegistrationInformationFieldForm
from events.admin.inlines import (
    PizzaEventInline,
    PromotionRequestInline,
    RegistrationInformationFieldInline,
)
from events.admin.views import (
    EventAdminDetails,
    EventMarkPresentQR,
    EventRegistrationsExport,
)
from utils.admin import DoNextModelAdmin


@admin.register(models.Event)
class EventAdmin(DoNextModelAdmin):
    """Manage the events."""

    form = EventAdminForm

    inlines = (
        RegistrationInformationFieldInline,
        PizzaEventInline,
        PromotionRequestInline,
    )

    list_display = (
        "overview_link",
        "event_date",
        "registration_date",
        "num_participants",
        "get_organisers",
        "category",
        "published",
        "edit_link",
    )
    list_display_links = ("edit_link",)
    list_filter = (LectureYearFilter, "start", "published", "category")
    actions = ("make_published", "make_unpublished")
    date_hierarchy = "start"
    search_fields = ("title", "description")
    prepopulated_fields = {
        "map_location": ("location",),
    }

    filter_horizontal = ("documents", "organisers")

    fieldsets = (
        (
            _("General"),
            {
                "fields": (
                    "title",
                    "slug",
                    "published",
                    "organisers",
                )
            },
        ),
        (
            _("Detail"),
            {
                "fields": (
                    "category",
                    "start",
                    "end",
                    "description",
                    "caption",
                    "location",
                    "map_location",
                    "show_map_location",
                ),
                "classes": ("collapse", "start-open"),
            },
        ),
        (
            _("Registrations"),
            {
                "fields": (
                    "price",
                    "fine",
                    "tpay_allowed",
                    "max_participants",
                    "registration_without_membership",
                    "registration_start",
                    "registration_end",
                    "cancel_deadline",
                    "send_cancel_email",
                    "optional_registrations",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Registration status messages"),
            {
                "fields": (
                    "no_registration_message",
                    "registration_msg_optional",
                    "registration_msg_optional_registered",
                    "registration_msg_registered",
                    "registration_msg_open",
                    "registration_msg_full",
                    "registration_msg_waitinglist",
                    "registration_msg_will_open",
                    "registration_msg_expired",
                    "registration_msg_cancelled",
                    "registration_msg_cancelled_late",
                    "registration_msg_cancelled_final",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Extra"),
            {"fields": ("documents", "shift"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .select_properties("participant_count")
            .prefetch_related("organisers")
        )
        if not (
            request.user.has_perm("events.override_organiser")
            or request.user.has_perm("events.view_unpublished")
        ):
            queryset_published = queryset.filter(published=True)
            queryset_unpublished = queryset.filter(
                published=False,
                organisers__in=list(
                    request.member.get_member_groups().values_list("id", flat=True)
                ),
            )
            queryset = queryset_published | queryset_unpublished
        return queryset

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
        return form

    def overview_link(self, obj):
        return format_html(
            '<a href="{link}">{title}</a>',
            link=reverse("admin:events_event_details", kwargs={"pk": obj.pk}),
            title=obj.title,
        )

    def has_delete_permission(self, request, obj=None):
        """Only allow deleting an event if the user is an organiser."""
        if obj is not None and not services.is_organiser(request.member, obj):
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        """Only allow access to the change form if the user is an organiser."""
        if obj is not None and not services.is_organiser(request.member, obj):
            return False
        return super().has_change_permission(request, obj)

    def event_date(self, obj):
        event_date = timezone.make_naive(obj.start)
        return _date(event_date, "l d b Y, G:i")

    event_date.short_description = _("Event Date")
    event_date.admin_order_field = "start"

    def registration_date(self, obj):
        if obj.registration_start is not None:
            start_date = timezone.make_naive(obj.registration_start)
        else:
            start_date = obj.registration_start

        return _date(start_date, "l d b Y, G:i")

    registration_date.short_description = _("Registration Start")
    registration_date.admin_order_field = "registration_start"

    def edit_link(self, obj):
        return _("Edit")

    edit_link.short_description = ""

    def num_participants(self, obj):
        """Pretty-print the number of participants."""
        num = obj.participant_count  # prefetched aggregateproperty
        if not obj.max_participants:
            return f"{num}/∞"
        return f"{num}/{obj.max_participants}"

    num_participants.short_description = _("Number of participants")

    def get_organisers(self, obj):
        return ", ".join(str(o) for o in obj.organisers.all())

    get_organisers.short_description = _("Organisers")

    def make_published(self, request, queryset):
        """Change the status of the event to published."""
        self._change_published(request, queryset, True)

    make_published.short_description = _("Publish selected events")

    def make_unpublished(self, request, queryset):
        """Change the status of the event to unpublished."""
        self._change_published(request, queryset, False)

    make_unpublished.short_description = _("Unpublish selected events")

    @staticmethod
    def _change_published(request, queryset, published):
        if not request.user.is_superuser:
            queryset = queryset.filter(
                organisers__in=request.member.get_member_groups()
            )
        queryset.update(published=published)

    def save_formset(self, request, form, formset, change):
        """Save formsets with their order."""
        formset.save()

        informationfield_forms = (
            x
            for x in formset.forms
            if isinstance(x, RegistrationInformationFieldForm)
            and "DELETE" not in x.changed_data
        )
        form.instance.set_registrationinformationfield_order(
            [
                f.instance.pk
                for f in sorted(
                    informationfield_forms,
                    key=lambda x: (x.cleaned_data["order"], x.instance.pk),
                )
            ]
        )
        form.instance.save()

    def save_model(self, request, obj, form, change):
        if change and "max_participants" in form.changed_data:
            prev = self.model.objects.get(id=obj.id)
            prev_limit = prev.max_participants
            self_limit = obj.max_participants
            if prev_limit is None:
                prev_limit = prev.participant_count
            if self_limit is None:
                self_limit = obj.participant_count

            if prev_limit < self_limit and prev_limit < obj.participant_count:
                diff = self_limit - prev_limit
                joiners = prev.queue[:diff]
                for registration in joiners:
                    emails.notify_waiting(obj, registration)
                messages.info(
                    request,
                    "The maximum number of participants was increased. Any members that moved from the waiting list to the participants list have been notified.",
                )
            elif self_limit < prev_limit and self_limit < obj.participant_count:
                diff = self_limit - prev_limit
                leavers = prev.registrations[self_limit:]
                address = map(lambda r: r.email, leavers)
                link = "mailto:?bcc=" + ",".join(address)
                messages.warning(
                    request,
                    format_html(
                        "The maximum number of participants was decreased and some members moved to the waiting list. <a href='{}' style='text-decoration: underline;'>Use this link to send them an email.</a>",
                        link,
                    ),
                )
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if self.has_change_permission(request, obj) or obj is None:
                yield inline.get_formset(request, obj), inline

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:pk>/details/",
                self.admin_site.admin_view(EventAdminDetails.as_view()),
                name="events_event_details",
            ),
            path(
                "<int:pk>/export/",
                self.admin_site.admin_view(EventRegistrationsExport.as_view()),
                name="events_event_export",
            ),
            path(
                "<int:pk>/mark-present-qr/",
                self.admin_site.admin_view(EventMarkPresentQR.as_view()),
                name="events_event_mark_present_qr",
            ),
        ]
        return custom_urls + urls
