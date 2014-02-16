from django.shortcuts import render
from django.template import RequestContext
from models import MatchUp, UserProfile

def matchUpRequest(request):
    context = RequestContext(request)

    active = None

    try:
        print MatchUp.objects.get(match_maker=request.user.pk, in_progress=True)
        active = MatchUp.objects.get(match_maker=request.user,in_progress=True)
    except MatchUp.DoesNotExist:
        pass

    try:
        if request.method == 'POST':
            if not active:
                post = request.POST
                his_phone = post['hisphone']
                her_phone = post['herphone']
                lat = post['lat']
                long = post['long']

                him = None
                her = None
                try:
                    him = UserProfile.objects.get(phone=his_phone)
                except:
                    pass
                try:
                    her = UserProfile.objects.get(phone=her_phone)
                except:
                    pass

                matchup = MatchUp(match_maker=request.user, him=him, her=her, his_phone=his_phone, her_phone=her_phone)
                matchup.save()

    except:
        context['error'] = "Please check the form and try again."


    context['active'] = active
    return render(request, 'matchup.html', context)