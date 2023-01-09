import math


def make_pagination_range(
    page_range,
    qt_pages,
    current_page,
):
    middle_range = math.ceil(qt_pages/2)
    # vai arredondar o meio do range
    start_range = current_page - middle_range
    stop_range = current_page + middle_range

    # tratando o range offset - saiu fora do range negativo -  abs pra transformar de neg pra pos
    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        start_range += start_range_offset

    return page_range[start_range:stop_range]
