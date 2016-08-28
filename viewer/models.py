from django.db import models
from django.core.exceptions import ValidationError


class Institution(models.Model):
    name = models.TextField(max_length=255)


class Disease(models.Model):
    title = models.TextField(max_length=255)


class Diagnosis(models.Model):
    dateOfConclusion = models.DateField()
    doctorsName = models.TextField(max_length=255)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL)
    comment = models.TextField(max_length=2047)


class Organ(models.Model):
    title = models.TextField(max_length=255)


class DicomImage(models.Model):
    filename = models.TextField(max_length=255)
    acquisition_date = models.DateField()
    source = models.ForeignKey(Institution, on_delete=models.SET_NULL)


class Contour(models.Model):
    filename = models.TextField(max_length=255)
    maskFilename = models.TextField(max_length=255)
    byHandObtained = models.BooleanField()
    producedBy = models.ForeignKey(TrainableModel, on_delete=models.SET_NULL)

    def clean(self):
        # A contour can be produced either by hand or by model, but not both
        if self.byHandObtained and self.producedBy is not None:
            raise ValidationError("Contour %d relates to model %d while it is by hand obtained.")


class OrganContour(Contour):
    organ = models.ForeignKey(Organ, on_delete=models.SET_NULL)


class PathologyContour(Contour):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL)


class TrainableModel(models.Model):
    structureFilename = models.TextField(max_length=255)
    weightsFilename = models.TextField(max_length=255)
    creationDate = models.DateField()
    description = models.TextField(max_length=2047)
