from django.db import models

class RetainingWall(models.Model):
    height = models.FloatField()
    top_breadth = models.FloatField()
    base_breadth = models.FloatField()
    Ka = models.FloatField()
    gamma_soil = models.FloatField()
    gamma_stone = models.FloatField()
    surcharge = models.FloatField()
    water_table = models.FloatField()
    passive_soil_height = models.FloatField()
    Kp = models.FloatField()

    def __str__(self):
        return f"Retaining Wall - Height: {self.height} m, Base Breadth: {self.base_breadth} m, Top Breadth: {self.top_breadth} m"
