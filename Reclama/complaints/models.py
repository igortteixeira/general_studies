from django.db import models
from django.utils import timezone

import accounts.models as accountsmodels
import defaults.models as defaultsmodels
import complaints.models as complaintsmodels



#Add more fields such as likes/dislikes, view_count
#And perhaps a complaint shouldn't be deleted even if customer/company are to be deleted. Either or both
class Complaint(models.Model):
    author = models.ForeignKey(accountsmodels.CustomUser,on_delete=models.CASCADE,related_name='author_related_name')
    company = models.ForeignKey(accountsmodels.CustomUser,on_delete=models.CASCADE,related_name='company_related_name')

    title = models.CharField(max_length=60)
    body = models.TextField()
    score_type = models.PositiveSmallIntegerField(choices=defaultsmodels.ScoreTypes.choices,default=defaultsmodels.ScoreTypes.OK)

    is_active = models.BooleanField(default=True)
    is_solved = models.BooleanField(default=False)

    date_created = models.DateTimeField(default=timezone.now)


#And perhaps a comment shouldn't be deleted even if customer/company are to be deleted. Either or both
class ComplaintComment(models.Model):
    author = models.ForeignKey(accountsmodels.CustomUser,on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint,on_delete=models.CASCADE)

    body = models.TextField()

    date_created = models.DateTimeField(default=timezone.now)
