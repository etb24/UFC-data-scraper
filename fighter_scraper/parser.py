from bs4 import BeautifulSoup
import time


def safe_text(element, default='None'):
    return element.text.strip() if element else default

#parse bio section for place of birth
def extract_bio_field(soup, field_name):
    bio_fields = soup.find_all('div', class_='c-bio__field')
    
    for field in bio_fields:
        label_div = field.find('div', class_='c-bio__label')
        value_div = field.find('div', class_='c-bio__text')

        if not label_div or not value_div:
            continue
        
        label = label_div.text.strip().lower()
        target = field_name.strip().lower()

        if target in label:  #allows partial matches
            return value_div.text.strip()
    
    return ''


def parse_fighter_data(driver, url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    place_text = extract_bio_field(soup, 'Place of Birth')
    parts = [p.strip() for p in place_text.split(',')]
    country = parts[-1] if parts else 'Unknown'


    fighter = {
        'Name': safe_text(soup.find('h1', class_='hero-profile__name')),
        'Nickname': safe_text(soup.find('p', class_='hero-profile__nickname')),
        'Weight Class': safe_text(soup.find('p', class_='hero-profile__division-title')),
        'Record': safe_text(soup.find('p', class_='hero-profile__division-body')),
        'Place of Birth': place_text,
        'Country': country
    }

    stats = {
        'Knockouts': '0',
        'Submissions': '0',
        'First Round Finishes': '0',
        'Striking Accuracy': 'N/A',
        'Takedown Accuracy': 'N/A',
        'Sig Str Landed Total': '0',
        'Sig Str Attempted Total': '0',
        'Takedowns Landed Total': '0',
        'Takedowns Attempted Total': '0',
        'Sig Strikes Per Min': 'N/A',
        'Takedown Avg Per Min': 'N/A',
        'Sig Str Def': 'N/A',
        'Knockdown Avg': 'N/A',
        'Sig Strikes Absorbed Per Min': 'N/A',
        'Sub Avg Per Min': 'N/A',
        'Takedown Def': 'N/A',
        'Avg Fight Time': 'N/A',
        'Sig Strikes While Standing': 'N/A',
        'Sig Strikes While Clinched': 'N/A',
        'Sig Strikes While Grounded': 'N/A',
        'Sig Strikes Head': 'N/A',
        'Sig Strikes Body': 'N/A',
        'Sig Strikes Leg': 'N/A',
        'Win by KO/TKO': '0(0%)',
        'Win by Decision': '0(0%)',
        'Win by Submission': '0(0%)'
    }

    try:
        groups1 = soup.find_all("div", class_="c-stat-compare__group c-stat-compare__group-1")
        for group in groups1:
            label = safe_text(group.find("div", class_="c-stat-compare__label")).lower()
            value = safe_text(group.find("div", class_="c-stat-compare__number"), 'N/A')

            if "str. landed" in label:
                stats['Sig Strikes Per Min'] = value
            elif "taked" in label:
                stats['Takedown Avg Per Min'] = value
            elif "str. def" in label:
                stats['Sig Str Def'] = value
            elif "knock" in label:
                stats['Knockdown Avg'] = value
    except:
        pass

    try:
        groups2 = soup.find_all("div", class_="c-stat-compare__group c-stat-compare__group-2")
        for group in groups2:
            label = safe_text(group.find("div", class_="c-stat-compare__label")).lower()
            value = safe_text(group.find("div", class_="c-stat-compare__number"), 'N/A')
            if "str. abs" in label:
                stats['Sig Strikes Absorbed Per Min'] = value
            elif "subm" in label:
                stats['Sub Avg Per Min'] = value
            elif "takedown def" in label:
                stats['Takedown Def'] = value
            elif "fight time" in label:
                stats['Avg Fight Time'] = value
    except:
        pass

    try:
        groups3 = soup.find_all("div", class_='c-stat-3bar__group')
        for group in groups3:
            label = safe_text(group.find("div", class_="c-stat-3bar__label")).lower()
            value = safe_text(group.find("div", class_="c-stat-3bar__value"), '0(0%)')
            if "standing" in label:
                stats['Sig Strikes While Standing'] = value
            elif "clinch" in label:
                stats['Sig Strikes While Clinched'] = value
            elif "ground" in label:
                stats['Sig Strikes While Grounded'] = value
            elif "tko" in label:
                stats['Win by KO/TKO'] = value
            elif "dec" in label:
                stats['Win by Decision'] = value
            elif "sub" in label:
                stats['Win by Submission'] = value
    except:
        pass

    try:
        if soup.find('div', class_='c-stat-body__title'):
            stats['Sig Strikes Head'] = safe_text(soup.find('text', id='e-stat-body_x5F__x5F_head_value')) + '(' + safe_text(soup.find('text', id='e-stat-body_x5F__x5F_head_percent')) + ')'
            stats['Sig Strikes Body'] = safe_text(soup.find('text', id='e-stat-body_x5F__x5F_body_value')) + '(' + safe_text(soup.find('text', id='e-stat-body_x5F__x5F_body_percent')) + ')'
            stats['Sig Strikes Leg'] = safe_text(soup.find('text', id='e-stat-body_x5F__x5F_leg_value')) + '(' + safe_text(soup.find('text', id='e-stat-body_x5F__x5F_leg_percent')) + ')'
    except:
        pass

    try:
        labels = [el.text.lower() for el in soup.find_all("p", class_="athlete-stats__text athlete-stats__stat-text")]
        values = [el.text for el in soup.find_all("p", class_="athlete-stats__text athlete-stats__stat-numb")]
        for i, label in enumerate(labels):
            if "knock" in label:
                stats['Knockouts'] = values[i]
            elif "subm" in label:
                stats['Submissions'] = values[i]
            elif "finish" in label:
                stats['First Round Finishes'] = values[i]
    except:
        pass


    try:
        dt_labels = [el.text.lower() for el in soup.find_all('dt', class_='c-overlap__stats-text')]
        dd_values = [el.text for el in soup.find_all('dd', class_='c-overlap__stats-value')]
        for i, label in enumerate(dt_labels):
            if "strikes landed" in label:
                stats['Sig Str Landed Total'] = dd_values[i]
            elif "strikes attempted" in label:
                stats['Sig Str Attempted Total'] = dd_values[i]
            elif "takedowns landed" in label:
                stats['Takedowns Landed Total'] = dd_values[i]
            elif "takedowns attempted" in label:
                stats['Takedowns Attempted Total'] = dd_values[i]
    except:
        pass

    try:
        accuracy_values = [el.text.strip() for el in soup.find_all('text', class_='e-chart-circle__percent')]

        if len(accuracy_values) >= 1:
            stats['Striking Accuracy'] = accuracy_values[0]
        if len(accuracy_values) >= 2:
            stats['Takedown Accuracy'] = accuracy_values[1]
    except:
        pass

    fighter.update(stats)

    return fighter
