from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from defaults.models import ScoreTypes,BoolStates



#Add more fields such as likes/dislikes, view_count
#And perhaps a complaint shouldn't be deleted even if customer/company are to be deleted. Either or both
class ComplaintPost(models.Model):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='author_related_name')
    company = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='company_related_name')

    title = models.CharField(max_length=60)
    body = models.TextField()
    score_type = models.PositiveSmallIntegerField(choices=ScoreTypes.choices,default=ScoreTypes.OK,max_length=1)

    is_active = models.PositiveSmallIntegerField(choices=BoolStates.choices,default=BoolStates.YES,max_length=1)
    is_solved = models.PositiveSmallIntegerField(choices=BoolStates.choices,default=BoolStates.NO,max_length=1)

    date_created = models.DateTimeField(default=timezone.now)


#And perhaps a comment shouldn't be deleted even if customer/company are to be deleted. Either or both
class ComplaintComment(models.Model):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    complaint_post = models.ForeignKey(ComplaintPost,on_delete=models.CASCADE)

    body = models.TextField()

    date_created = models.DateTimeField(default=timezone.now)
