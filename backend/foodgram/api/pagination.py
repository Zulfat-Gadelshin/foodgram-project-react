from rest_framework.pagination import PageNumberPagination


class CustomPageLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
