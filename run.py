import step_01_scrap_data
import step_02_csv_to_html
import step_03_analytics

# Run step 1
step_01_scrap_data.run('inmuebles en venta en monte grande')

# Run step 2
step_02_csv_to_html.run()

# Run step 3
import os
step_03_analytics.store_csv_to_sqlite(os.path.join(os.path.dirname(__file__), 'data', 'mercadolibre_scraped_data.csv'))
