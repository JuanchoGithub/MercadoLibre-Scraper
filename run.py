import step_01_scrap_data
import step_02_csv_to_html

# Run step 1
scraper = step_01_scrap_data.Scraper()
scraper.menu()
scraper.scraping('inmuebles en venta en monte grande')
scraper.data = [x for x in scraper.data if x['price_per_m2'] is not None]
scraper.data.sort(key=lambda x: x['price_per_m2'])
scraper.export_to_csv()

# Run step 2
step_02_csv_to_html.create_html_page()
