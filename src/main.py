import requests
import json
from config import ParserConfig
import csv


def divide_cookies(str):

    """ Function which returned divide dict with cookies """

    lst_cook = str.split('; ')
    cookie_dict = {}
    for elem in lst_cook:
        bef_dict_lst = elem.split('=', 1)
        cookie_dict[bef_dict_lst[0]] = bef_dict_lst[1]

    for key in cookie_dict.keys():
        cookie_dict[key] = cookie_dict[key].replace('"', '')
    return cookie_dict


def dict_headers():

    """ Function which return dict with user-agent data"""

    dict_head = {}
    dict_head['User-Agent'] = ParserConfig.user_brows
    dict_head['X-Li-Track'] = ParserConfig.x_line
    dict_head['Csrf-Token'] = ParserConfig.csrf_token
    return dict_head


def extract_skills_from_json(json_f):

    """ Function which return extracting data from JSON format file """

    try:
        lst_with_skills = []
        json_dmp = json.dumps(json_f['elements'][0]['suggestedEntities'])
        true_json = json.loads(json_dmp)
        for i in true_json:
            lst_with_skills.append(i['optionText']['text'])
    except:
        lst_with_skills.append('No information')
    return lst_with_skills


def extract_titles():

    """ Function which return list with changed titles"""

    with open('titles_clear.txt', 'r') as file:
        clear_titles = file.readlines()

    titles_lst = []
    for title in clear_titles:
        div_row = title.split(', ')
        titles_lst.append(div_row[1].replace('\n', ''))

        # titles.append(title[1].replace('\n', ''))
    for index, elem in enumerate(titles_lst):
        titles_lst[index] = elem.replace(' ', '%20')
    return titles_lst


def extract_true_titles():

    """ Function which return list with changed titles withount inserting special symbols """

    with open('titles_clear.txt', 'r') as file:
        a = file.readlines()

    titles_lst = []
    for title in a:
        div_row = title.split(', ')
        titles_lst.append(div_row[1].replace('\n', ''))
    return titles_lst


def list_links_add_dict(lst_with_titles, url):

    """ Function which return list with links for each title """

    lst_links = []
    for name in lst_with_titles:
        lst_links.append(url.replace('Owner', name))
    return lst_links


def return_dict():

    """ Function which return dict with titles and id"""

    with open('titles_clear.txt', 'r') as f:
        rows = f.readlines()
        lst = []
        for row in rows:
            lst.append(row)
    new_dict = {}
    for row in lst:
        a = row.split(', ')
        new_dict[a[1].replace('\n', '')] = int(a[0])
    return new_dict


if __name__ == "__main__":
    dict_id = return_dict()
    dict_with_skills = {}

    with open('shallom.csv', 'a') as file:
        lst = ['id', 'title', 'skills']
        writer = csv.writer(file)
        writer.writerow(lst)
        print('Add string header')
        file.close()

    links = list_links_add_dict(extract_titles(), ParserConfig.first_url)
    titles = extract_true_titles()

    for title, link in zip(titles, links):
        try:
            response = requests.get(
                url=link,
                headers=dict_headers(),
                cookies=divide_cookies(ParserConfig.cookie)
            )
            dict_with_skills[title] = extract_skills_from_json(response.json())

            with open('shallom.csv', 'a') as f:
                lst = [dict_id[title], title, extract_skills_from_json(response.json())]
                writer = csv.writer(f)
                writer.writerow(lst)
                print(dict_id[title])
                f.close()
        except:
            dict_with_skills[title] = ['No information']

            with open('shallom.csv', 'a') as f:
                lst = [dict_id[title], title, ['No information']]
                writer = csv.writer(f)
                writer.writerow(lst)
                f.close()