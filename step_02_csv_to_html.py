
import os
import sqlite3

def get_data_from_db(db_path='properties.db'):
    data = []
    db_path = os.path.join(os.path.dirname(__file__), *db_path.split('/'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties_fact WHERE price > 20000 AND price < 100000 ORDER BY price_per_m2 ASC")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return data

def get_filtered_data_from_db(db_path='properties.db', filter='*'):
    data = []
    db_path = os.path.join(os.path.dirname(__file__), *db_path.split('/'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT * FROM properties_fact WHERE price > 20000 AND price < 100000 AND title LIKE '%{filter}%' ORDER BY price_per_m2 ASC"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return data


def get_newest_properties(db_path='properties.db'):
    from datetime import datetime
    data = []
    db_path = os.path.join(os.path.dirname(__file__), *db_path.split('/'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    today_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(f"SELECT * FROM properties_fact WHERE price > 20000 AND price < 100000 AND creation_date = '{today_date}' ORDER BY price_per_m2 ASC")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return data

def get_price_lowered(db_path='properties.db'):
    from datetime import datetime
    data = []
    db_path = os.path.join(os.path.dirname(__file__), *db_path.split('/'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    today_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(f"SELECT * FROM properties_fact WHERE price > 20000 AND price < 100000 AND first_price_per_m2 > min_price_per_m2 AND last_price_per_m2 = min_price_per_m2 ORDER BY price_per_m2 ASC")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return data

def get_price_raised(db_path='properties.db'):
    from datetime import datetime
    data = []
    db_path = os.path.join(os.path.dirname(__file__), *db_path.split('/'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    today_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(f"SELECT * FROM properties_fact WHERE price > 20000 AND price < 100000 AND last_price_per_m2 > min_price_per_m2 ORDER BY price_per_m2 ASC")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return data


def create_html_page(page_number, page_data, file_name):
    os.makedirs('html', exist_ok=True)
    with open(f'html/{file_name}_{page_number}.html', 'w', encoding='utf-8') as file:
        file.write('<div style="text-align:center; margin: 50px;">\n')
        if page_number > 1:
            file.write('<a href="properties_' + str(page_number - 1) + '.html" style="margin-right: 20px; font-size: 20px;">Previous</a>\n')
        file.write('<a href="properties_' + str(page_number + 1) + '.html" style="font-size: 20px;">Next</a>\n')
        file.write('</div>\n')

        file.write('<style>.property-card {display: flex; margin: 10px;}</style>\n')
        file.write('<style>.property-text {margin-left: 10px;}</style>\n')
        for index, property in enumerate(page_data):


            file.write('<div class="property-card">\n')
            file.write('<div style="display: flex;">\n')
            file.write('<div style="flex: 1;">\n')
            file.write('<img src="' + property['first_photo'] + '" alt="Property photo" style="width: 400px; height: 250px;">\n')
            file.write('</div>\n')
            file.write('<div style="flex: 1;">\n')
            file.write('<div class="property-text">\n')
            file.write('<h1>' + property['title'] + '</h1>\n')
            file.write('<p>Price: ' + "{:,.2f}".format(property['price']) + '</p>\n')
            file.write('<p>Rooms: ' + str(property['rooms']) + '</p>\n')
            file.write('<p>Bathrooms: ' + str(property['bathrooms']) + '</p>\n')
            file.write('<p>Square Meters: ' + str(property['square_meters']) + '</p>\n')
            file.write('<p>Location: ' + property['location'] + '</p>\n')
            file.write('<p>Link: <a href="' + property['link'] + '" target="_blank">Link</a></p>\n')
            file.write('<p>Processing Date: ' + str(property['processing_date']) + '</p>\n')
            file.write('<p>Creation Date: ' + str(property['creation_date']) + '</p>\n')
            file.write('</div>\n')
            file.write('</div>\n')
            file.write('<div style="flex: 1;">\n')
            file.write('<table>\n')
            file.write('<tr><td>\n')
            file.write('<h2>$ x m2: ' + "{:,.2f}".format(property['price_per_m2']) + '</h2>\n')
            file.write('<h2>Min $: ' + "{:,.2f}".format(property['min_price_per_m2']) + '</h2>\n')
            file.write('<h2>First $: ' + "{:,.2f}".format(property['first_price_per_m2']) + '</h2>\n')
            file.write('</td><td>\n')
            if property['last_price_per_m2'] > property['first_price_per_m2']:
                file.write('<p>Price Trend: Up</p>\n')
            elif property['last_price_per_m2'] < property['first_price_per_m2']:
                file.write('<p>Price Trend: Down</p>\n')
            else:
                file.write('<p>Price Trend: Stable</p>\n')
            from datetime import datetime
            now = datetime.now()
            days_since_update = (now - datetime.strptime(property['creation_date'], '%Y-%m-%d')).days
            file.write('<p>Published: ' + str(days_since_update) + ' days ago</p>\n')
            file.write('</td></tr>\n')
            file.write('</table>\n')
            file.write('</div>\n')
            file.write('</div>\n')
            file.write('</div>\n')
            file.write('<hr>\n')

        file.write('<div style="text-align:center; margin: 50px;">\n')
        if page_number > 1:
            file.write('<a href="properties_' + str(page_number - 1) + '.html" style="margin-right: 20px; font-size: 20px;">Previous</a>\n')
        file.write('<a href="properties_' + str(page_number + 1) + '.html" style="font-size: 20px;">Next</a>\n')
        file.write('</div>\n')

def create_pages(properties_per_page, properties_list, file_name = 'properties'):
    num_pages = min(6, len(properties_list) // properties_per_page + (len(properties_list) % properties_per_page > 0))
    for page_number in range(1, num_pages + 1):  # Create up to 6 pages
        start_index = (page_number - 1) * properties_per_page
        end_index = start_index + properties_per_page
        page_data = properties_list[start_index:end_index]
        create_html_page(page_number, page_data, file_name)

def run():
    db = 'properties.db'
    properties_per_page = 100
    properties_list = get_data_from_db(db)
    properties_new = get_newest_properties(db)
    properties_low = get_price_lowered(db)
    properties_high = get_price_raised(db)
    properties_terr = get_filtered_data_from_db(db, 'terreno')
    properties_dpto = get_filtered_data_from_db(db, 'departamento')
    properties_casa = get_filtered_data_from_db(db, 'casa')
    create_pages(100, properties_list, 'properties')
    create_pages(100, properties_new, 'nuevos')
    create_pages(100, properties_low, 'bajaron')
    create_pages(100, properties_high, 'aumentaros')
    create_pages(100, properties_terr, 'terrenos')
    create_pages(100, properties_dpto, 'deptos')
    create_pages(100, properties_casa, 'casas')

run()