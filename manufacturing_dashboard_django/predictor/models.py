from django.db import models

class QualityPredictionLog(models.Model):
    temperature_c = models.FloatField()
    pressure_psi = models.FloatField()
    speed_rpm = models.FloatField()
    viscosity_pas = models.FloatField()
    hours_since_maintenance = models.FloatField()
    cycle_time_s = models.FloatField()
    predicted_quality = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class ImagePredictionLog(models.Model):
    image = models.ImageField(upload_to='plastic_images/')
    identified_plastic = models.CharField(max_length=50)
    confidence_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.identified_plastic} ({self.confidence_score:.2%}) at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"