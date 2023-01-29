from django.utils.translation import gettext as _

PRESCRIPTION_TYPE = (
    (1, _("Acute (not to be repeated)")),
    (2, _("Repeat (long term medication)")),
    (3, _("Repeat Dispensing (specific amount of ussues)")),
     )

MEDICINE_TYPE = (
    (1, _("Pain relievers")),
    (2, _("Tranquilizers")),
    (3, _("Stimulants")),
    (4, _("Sedatives"))
     )

PAYMENT_OPTIONS = (
    (1, _("NHIF")),
    (2, _("INSURANCE COMPANY")),
    (3, _("PATIENT")),
    (4, _("PATIENT and NHIF")),
     )