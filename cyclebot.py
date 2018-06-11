#!/usr/bin/env python
from datetime import datetime
import dateparser

from flask import abort, Flask, jsonify, request


app = Flask(__name__)

CYCLES = [
    {
        'name': 'Grizzly',
        'start': 'May 01 2017',
        'end': 'June 09 2017'
    },
    {
        'name': 'Kodiak',
        'start': 'June 26 2017',
        'end': 'August 04 2017'
    },
    {
        'name': 'Panda',
        'start': 'August 21 2017',
        'end': 'September 29 2017'
    },
    {
        'name': 'Polar',
        'start': 'October 16 2017',
        'end': 'November 26 2017'
    },
    {
        'name': 'Spirit',
        'start': 'December 11 2017',
        'end': 'January 19 2018'
    },
    {
        'name': 'Baloo',
        'start': 'February 05 2018',
        'end': 'March 23 2018'
    },
    {
        'name': 'Fozzie',
        'start': 'April 09 2018',
        'end': 'May 18 2018'
    },
    {
        'name': 'Gummi',
        'start': 'June 04 2018',
        'end': 'July 13 2018'
    },
    {
        'name': 'Smokey',
        'start': 'July 30 2018',
        'end': 'Semptember 07 2018'
    },
    {
        'name': 'Teddy',
        'start': 'September 24 2018',
        'end': 'November 02 2018'
    },
    {
        'name': 'Yogi',
        'start': 'November 19 2018',
        'end': 'December 28 2018'
    }
]

# stole this from https://stackoverflow.com/a/11944910/356201
def week_difference(start, end):
    assert start <= end
    start_year, start_week, start_dayofweek = start.isocalendar()
    end_year, end_week, end_dayofweek = end.isocalendar()

    return ((end_year - start_year) * 52) - start_week + end_week + 1

def get_next_cycle(date=datetime.now()):
    for c in CYCLES:
        start = dateparser.parse(c['start'])
        if start >= date:
            return c

def get_past_cycles():
    return [c for c in CYCLES if dateparser.parse(c['end']) < datetime.now()]

def get_future_cycles():
    return [c for c in CYCLES if dateparser.parse(c['start']) > datetime.now()]

def get_current_or_last_cycle():
    return [c for c in CYCLES if dateparser.parse(c['start']) < datetime.now()][-1]

def get_cycle_by_date(date):
    try:
        date = dateparser.parse(date)
        if not date:
            return None
    except ValueError: #couldn't parse that date
        return None
    return [c for c in CYCLES if dateparser.parse(c['start']) < date][-1]

def is_request_valid(request):
    is_token_valid = request.form['token'] == 'fdpOhzy5YX8jOkxDWJf2Atlt'
    is_team_id_valid = request.form['team_id'] == 'T0258KQ7G'

    # is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    # is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']
    return is_token_valid and is_team_id_valid

def get_cycle_by_name(name):
    match = [c for c in CYCLES if c['name'].lower() == name.lower()]
    return match[0] if len(match) > 0 else None

@app.route('/buffercycles', methods=['POST'])
def buffercycles():
    if not is_request_valid(request):
        abort(400)

    command = request.form.get('text', 'now')
    if command in ['now', '']:
        current_or_last = get_current_or_last_cycle()
        next_cycle = get_next_cycle()
        if dateparser.parse(current_or_last['end']) < datetime.now():
            text = ("Hello! We're currently mid-cycle!\n"
                    "The last cycle was {} which ended on {}!\n"
                    "The next cycle is {} which starts on {}").format(
                        current_or_last['name'],
                        current_or_last['end'],
                        next_cycle['name'],
                        next_cycle['start']
                    )
        else:
            week = week_difference(dateparser.parse(current_or_last['start']), datetime.now())
            text = ("Hello! We're currently in week {} of {}!\n"
                    "The next cycle is {} which starts {} and ends {}.").format(
                        week,
                        current_or_last['name'],
                        next_cycle['name'],
                        next_cycle['start'],
                        next_cycle['end'])
    elif command == 'past':
        past_cycles = get_past_cycles()
        text = '\n'.join(["{}: {} to {}".format(c['name'], c['start'], c['end']) for c in past_cycles])

    elif command == 'future':
        past_cycles = get_future_cycles()
        text = '\n'.join(["{}: {} to {}".format(c['name'], c['start'], c['end']) for c in past_cycles])

    elif command == 'all':
        text = '\n'.join(["{}: {} to {}".format(c['name'], c['start'], c['end']) for c in CYCLES])
    elif command == 'help':
        text = "Heyoo! You can try commands like `now`, `past`, `future`, `all` or specify a cycle name or date"
    elif get_cycle_by_name(command):
        cycle = get_cycle_by_name(command)
        text = ("Hello! The {} cycle starts {} and ends {}.").format(
                    cycle['name'],
                    cycle['start'],
                    cycle['end'])
    elif get_cycle_by_date(command):
        command_date = dateparser.parse(command)
        cycle = get_cycle_by_date(command)
        next_cycle = get_next_cycle(dateparser.parse(cycle['end']))
        if dateparser.parse(cycle['end']) < command_date:
            text = ("Hello! {} is mid-cycle!\n"
                    "The preceeding cycle is {} which ends on {}!\n"
                    "The next cycle is {} which starts on {}").format(
                        command_date.strftime('%Y-%m-%d'),
                        cycle['name'],
                        cycle['end'],
                        next_cycle['name'],
                        next_cycle['start']
                    )
        else:
            week = week_difference(dateparser.parse(cycle['start']), command_date)
            text = ("Hello! {} is in week {} of {}!\n".format(
                        command_date.strftime('%Y-%m-%d'),
                        week,
                        cycle['name']))
    else:
        text = "Sorry I didn't understand that! You can try commands like `now`, `past`, `future`, `all` or specify a cycle name or date"

    return jsonify(
        response_type='in_channel',
        text=text,
        icon_emoji=':bear:'
    )

if __name__ == '__main__':
    app.run(debug=True)
