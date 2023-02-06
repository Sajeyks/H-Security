from django.utils.translation import gettext as _

PRESCRIPTION_TYPE = (
    ("Acute (not to be repeated)", _("Acute (not to be repeated)")),
    ("Repeat (long term medication)", _("Repeat (long term medication)")),
    ("Repeat Dispensing (specific amount of ussues)", _("Repeat Dispensing (specific amount of ussues)")),
     )

MEDICINE_TYPE = (
    ("Pain relievers", _("Pain relievers")),
    ("Tranquilizers", _("Tranquilizers")),
    ("Stimulants", _("Stimulants")),
    ("Sedatives", _("Sedatives"))
     )

PAYMENT_OPTIONS = (
    ("NHIF", _("NHIF")),
    ("INSURANCE COMPANY", _("INSURANCE COMPANY")),
    ("PATIENT", _("PATIENT")),
    ("PATIENT and NHIF", _("PATIENT and NHIF")),
     )