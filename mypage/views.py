import numpy as np
from plotly import graph_objects as go
from django.contrib import messages
from plotly.io import to_html
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import random
import datetime

from cutpanion.util import get_storage_url
from mypage.fatlossjourney import FatlossJourney
from mypage.forms import FatLossJourneyParamsAddForm, WeightBFForm
from mypage.models import FatLossJourneyParams, WeightBF, WhyCut


@login_required
def newfatlossjourneyform(request):  

    if request.method == 'POST':
        FatLossJourneyParams.objects.filter(owner=request.user).delete()
        form = FatLossJourneyParamsAddForm(request.POST)
        if form.is_valid:
            flj = form.save(commit=False)
            flj.owner = request.user
            flj.username = request.user.username
            flj.save()

            messages.success(
                request, "Fat Loss Journey added successfully.", extra_tags='alert alert-success alert-dismissible fade show')

            return redirect('mypage:home')
    else:
        form = FatLossJourneyParamsAddForm()
    context = {
        'form': form,
    }
    return render(request, 'mypage/fatloss_journey_add_form.html', context)

@login_required
def addWeightBF(request):
    """Add bodyfat/weight data to your records"""
    reasons = WhyCut.objects.filter(owner=request.user).all()
    messages.success(request, f"Why cut?\n{random.choice(reasons).reason}", extra_tags='alert alert-success alert-dismissible fade show')

    if request.method == 'POST':
        form = WeightBFForm(request.POST)
        if form.is_valid:
            flj = form.save(commit=False)
            flj.owner = request.user
            flj.username = request.user.username
            flj.save()

            messages.success(
                request, "Weight/BF added successfully", extra_tags='alert alert-success alert-dismissible fade show')

            return redirect('mypage:addWeightBF')
    else:
        form = WeightBFForm()
    context = {
        'form': form,
    }
    return render(request, 'mypage/weight_bf_form.html', context)


@login_required
def mypageview(request):
    reasons = WhyCut.objects.filter(owner=request.user).all()
    messages.success(request, f"Why cut?\n{random.choice(reasons).reason}", extra_tags='alert alert-success alert-dismissible fade show')
    username = request.user.username
    context = {
        'img_url': get_storage_url(f'img/{username}_background.jpg'),
        'whycuts': WhyCut.objects.filter(owner=request.user).all(),
        'username': username
    }
    return render(request,'mypage/mypage.html', context)

@login_required
def trajectoryView(request):
    """Plot exoected trajectory of fatloss"""
    reasons = WhyCut.objects.filter(owner=request.user).all()
    messages.success(request, f"Why cut?\n{random.choice(reasons).reason}", extra_tags='alert alert-success alert-dismissible fade show')

    np.random.seed(42)
    
    random_x= np.random.randint(1,101,100)
    random_y= np.random.randint(1,101,100)
    
    fig = go.Figure(data=[go.Scatter(
        x = random_x,
        y = random_y,
        mode = 'markers',)
    ])
                    
    plot_div = to_html(fig, include_plotlyjs="cdn", full_html=False)
    context = {"plot_div": plot_div}
    return render(request,'mypage/trajectory.html', context)


@login_required
def FatlossjourneyView(request):
    """
    day0parms: dict
    dict with keys:
        c: caloric deficit per day
        df: journey length in days
        w0: initial dry weight
        b0: inital bodyfat ratio
        db0: uncertainty in b0
        dw: deficit days per week
        dc_cons_opt: len 2 array
            actual cal deficit per day - nominal value. conservative and optimistic values.
    """

    reasons = WhyCut.objects.filter(owner=request.user).all()
    messages.success(request, f"Why cut?\n{random.choice(reasons).reason}", extra_tags='alert alert-success alert-dismissible fade show')
    
    username = request.user.username
    flj_params = FatLossJourneyParams.get_most_recent(username)
    if flj_params is None:
        return redirect('mypage:addFatLossJourneyForm')

    params = {
        'initial_cut_date': flj_params.initial_cut_date,
        'c': flj_params.cal_deficit_per_day,
        'df': flj_params.days_journey_length,
        'w0': flj_params.weight_initial_dry,
        'b0': flj_params.bf_initial,
        'db0': flj_params.delta_bf_initial,
        'dw': flj_params.deficit_days_per_week,
        'dc_cons_opt': [flj_params.daily_deficit_uncertainty, -flj_params.daily_deficit_uncertainty],
    }
    weightBFs = WeightBF.objects.filter(owner=request.user).all().order_by('date')

    flj= FatlossJourney(params)
    flj_fig_bf = flj.plot_projection_lines(show=False)
    flj_fig_bf = flj.plot_projection_cdev_bands(flj_fig_bf, show=False)

    flj_fig_bodyweight = flj.plot_projection_lines(fig=None, variable="bodyweight", show=False)
    flj_fig_bodyweight = flj.plot_projection_cdev_bands(fig=flj_fig_bodyweight, variable="bodyweight", show=False)

    weightBF_data = {'dates': [], 'weights': [], 'bfs': []}
    for wbf in weightBFs:
        weightBF_data['dates'].append(wbf.date)
        weightBF_data['weights'].append(wbf.weight)
        weightBF_data['bfs'].append(wbf.bf_percent)


    # this should be util func 
    weekly_lows_weights = []
    weekly_dates = []
    first_date = min(weightBF_data['dates']).date()
    last_date = max(weightBF_data['dates']).date()
    delta = last_date - first_date  
    all_dates_in_range = [first_date + datetime.timedelta(days=i) for i in range(delta.days + 1)] 
    n_weeks = int(np.ceil(len(all_dates_in_range)))

    for n in range(n_weeks):
        this_week_weights = []
        week_dates = all_dates_in_range[n * 7: (n + 1) * 7]
        week_date_day: datetime.date
        for wbf in weightBFs:
            if wbf.date.date() in week_dates:
                this_week_weights.append(wbf.weight)
                week_date_day = wbf.date.date()

        if this_week_weights:
            weekly_lows_weights.append(np.min(this_week_weights))
            weekly_dates.append(week_date_day)

    flj_fig_bf = flj_fig_bf.add_trace(
        go.Scatter(
            x=weightBF_data['dates'],
            y=weightBF_data['bfs'],
            name="Bodyfat Actual",
            mode='lines',
            line=dict(color='rgba(0,0,0,1)'),
        ),
        secondary_y=False,
    )

    flj_fig_bodyweight = flj_fig_bodyweight.add_trace(
        go.Scatter(
            x=weightBF_data['dates'],
            y=weightBF_data['weights'],
            name="Weight Actual",
            mode='lines',
            line=dict(color='rgba(0,0,0,.5)', width=3, dash='dash'),
        ),
        secondary_y=False,
    )

    flj_fig_bodyweight = flj_fig_bodyweight.add_trace(
        go.Scatter(
            x=weekly_dates,
            y=weekly_lows_weights,
            name="Weekly Lows",
            mode='lines',
            line=dict(color='rgba(0,0,0,1)', width=4),
        ),
        secondary_y=False,
    )




    plot_div_bf = to_html(flj_fig_bf, include_plotlyjs="cdn", full_html=False)
    plot_div_bodyweight = to_html(flj_fig_bodyweight, include_plotlyjs="cdn", full_html=False)

    context = {
        "plot_div_bf": plot_div_bf, 
        "plot_div_bodyweight": plot_div_bodyweight,
        "username": username,
    }
    return render(request,'mypage/trajectory.html', context)


