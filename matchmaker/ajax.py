from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from matchmaker.models import MatchUp

import json

@login_required
@require_POST
def toggle_confirm_date(request):
    response = {}

    try:
        matchupid = request.POST["matchup"]
        matchup = MatchUp.objects.get(id=matchupid)
        confirmed = True

        if matchup.him == request.user:
            confirmed = not matchup.him_confirmed
            matchup.him_confirmed = confirmed

        elif matchup.her == request.user:
            confirmed = not matchup.her_confirmed
            matchup.her_confirmed = confirmed

        else:
            raise Exception("Non matchup owner")

        matchup.save()

        response['confirmed'] = confirmed

    except Exception, err:
        response['error'] = err.__str__()

    return HttpResponse(json.dumps(response), content_type="application/json")