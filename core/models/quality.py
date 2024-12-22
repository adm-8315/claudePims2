from django.db import models

class QCTest(models.Model):
    slot = models.IntegerField(default=0)
    start_time = models.DateTimeField(db_column='startTime')
    stop_time = models.DateTimeField(null=True, db_column='stopTime')
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    water = models.FloatField()
    mix = models.IntegerField()
    vib = models.IntegerField()
    lotcode = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'QC Test {self.id} - {self.material}'

class QCTestData(models.Model):
    qc_test = models.ForeignKey(QCTest, on_delete=models.CASCADE, db_column='qcTest')
    timestamp = models.DateTimeField()
    temperature = models.FloatField()

    class Meta:
        unique_together = ['qc_test', 'timestamp']