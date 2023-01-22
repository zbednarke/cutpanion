import numpy as np
from plotly import graph_objects as go
from django.contrib import messages
from plotly.io import to_html
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

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
    username = request.user.username
    context = {
        'img_url': get_storage_url(f'img/{username}_background.jpg'),
        'whycuts': WhyCut.objects.filter(owner=request.user).all()
    }
    return render(request,'mypage/mypage.html', context)

@login_required
def trajectoryView(request):
    """Plot exoected trajectory of fatloss"""

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
            line=dict(color='rgba(0,0,0,1)'),
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


