UZ_MONTHS = (
    'Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun',
    'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr',
)


def format_uz_date(value):
    """date(2026, 10, 12) -> '12 Oktabr, 2026'"""
    return f'{value.day:02d} {UZ_MONTHS[value.month - 1]}, {value.year}'


def format_time_range(start, end=None):
    """09:00 — 18:00"""
    if end is None:
        return f'{start:%H:%M}'
    return f'{start:%H:%M} — {end:%H:%M}'
