from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.core.exceptions import ValidationError

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


# Describes an organization where images were produced
class Institution(models.Model):
    title = models.TextField(max_length=255)


# Describes a disease which appears on X-ray images
class Disease(models.Model):
    title = models.TextField(max_length=255)


# Describes medical report given by a doctor
class Diagnosis(models.Model):
    dateOfConclusion = models.DateField()
    doctorsName = models.TextField(max_length=255)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(max_length=2047)


# Describes a model which can be used so as to obtain contours
class TrainableModel(models.Model):
    structureFile = models.FileField(upload_to="data/trainable_models/structures/",
                                     default="data/trainable_models/structures/default.yaml")
    weightsFile = models.FileField(upload_to="data/trainable_models/weights",
                                   default="data/trainable_models/weights/default.h5")
    creationDate = models.DateField()
    description = models.TextField(max_length=2047)


# Describes a medical image
class DicomImage(models.Model):
    owner = models.ForeignKey('auth.User', related_name='dicom_images', default=2)
    file = models.FileField(upload_to="data/dicom_images/", default="data/dicom_images/default.dcm")
    acquisition_date = models.DateField()
    source = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)


# Describes a contour of some structure (organ or pathology)
class Contour(models.Model):
    contourFile = models.FileField(upload_to="data/contour_files/", default="/data/contour_files/default.npz")
    maskFile = models.FileField(upload_to="data/mask_files/", default="/data/mask_files/default.npz")
    byHandObtained = models.BooleanField()
    producedBy = models.ForeignKey(TrainableModel, on_delete=models.SET_NULL, null=True)

    def clean(self):
        # A contour can be produced either by hand or by model, but not both
        if self.byHandObtained and self.producedBy is not None:
            raise ValidationError("Contour %d relates to model %d while it is by hand obtained.")


class OrganContour(Contour):
    organ = models.TextField(max_length=255)


class PathologyContour(Contour):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True)
