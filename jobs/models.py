from django.db import models

class Job(models.Model):
    date = models.DateField()
    party_name = models.CharField(max_length=255)
    job_size = models.CharField(max_length=100)
    paper = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    job_details = models.TextField()
    ctp = models.CharField(max_length=100, blank=True, null=True)
    paper_by = models.CharField(max_length=100, blank=True, null=True)
    narration = models.TextField(blank=True, null=True)
    lami_size = models.CharField(max_length=100, blank=True, null=True)
    enve_size = models.CharField(max_length=100, blank=True, null=True)
    ctp_no = models.PositiveIntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paper_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lami_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    enve_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    recieved = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bal_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.date} - {self.party_name} - {self.job_details}"
