from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

import accounts.models as accountsmodels
import complaints.models as complaintsmodels
import home.models as homemodels
import defaults.models as defaultsmodels


#ENV_VARIABLES
object_types_user = defaultsmodels.ObjectTypes.USER
object_types_complaint = defaultsmodels.ObjectTypes.COMPLAINT
object_types_dict = {'user':object_types_user,'complaint':object_types_complaint}
bool_states_yes = defaultsmodels.BoolStates.YES
bool_states_no = defaultsmodels.BoolStates.NO
bool_states_dict = {'yes':bool_states_yes,'no':bool_states_no}

score_types_choices = defaultsmodels.ScoreTypes.choices


def home_view(request):
    
    context = {}

    request_user = request.user

    is_authenticated = bool_states_no

    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            is_authenticated = bool_states_yes
            request_user_id = request_user.pk

        #user is not authenticated
        else:
            request_user_id = bool_states_no

        print("==========================================================")

        for score_type_tuple in score_types_choices:
            print(f"Value: {score_type_tuple[0]}")
            print(f"Human readable: {score_type_tuple[1]}")

        print("==========================================================")



        #GET_DATA

        defaults_dict = {'bool_states_dict':bool_states_dict}

        user_dict = {'id':request_user_id,'is_authenticated':is_authenticated}


        context['GET_data']={
            'user_dict':user_dict,
            'defaults_dict':defaults_dict
        }


        return render(request,'home/home.html',context)

    else:
        return HttpResponse("INVALID REQUEST!")



def searching_view(request, *args, **kwargs):
    if request.method == 'GET':

        context = {}
        filter_results = []
        sorted_filter_results = []

        is_result = bool_states_no

        parameter_search_string = request.GET.get("parameter_search_string")

        #if user passed some arguments
        if parameter_search_string:

            company_results = accountsmodels.CompanyProfile.objects.filter(name__icontains=parameter_search_string)
            complaint_results = complaintsmodels.ComplaintPost.objects.filter(title__icontains=parameter_search_string)

            #check if there's company or complaint results
            if company_results or complaint_results:

                is_result = bool_states_yes

                #if there's company results
                if company_results:

                    for company in company_results:

                        #company info

                        company_object = company.user
                        company_id = company_object.id
                        company_name = company.name

                        filter_results.append({'id':company_id,'name':company_name,'object_type':object_types_user})

                #no company results
                else:
                    pass

                #if there's complaint results
                if complaint_results:

                    for complaint in complaint_results:

                        #complaint info

                        complaint_id = complaint.pk
                        complaint_title = complaint.title

                        filter_results.append({'id':complaint_id,'name':complaint_title,'object_type':object_types_complaint})

                #No complaint results
                else:
                    pass

                sorted_filter_results = sorted(filter_results, key=lambda x: x.name, reverse=False)

            #No results
            else:
                pass

        #No arguments
        else:
            pass


        #GET Data

        search_result_dicts = {'is_result':is_result,'dicts':sorted_filter_results}

        defaults_dict = {'object_types_dict':object_types_dict,'bool_states_dict':bool_states_dict}


        context['GET_data']={

            'search_result_dicts':search_result_dicts,
            'defaults_dict':defaults_dict
        }

        return render(request,'home/searching.html',context)

    else:
        return HttpResponse("INVALID REQUEST!")


