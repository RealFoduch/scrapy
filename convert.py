import html_text
from tests import *

sample = {
    "company_name": "",
    "cvr_number": "",
    "address": "",
    "postal_code": "",
    "city": "",
    "start_date": "",
    "cessation_date": "",
    "business_type": "",
    "advertising_protection": "",
    "status": "",
    "expanded_business_information": {
        "municipality": "",
        "activity_code": "",
        "objects": "",
        "registered_for_vat": "",
        "activity_code_description": "",
        "financial_year": "",
        "latest_articles_of_association": "",
        "classes_of_shares": "",
        "registered_capital": "",
        "first_accounting_period": ""
    },
    "power_to_bind_and_key_individuals_and_auditor": {
        "power_to_bind": "",
        "branch_manager": [{
            "position": "",
            "name": "",
            "address": "",
            "postal_code": "",
            "city": "",
            "country": ""
        }],
        "branch_founders": [{
            "name": "",
            "address": "",
            "postal_code": "",
            "city": "",
            "country": ""
        }],
    },
    "owners": {
    },
    "information_on_main_company": {
    },
    "production_units": {
    }
}

# semi-universal converter
def convert(table1, table2, information, cout=0, dict=""):
    table2 = convert_url(table2)
    for element in table1:
        element = element.lstrip().rstrip()
        element = element.lower().split(" ")
        element = '_'.join(element)
        table2[cout] = table2[cout].lstrip().rstrip()
        if dict:
            information[dict][element] = table2[cout]
        else:
            if element == 'postal_code_and_city':
                information['postal_code'] = table2[cout][:4]
                information['city'] = table2[cout][5:]
            else:
                information[element] = table2[cout]
        cout += 1
    return information


def convert_url(urls):
    for index, element in enumerate(urls[:-1]):
        el = html_text.parse_html(element)
        if '<a' and 'href=' in element:
            urls[index] = el.xpath("//div/text()")[0] + el.xpath("//div/a/text()")[0] + " url:" + el.xpath("//div/a/@href")[0]
        else:
            urls[index] = el.xpath("//div/text()")[0]
    return urls

# converter power_to_bind_and_key_individuals_and_auditor
def convert_power_to_bind_and_key_individuals_and_auditor(table1, table2, information):
    table2 = convert_ptbakiaa_url(table2)
    power = 'power_to_bind_and_key_individuals_and_auditor'
    information[power]['power_to_bind'] = table2[0][0].lstrip().rstrip()
    for i in range(1, len(table2) - 1):
        free_dict = []
        count_el = 0
        for element in table2[i]:
            if 'url:' in element:
                count_el += 1
        count = (len(table2[i]) - 1)//count_el
        element = table1[i].lower().split(" ")
        element = '_'.join(element)
        branch = f'branch_{element}'
        if count == 5:
            for index in range(0, len(table2[i]) - 1, count):
                # myList.append({'joo': 48, 'par': 28})
                free_dict.append({
                    'position': table2[i][index].lstrip().rstrip(),
                    'name': table2[i][index + 1].lstrip().rstrip(),
                    'address': table2[i][index + 2].lstrip().rstrip(),
                    'postal_code': table2[i][index + 3].lstrip().rstrip()[:4],
                    'city': table2[i][index + 3].lstrip().rstrip()[5:],
                    'country': table2[i][index + 4].lstrip().rstrip(),
                })
        elif count == 4:
            for index in range(0, len(table2[i]) - 1, count):
                free_dict.append({
                    'name': table2[i][index + 1].lstrip().rstrip(),
                    'address': table2[i][index + 2].lstrip().rstrip(),
                    'postal_code': table2[i][index + 3].lstrip().rstrip()[:4],
                    'city': table2[i][index + 3].lstrip().rstrip()[5:],
                    'country': table2[i][index + 4].lstrip().rstrip(),
                })
        elif count == 3:
            for index in range(0, len(table2[i]) - 1, count):
                free_dict.append({
                    'name': table2[i][index].lstrip().rstrip(),
                    'address': table2[i][index + 1].lstrip().rstrip(),
                    'postal_code': table2[i][index + 2].lstrip().rstrip()[:4],
                    'city': table2[i][index + 2].lstrip().rstrip()[5:]
                })
        else:
            print("Нужен лог")
        information[power][branch] = free_dict
    return information


def convert_ptbakiaa_url(table, coordinate=1):
    table[0] = html_text.parse_html(table[0])
    table[0] = table[0].xpath('//div/text()')
    for index, element in enumerate(table[1:-1]):
        if index == 0:
            insert = True
            step = 5
        else:
            insert = False
            step = 4
        el = html_text.parse_html(element)
        table[index+1] = el.xpath('//div/text()')
        for j, i in enumerate(range(0, len(table[index+1])-1, step)):
            hpaths = el.xpath("//div/a/text()")[j] + " url:" + el.xpath("//div/a/@href")[j]
            if insert:
                table[index+1].insert(i + 1, hpaths)
            else:
                table[index+1][i] = hpaths
    return table


#ovnership converter
def convert_ownership(table1, table2, information):
    table2 = convert_ownership_url(table2)
    for i in range(0, len(table2) - 1):
        free_dict = []
        count_el = 0
        for element in table2[i]:
            if 'url:' in element:
                count_el += 1
        if count_el:
            count = (len(table2[i]))//count_el
        else:
            count = 1
        element = table1[i].lower().split(" ")
        element = '_'.join(element)
        branch = f'branch_{element}'
        if count == 6:
            for index in range(0, len(table2[i]), count):
                # myList.append({'joo': 48, 'par': 28})
                free_dict.append({
                    'name': table2[i][index].lstrip().rstrip(),
                    'address': table2[i][index + 1].lstrip().rstrip(),
                    'country': table2[i][index + 2].lstrip().rstrip(),
                    'pct_of_share_capital': table2[i][index + 3][23:].lstrip().rstrip(),
                    'pct_of_voting_rights': table2[i][index + 4][23:].lstrip().rstrip(),
                    'date_of_change': table2[i][index + 5][16:].lstrip().rstrip(),
                })
        elif count == 7:
            for index in range(0, len(table2[i]), count):
                free_dict.append({
                    'name': table2[i][index].lstrip().rstrip(),
                    'address': table2[i][index + 1].lstrip().rstrip(),
                    'post': table2[i][index + 2].lstrip().rstrip(),
                    'country': table2[i][index + 3].lstrip().rstrip(),
                    'pct_of_share_capital': table2[i][index + 3][23:].lstrip().rstrip(),
                    'pct_of_voting_rights': table2[i][index + 4][23:].lstrip().rstrip(),
                    'date_of_change': table2[i][index + 5][16:].lstrip().rstrip(),
                })
        elif count == 1:
            for index in range(0, len(table2[i]), count):
                free_dict.append({
                    'info': table2[i][index].lstrip().rstrip(),
                })
        else:
            print("Нужен лог")
        information['owners'][branch] = free_dict
    return information


def convert_ownership_url(table):
    for index, element in enumerate(table[:]):
        if index == 0:
            step = 6
        else:
            step = 7
        el = html_text.parse_html(element)
        table[index] = el.xpath('//div/text()')
        check = table[index]
        while '\n' in check:
            check.remove('\n')
        if len(check) != 1:
            for j, i in enumerate(range(0, len(table[index])-1, step)):
                hpaths = el.xpath("//div/a/text()")[j] + " url:" + el.xpath("//div/a/@href")[j]
                # table[index][i] = hpaths
                table[index].insert(i, hpaths)
        else:
            table[index] = check
    return table

# history converter
def convert_history(table, information):
    table = convert_history_first(table)
    reg = 'registration_history_in_danish'
    free_dict = []
    for i, inform in enumerate(table):
        free_dict.append({})
        free_dict[i]['record_date'] = inform[0][:10]
        free_dict[i]['record_type'] = inform[0][11:]
        free_dict[i]['cvr_number'] = inform[1]
        j = 3
        while j < len(inform):
            my_info = ''
            if ':' in inform[j]:
                if inform[j][-1] == ':':
                    element = inform[j].lower().split(" ")
                    element = '_'.join(element)
                    key = element[:-1]
                else:
                    key = inform[j][:inform[j].index(':')]
                    key = key.lower().split(" ")
                    key = '_'.join(key)
                    my_info = inform[j][inform[j].index(':') + 1:]
                while j + 1 < len(inform):
                    j += 1
                    if ':' in inform[j]:
                        j -= 1
                        break
                    else:
                        my_info += ' ' + inform[j]
            else:
                inform[j] = inform[j] + ':'
                print('continue')
                continue

            free_dict[i][key] = my_info.lstrip().rstrip()
            j += 1
            # print(free_dict)
        information['registration_history_in_danish'] = free_dict
    return information


def convert_history_first(table):
    for i, element in enumerate(table):
        el = html_text.parse_html(element)
        el = el.xpath('//text()')
        while '\n' in el:
            el.remove('\n')
        for j, ele in enumerate(el):
            el[j] = el[j].lstrip().rstrip()
        table[i] = el
        if table[i] == ['Show fewer registrations'] or table[i] == [] or table[i] == ['Close Registration history (in Danish)']:
            table.pop(i)
    return table[:-1]
