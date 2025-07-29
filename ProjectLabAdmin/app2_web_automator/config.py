"""
Configuration for web automator application

Add your automation configurations here
"""

# Example automation configurations
AUTOMATION_CONFIGS = {
    'form_filling_example': {
        'url': 'https://example.com/form',
        'require_login': True,
        'actions': [
            {
                'type': 'wait',
                'seconds': 2
            },
            {
                'type': 'input',
                'by': 'ID',
                'value': 'name-field',
                'field_name': 'name'  # Column name from Excel
            },
            {
                'type': 'input',
                'by': 'ID', 
                'value': 'email-field',
                'field_name': 'email'  # Column name from Excel
            },
            {
                'type': 'select',
                'by': 'ID',
                'value': 'category-dropdown',
                'field_name': 'category'  # Column name from Excel
            },
            {
                'type': 'click',
                'by': 'ID',
                'value': 'submit-button'
            },
            {
                'type': 'wait',
                'seconds': 3
            }
        ]
    },
    
    'search_example': {
        'url': 'https://example.com/search',
        'require_login': False,
        'actions': [
            {
                'type': 'input',
                'by': 'NAME',
                'value': 'search',
                'field_name': 'search_term'  # Column name from Excel
            },
            {
                'type': 'click',
                'by': 'CSS_SELECTOR',
                'value': 'button[type="submit"]'
            },
            {
                'type': 'wait',
                'seconds': 5
            }
        ]
    }
}

# Add your custom configurations here
