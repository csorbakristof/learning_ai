"""
Configuration for data collector application

Add your scraping configurations here
"""

# DLNEP - Neptun System Configuration
NEPTUN_CONFIG = {
    'login_url': 'https://neptun.bme.hu/oktatoi/login.aspx',
    'courses_url': 'https://neptun.bme.hu/oktatoi/main.aspx?ismenuclick=true&ctrl=1902',
    'dropdown_alt_text': 'Lehetőségek',
    'grades_menu_text': 'Jegybeírás',
    'export_button_alt': 'Exportálás Excel-fájlba',
    'download_timeout': 30  # seconds
}

# DLXLS - BME Portal Configuration
BME_PORTAL_CONFIG = {
    'login_url': 'https://www.aut.bme.hu',
    'workload_url': 'https://www.aut.bme.hu/StaffMembers/MyWorkload.aspx',
    'export_link_text': 'Terhelés exportálása',
    'target_worksheet_keyword': 'konzultáció',
    'download_timeout': 30  # seconds
}

# Example scraping configurations
SCRAPING_CONFIGS = {
    'quotes_example': {
        'type': 'requests',
        'url': 'https://quotes.toscrape.com/',
        'selectors': {
            'quote': '.quote .text',
            'author': '.quote .author',
            'tags': '.quote .tags'
        }
    },
    
    'selenium_example': {
        'type': 'selenium',
        'url': 'https://example.com',
        'require_login': False,
        'actions': [
            {
                'type': 'wait',
                'seconds': 2
            },
            {
                'type': 'click',
                'by': 'ID',
                'value': 'some-button-id'
            },
            {
                'type': 'extract',
                'selectors': {
                    'title': 'h1',
                    'description': '.description'
                }
            }
        ]
    }
}

# Add your custom configurations here
