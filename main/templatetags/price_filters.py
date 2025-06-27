from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def format_price(value):
    """Format price with thousands separators using dots (Indonesian format)"""
    if value is None:
        return "0"
    
    try:
        # Convert to int if it's a decimal without decimal places
        if isinstance(value, (Decimal, float)) and value == int(value):
            value = int(value)
        
        # Format with dots as thousands separator
        return f"{value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(value)
