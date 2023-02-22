from django.utils.translation import gettext as _

PAYMENT_OPTIONS = (
    ("NHIF", _("NHIF")),
    ("INSURANCE COMPANY", _("INSURANCE COMPANY")),
    ("PATIENT", _("PATIENT")),
    ("PATIENT and NHIF", _("PATIENT and NHIF")),
     )