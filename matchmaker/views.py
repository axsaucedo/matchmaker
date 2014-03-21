from django.shortcuts import render
from django.template import RequestContext
from models import MatchUp, UserProfile, User
from twilio.rest import TwilioRestClient
import random


# Twilio Settings
account = "AC8f68f68ffac59fd5afc1a3317b1ffdf8"
token = "5a556d4a9acf96753850c39111646ca4"
client = TwilioRestClient(account, token)
fromnumber = "+447903518974"

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

                him_pass = random.randrange(9999)
                her_pass = random.randrange(9999)
                try:
                    him = UserProfile.objects.get(phone=his_phone)
                except:
                    u_him = User.objects.create(username=his_phone.replace('+',''), password=him_pass)
                    him = UserProfile.objects.create(user=u_him, phone=his_phone)
                try:
                    her = UserProfile.objects.get(phone=her_phone)
                except:
                    u_her = User.objects.create(username=her_phone.replace('+',''), password=her_pass)
                    her = UserProfile.objects.create(user=u_her, phone=her_phone)

                matchup = MatchUp(match_maker=request.user, him=him.user, her=her.user, his_phone=his_phone, her_phone=her_phone)
                matchup.save()

                print him
                print her

                message = "Your friend " + request.user.first_name + " " + request.user.last_name + " has set you up on a blind date! Please access http://localhost:8000/matchups/" + str(matchup.id) + " to check it!"

#                his_sms = client.sms.messages.create(body=message,
#                                                    to=her_phone,
#                                                    from_=fromnumber)
#
#                her_sms = client.sms.messages.create(body=message,
#                                                    to=his_phone,
#                                                    from_=fromnumber)

                print "Emails sent"

                active = matchup


    except:
        context['error'] = "Please check the form and try again."


    context['active'] = active
    return render(request, 'matchup/matchup.html', context)

def viewMatchUpRequest(request, matchid):
    context = RequestContext(request)

    match = None

    try:
        match = MatchUp.objects.get(id=matchid)
    except:
        return render(request, 'matchup/404.html', context)

    context['match'] = match

    return render(request, 'matchup/matchups.html', context)

def viewProfile(request, username):
    context = RequestContext(request)

    user = None

    try:
        user = User.objects.get(username=username)
    except:
        pass

    context['user'] = user
    return render(request, 'accounts/profile.html', context)