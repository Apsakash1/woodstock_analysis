import math
import time
import requests
from fpdf import FPDF
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
import datetime

author_name = 'Akash Pratap Singh'
author_id = '2018A8PS0462P'


def draw_commits(commits, name):
    print('Creating ' + name.upper() + ' commits chart...')
    n = len(commits)
    x = list(range(1, n))
    x.append(n)
    y = []
    for commit in commits:
        y.append(commit['total'])

    index = np.arange(n)
    fig, ax = plt.subplots(1, 1, figsize=(16, 7), dpi=96)
    plt.plot(x, y, label='Commits', color='black', linewidth=2.0)
    b1 = plt.bar(index + 1, y, label='Commits', color=[(0.06667, 0.5647, 0.7961)], width=0.150)

    plt.xticks(fontsize=14, rotation=45, horizontalalignment='center', color='darkgrey')
    plt.yticks(fontsize=14, color='darkgrey')
    plt.xlim(-1.0)
    ax.yaxis.grid(alpha=0.5)
    # plt.yscale('log', basey=1.00001)

    plt.gca().spines["top"].set_alpha(0)
    plt.gca().spines["bottom"].set_alpha(0.5)
    plt.gca().spines["right"].set_alpha(0)
    plt.gca().spines["left"].set_alpha(0)
    print('Saving plot ...')
    plt.savefig(name + '_commits_fig.png', orientation='portrait', transparent=True, bbox_inches=None, pad_inches=0)


def draw_comparison_commits(commits, name, commits_other, name_other):
    print(name.upper() + ' versus ' + name_other.upper() + ' commits chart...')
    n = len(commits)
    x = list(range(1, n))
    x.append(n)
    y = []
    for commit in commits:
        y.append(commit['total'])

    n_other = len(commits_other)
    x_other = list(range(1, n_other))
    x_other.append(n_other)
    y_other = []
    for commit in commits_other:
        y_other.append(commit['total'])

    index = np.arange(n)
    fig, ax = plt.subplots(1, 1, figsize=(16, 7), dpi=96)
    print('Plotting Lines...')
    plt.plot(x, y, label='Commits', color='black', linewidth=4.0)
    plt.plot(x, y_other, label='Commits_other', color='r', linewidth=4.0)
    print('Plotting Bar Graphs...')
    b1 = plt.bar(index - 0.15 + 1, y, label='Commits' + name, color=[(0.06667, 0.5647, 0.7961)], width=0.3)
    b2 = plt.bar(index + 0.15 + 1, y_other, label='Commits ' + name_other, color=[(1, 0.4118, 0.4118)], width=0.3)

    print('Aligning labels & rotating X-labels ...')
    plt.xticks(fontsize=14, rotation=45, horizontalalignment='center', color='darkgrey')
    plt.yticks(fontsize=14, color='darkgrey')
    plt.xlim(-1.0)
    ax.yaxis.grid(alpha=0.5)
    # plt.yscale('log', basey=1.00001)

    plt.gca().spines["top"].set_alpha(0)
    plt.gca().spines["bottom"].set_alpha(0.5)
    plt.gca().spines["right"].set_alpha(0)
    plt.gca().spines["left"].set_alpha(0)
    print('Saving comparison analysis plot ...')
    plt.savefig(name + '_' + name_other + '_commits_fig.png', orientation='portrait', transparent=True,
                bbox_inches=None, pad_inches=0)


def plot_comparison(name, name_other, commits_data1, commits_data2):
    print('Starting Comparison ...')
    draw_comparison_commits(commits_data1, name, commits_data2, name_other)
    pdf.add_page()
    pdf.set_top_margin(20)
    pdf.set_xy(0, 20)
    pdf.set_font('arial', 'B', 20)
    pdf.cell(0, 30, '' + name.upper() + ' vs ' + name_other.upper(), 0, 2, 'C')
    print('Embedding comparison chart chart into pdf...')
    pdf.image(name + '_' + name_other + '_commits_fig.png', x=0, y=60, w=210, h=100)

    # Perform Analysis
    total_weekly_commits1 = []
    total_weekly_commits2 = []
    max_weekly_commits1 = 0
    max_weekly_commits2 = 0
    weekdays_commits1 = 0
    weekdays_commits2 = 0
    weekend_commits1 = 0
    weekend_commits2 = 0
    latest_three_week_commits1 = 0
    latest_three_week_commits2 = 0
    oldest_three_week_commits1 = 0
    oldest_three_week_commits2 = 0
    total_weeks1 = len(commits_data1)
    total_weeks2 = len(commits_data2)
    for index, week in enumerate(commits_data1):
        if week['total'] > max_weekly_commits1:
            max_weekly_commits1 = week['total']
        total_weekly_commits1.append(week['total'])
        weekdays_commits1 += week['days'][0] + week['days'][1] + week['days'][2] + week['days'][3] + week['days'][4]
        weekend_commits1 += week['days'][5] + week['days'][6]
        if index < 3:
            oldest_three_week_commits1 += week['total']
        elif total_weeks - index <= 3:
            latest_three_week_commits1 += week['total']

    for index, week in enumerate(commits_data2):
        if week['total'] > max_weekly_commits2:
            max_weekly_commits2 = week['total']
        total_weekly_commits2.append(week['total'])
        weekdays_commits2 += week['days'][0] + week['days'][1] + week['days'][2] + week['days'][3] + week['days'][4]
        weekend_commits2 += week['days'][5] + week['days'][6]
        if index < 3:
            oldest_three_week_commits2 += week['total']
        elif total_weeks - index <= 3:
            latest_three_week_commits2 += week['total']

    # Prepare Analysis
    more_less = 'more' if (max_weekly_commits1 > max_weekly_commits2) else 'less'
    max_weekly_commits_anal1 = name + ' has ' + str(max_weekly_commits1) + ' maximum weekly commits throughout the year'
    max_weekly_commits_anal2 = 'while ' + name_other + ' has ' + str(max_weekly_commits2) + ' maximum weekly commits throughout the year.'
    max_weekly_commits_anal3 = 'This indicates ' + name + ' has a ' + more_less + ' active developer community.'


    more_less = 'more ' if (sum(total_weekly_commits1) > sum(total_weekly_commits2)) else ' less '
    yearly_total_commits_anal1 = name + ' has ' + str(sum(total_weekly_commits1)) + ' total commits this year while '
    yearly_total_commits_anal2 = 'while' + name_other + ' has ' + str(sum(total_weekly_commits2)) + ' total commits for this year.'
    yearly_total_commits_anal3 = 'This indicates ' + name + ' has ' + more_less + ' support '
    yearly_total_commits_anal4 = 'from developer community than ' + name_other + '.'

    more_less = 'more ' if (oldest_three_week_commits1 > oldest_three_week_commits2) else ' less '
    active_a_year_ago1 = name + ' have ' + str(oldest_three_week_commits1) + ' total commits for a cumulative '
    active_a_year_ago2 = 'of three weeks a year ago while ' + name_other + ' has' + str(oldest_three_week_commits2) + 'commits during the same duration.'
    active_a_year_ago3 = 'This indicates ' + name + ' had ' + more_less + ' active '
    active_a_year_ago4 = ' developer community than ' + name_other + '.'

    more_less = 'more ' if (latest_three_week_commits1 > latest_three_week_commits2) else ' less '
    active_now1 = name + ' have ' + str(latest_three_week_commits1) + ' total commits for most recent three weeks while '
    active_now2 = name_other + ' has ' + str(latest_three_week_commits2) + 'commits during the same duration.'
    active_now3 = 'This indicates ' + name + ' has currently ' + more_less + ' active developer community than ' + name_other + '.'

    # Present Analysis
    pdf.set_font('arial', '', 12)
    pdf.set_left_margin(20)
    pdf.set_xy(20, 165)
    pdf.cell(0, 10, '\n\n', 0, 2)
    pdf.cell(0, 10, max_weekly_commits_anal1, 0, 2)
    pdf.cell(0, 10, max_weekly_commits_anal2, 0, 2)
    pdf.cell(0, 10, max_weekly_commits_anal3, 0, 2)
    pdf.cell(0, 10, '\n', 0, 2)
    pdf.cell(0, 10, yearly_total_commits_anal1, 0, 2)
    pdf.cell(0, 10, yearly_total_commits_anal2, 0, 2)
    pdf.cell(0, 10, yearly_total_commits_anal3, 0, 2)
    pdf.cell(0, 10, yearly_total_commits_anal4, 0, 2)
    pdf.cell(0, 10, '\n', 0, 2)
    pdf.cell(0, 10, active_a_year_ago1, 0, 2)
    pdf.cell(0, 10, active_a_year_ago2, 0, 2)
    pdf.cell(0, 10, active_a_year_ago3, 0, 2)
    pdf.cell(0, 10, active_a_year_ago4, 0, 2)
    pdf.cell(0, 10, '\n', 0, 2)
    pdf.cell(0, 10, active_now1, 0, 2)
    pdf.cell(0, 10, active_now2, 0, 2)
    pdf.cell(0, 10, active_now3, 0, 2)
    pdf.cell(0, 10, '\n', 0, 2)


# owners = ['bitcoin']
# repos = ['bitcoin']
owners = ['bitcoin', 'ethereum', 'trustwallet', 'solana-labs', 'ava-labs', 'groestlcoin']
repos = ['bitcoin', 'go-ethereum', 'wallet-core', 'solana', 'avalanchego', 'groestlcoin']
# commit_activity = 'https://api.github.com/repos/bitcoin/bitcoin/stats/commit_activity'
commit_activity = 'https://api.github.com/repos/{}/{}/stats/commit_activity'

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_author(author=author_name)
pdf.set_xy(0, 10)
pdf.set_font('arial', 'B', 50)
pdf.cell(60)
pdf.cell(75, 30, 'A Report on', 0, 2, 'C')
pdf.cell(75, 30, 'Developer Activity', 0, 2, 'C')
pdf.cell(75, 30, 'of Crypto Assets', 0, 2, 'C')
pdf.set_font('arial', 'B', 25)
pdf.cell(75, 15, author_name, 0, 2, 'C')
pdf.cell(75, 15, author_id, 0, 2, 'C')
pdf.image('woodstock.png', x=40, y=150, w=109, h=50)
now = datetime.datetime.now()
pdf.set_font('arial', 'B', 15)
pdf.text(x=20, y=270, txt='Report Generated: ' + now.strftime('%H:%M:%S on %A, %B the %dth, %Y'))

commits_data = []
idx = 0
for owner, repo in zip(owners, repos):
    print('\n-------------------------------' + owner.upper() + '-------------------------------\n')
    print('Fetching ' + owner.upper() + ' commits Data...')
    response = requests.get(commit_activity.format(owner, repo))
    data = response.json()
    commits_data.append(data)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 404:
        print('Not Found. Error occured in requesting data from github API')
        print(response)
        print('Please Ensure you have internet connected and then run this')
        break
    elif response.status_code == 403:
        print(response.status_code)
        print(response.json())
        print('You have exceed the maximum API calls limit allowed by github for your IP address, try again tommorow or use VPN')
    else:
        print(response.status_code)
        print(response.json())
        print('Unexpected API response with - ' + str(response))
        break

    # print(data)
    draw_commits(data, owner)
    pdf.add_page()
    pdf.set_top_margin(20)
    pdf.set_xy(0, 20)
    pdf.set_font('arial', 'B', 50)
    pdf.cell(0, 30, '' + owner.upper(), 0, 2, 'C')
    pdf.image(owner + '_commits_fig.png', x=0, y=60, w=210, h=100)

    print('Analyzing ' + owner.upper() + ' commits Data...')

    total_weekly_commits = []
    max_weekly_commits = 0
    max_weekly_commits_index = 0
    weekdays_commits = 0
    weekend_commits = 0
    latest_three_week_commits = 0
    oldest_three_week_commits = 0
    total_weeks = len(data)
    for index, week in enumerate(data):
        if week['total'] > max_weekly_commits:
            max_weekly_commits = week['total']
            max_weekly_commits_index = index
        total_weekly_commits.append(week['total'])
        weekdays_commits += week['days'][0] + week['days'][1] + week['days'][2] + week['days'][3] + week['days'][4]
        weekend_commits += week['days'][5] + week['days'][6]
        if index < 3:
            oldest_three_week_commits += week['total']
        elif total_weeks - index <= 3:
            latest_three_week_commits += week['total']

    print('Writing ' + owner + ' analysis to pdf...')
    # last_week_commits = data[total_weeks-1] if (data[total_weeks-1]>0) else data[total_weeks-2]
    interest_decline = 'increase' if latest_three_week_commits > oldest_three_week_commits else 'decline'
    max_weekly_commits_anal1 = 'Maximum commits in last one year recorded is ' + str(
        max_weekly_commits) + ' which was ' + str(total_weeks - max_weekly_commits_index) + ' weeks ago.' + '\n'
    max_weekly_commits_anal2 = 'Total commits this week recorded till now is ' + str(
        data[total_weeks - 1]['total']) + ' and commits recorded previous week'
    max_weekly_commits_anal3 = 'are ' + str(data[total_weeks - 2]['total']) + "."
    recent_activity_compared_to_year_ago1 = 'Average weekly commits activity one year ago for a 3 weeks cumulative interval '
    recent_activity_compared_to_year_ago2 = 'was approximately ' + str(
        math.ceil(oldest_three_week_commits / 3)) + ' for the most recent three weeks time interval.'
    recent_activity_compared_to_year_ago3 = 'Average compared from a year ago show a ' + interest_decline + 'in developers interest'
    recent_activity_compared_to_year_ago4 = 'over time in ' + owner + ' cryptocurrency.'

    full_time = 'more' if (weekdays_commits > weekend_commits) else 'less'
    people_anal1 = 'Contributor who have contributed in bitcoin in the weekdays are ' + full_time + ' compared to'
    people_anal2 = 'the people working on weekends. It can be treated as a potential indicator that'
    people_anal3 = 'the people who pursue ' + owner + ' as a full time activity are ' + full_time + ' compared to'
    people_anal4 = 'the ones working part time. working part time.'

    pdf.set_font('arial', '', 12)
    pdf.set_left_margin(20)
    pdf.set_xy(20, 165)
    pdf.cell(0, 10, '\n\n', 0, 2)
    pdf.cell(0, 10, max_weekly_commits_anal1, 0, 2)
    pdf.cell(0, 10, max_weekly_commits_anal2, 0, 2)
    pdf.cell(0, 10, max_weekly_commits_anal3, 0, 2)
    pdf.cell(0, 10, '\n', 0, 2)
    pdf.cell(0, 10, recent_activity_compared_to_year_ago1, 0, 2)
    pdf.cell(0, 10, recent_activity_compared_to_year_ago2, 0, 2)
    pdf.cell(0, 10, recent_activity_compared_to_year_ago3, 0, 2)
    pdf.cell(0, 10, recent_activity_compared_to_year_ago4, 0, 2)
    pdf.cell(0, 10, '\n', 0, 2)
    pdf.cell(0, 10, people_anal1, 0, 2)
    pdf.cell(0, 10, people_anal2, 0, 2)
    pdf.cell(0, 10, people_anal3, 0, 2)
    pdf.cell(0, 10, people_anal4, 0, 2)

    idx += 1
    if idx % 2 == 0:
        print('\n---------------------' + owners[idx - 2].upper() + '  Versus  ' + owners[idx - 1].upper() + '-------------------------\n')
        plot_comparison(owners[idx - 2], owners[idx - 1], commits_data[0], commits_data[1])
        commits_data.clear()

pdf.add_page()
pdf.set_xy(70, 150)
pdf.set_font('arial', 'B', 50)
pdf.set_text_color(0, 102, 51)
pdf.cell(75, 30, 'Thank You!', 0, 2, 'C')
pdf.output('report.pdf')
print('------------------------------- THE END -------------------------------')
# df = pd.DataFrame()
# df['Question'] = ["Q1", "Q2", "Q3", "Q4"]
# df['Charles'] = [3, 4, 5, 3]
# df['Mike'] = [3, 3, 4, 4]
#
# title("Professor Criss's Ratings by Users")
# xlabel('Question Number')
# ylabel('Score')
#
# c = [2.0, 4.0, 6.0, 8.0]
# m = [x - 0.5 for x in c]
#
# xticks(c, df['Question'])
#
# bar(m, df['Mike'], width=0.5, color="#91eb87", label="Mike")
# bar(c, df['Charles'], width=0.5, color="#eb879c", label="Charles")
#
# legend()
# axis([0, 10, 0, 8])
# savefig('barchart.png')
#
# pdf = FPDF()
# pdf.add_page()
# pdf.set_xy(0, 0)
# pdf.set_font('arial', 'B', 12)
# pdf.cell(60)
# pdf.cell(75, 10, "A Tabular and Graphical Report of Professor Criss's Ratings by Users Charles and Mike", 0, 2, 'C')
# pdf.cell(90, 10, " ", 0, 2, 'C')
# pdf.cell(-40)
# pdf.cell(50, 10, 'Question', 1, 0, 'C')
# pdf.cell(40, 10, 'Charles', 1, 0, 'C')
# pdf.cell(40, 10, 'Mike', 1, 2, 'C')
# pdf.cell(-90)
# pdf.set_font('arial', '', 12)
# for i in range(0, len(df)):
#     pdf.cell(50, 10, '%s' % (df['Question'].iloc[i]), 1, 0, 'C')
#     pdf.cell(40, 10, '%s' % (str(df.Mike.iloc[i])), 1, 0, 'C')
#     pdf.cell(40, 10, '%s' % (str(df.Charles.iloc[i])), 1, 2, 'C')
#     pdf.cell(-90)
# pdf.cell(90, 10, " ", 0, 2, 'C')
# pdf.cell(-30)
# pdf.image('barchart.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
# pdf.output('test.pdf', 'F')
#
