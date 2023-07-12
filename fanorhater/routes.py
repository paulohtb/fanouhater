from flask import render_template, request
from bs4 import BeautifulSoup
from datetime import datetime
from fanorhater import app
import os
import re


@app.route('/')
def home():
    return render_template('initialpage.html')


@app.route('/uploads')
def uploads():
    return render_template('uploadpage.html')


@app.route('/choices', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return render_template('choices.html')


@app.route('/following', methods=['GET', 'POST'])
def following():
    with open('data/following.html') as fihtml:
        soup = BeautifulSoup(fihtml, 'html.parser')
        username = [(element.find('a').text.strip(),
                     extract_date(element)) for element in soup.find_all('div', class_='_a6-p')]
        usernames = sorted(username, key=lambda x: x[1], reverse=True)
        nicks = [(nick, date.strftime('%d/%m/%Y %H:%M')) for nick, date in usernames]
        return render_template('following.html', content=nicks)


@app.route('/followers', methods=['GET', 'POST'])
def followers():
    with open('data/followers_1.html') as fehtml:
        soup = BeautifulSoup(fehtml, 'html.parser')
        username = [(element.find('a').text.strip(),
                     extract_date(element)) for element in soup.find_all('div', class_='_a6-p')]
        usernames = sorted(username, key=lambda x: x[1], reverse=True)
        nicks = [(nick, date.strftime('%d/%m/%Y %H:%M')) for nick, date in usernames]
        return render_template('followers.html', content=nicks)


@app.route('/notfollowers', methods=['GET', 'POST'])
def not_followers():
    with open('data/following.html') as fihtml, open('data/followers_1.html') as fehtml:
        following_soup = BeautifulSoup(fihtml, 'html.parser')
        following_username = [(element.find('a').text.strip(),
                               extract_date(element)) for element in following_soup.find_all('div', class_='_a6-p')]
        followers_soup = BeautifulSoup(fehtml, 'html.parser')
        followers_username = [(element.find('a').text.strip(),
                               extract_date(element)) for element in followers_soup.find_all('div', class_='_a6-p')]
        username = [(nick, date.strftime('%d/%m/%Y %H:%M')) for nick, date in following_username
                    if nick not in [n for n, _ in followers_username]]
        usernames = sorted(username, key=lambda x: datetime.strptime(x[1], '%d/%m/%Y %H:%M'), reverse=True)
        nicks = [(nick, date) for nick, date in usernames]
        return render_template('not_followers.html', content=nicks)


def extract_date(element):
    date_str = element.find_all('div')[-1].text.strip()
    date_str = date_str.replace('de', '').strip()
    pattern = r'(\d{1,2})\s+(\w+)\s+(\d{4})\s+(\d{1,2}):(\d{2})'
    match = re.match(pattern, date_str)
    if match:
        day, month, year, hour, minute = match.groups()
        month_map = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
                     'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}
        month_num = month_map.get(month.lower(), 1)
        return datetime(int(year), month_num, int(day), int(hour), int(minute))
