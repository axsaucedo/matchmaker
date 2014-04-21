from django.shortcuts import render
from django.template import RequestContext
from models import MatchUp, UserProfile, User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from twilio.rest import TwilioRestClient
import random
from datetime import datetime
from matchmaker.settings import BASE_URL

from pytz import timezone
import pytz


# Twilio Settings
account = "AC8f68f68ffac59fd5afc1a3317b1ffdf8"
token = "5a556d4a9acf96753850c39111646ca4"
client = TwilioRestClient(account, token)
fromnumber = "+447903518974"

def matchUpRequest(request):
    context = RequestContext(request)

    try:
        if request.method == 'POST':
            post = request.POST
            his_phone = post['hisphone']
            her_phone = post['herphone']
            lat = post['lat']
            long = post['long']
            address = post['address']

            print post['date-date']
            print datetime.strptime(post['date-date'], '%d/%m/%Y %H:%M:%S')

            date_date = datetime.strptime(post['date-date'], '%d/%m/%Y %H:%M:%S')
            date_date = timezone('UTC').localize(date_date)

            print date_date

            him_pass = random.randrange(9999)
            her_pass = random.randrange(9999)
            try:
                him = UserProfile.objects.get(phone=his_phone)
            except:
                print his_phone.replace('+','')
                print str(him_pass)
                u_him = User.objects.create_user(username=his_phone.replace('+',''), password=str(him_pass))
                u_him.save()
                him = UserProfile.objects.create(user=u_him, phone=his_phone)
            try:
                her = UserProfile.objects.get(phone=her_phone)
            except:
                print her_phone.replace('+','')
                print str(her_pass)
                u_her = User.objects.create_user(username=her_phone.replace('+',''), password=str(her_pass))
                u_her.save()
                her = UserProfile.objects.create(user=u_her, phone=her_phone)

            print him
            print her

            matchup = MatchUp(    match_maker=request.user
                                , him=him.user
                                , her=her.user
                                , his_phone=his_phone
                                , her_phone=her_phone
                                , latitude=lat
                                , longitude=long
                                , address=address
                                , date_date=date_date)

            matchup.save()

            message_him = "Your friend " + request.user.first_name + " " + request.user.last_name + " has set you up on a blind date! Please access "+BASE_URL+"matchups/" + str(matchup.id) + "/?uname="+his_phone.replace('+','')+"&pass="+str(him_pass)+" to check it!"
            message_her = "Your friend " + request.user.first_name + " " + request.user.last_name + " has set you up on a blind date! Please access "+BASE_URL+"matchups/" + str(matchup.id) + "/?uname="+her_phone.replace('+','')+"&pass="+str(her_pass)+" to check it!"

            print message_him
            print message_her

            try:
                his_sms = client.sms.messages.create(body=message_him,
                                                    to=his_phone,
                                                    from_=fromnumber)

                her_sms = client.sms.messages.create(body=message_her,
                                                    to=her_phone,
                                                    from_=fromnumber)
            except Exception as e:
                print str(e)

            return redirect('/matchups/' + str(matchup.pk) + '/')


    except:
        context['error'] = "Please check the form and try again."

    return render(request, 'matchup/matchup.html', context)

def saveNumber(request):
    context = RequestContext(request)
    return render(request, 'matchup/phone_input.html', context)

def viewMatchUpRequest(request, matchid):
    context = RequestContext(request)

    match = None

    try:
        match = MatchUp.objects.get(id=matchid)
    except:
        return render(request, 'matchup/404.html', context)

    get = request.GET
    username = get.get('uname')
    password = get.get('pass')

    if request.method == 'GET' and username and password:

        print username, password
        user = authenticate(username=username, password=password)
        print user

        if user == None: return redirect('/signup/')

        login(request, user)

        you = match.him
        you_confirmed = match.him_confirmed
        partner = match.her
        partner_confirmed = match.her_confirmed

        if not user == you:
            partner = match.him
            partner_confirmed = match.him_confirmed
            you = match.her
            you_confirmed = match.her_confirmed

        context['you'] = you
        context['you_confirmed'] = you_confirmed
        context['partner'] = partner
        context['partner_confirmed'] = partner_confirmed

    context['match'] = match
    context['matcher'] = match.match_maker == request.user

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