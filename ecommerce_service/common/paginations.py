from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math


class CustomPagination(PageNumberPagination):
    page_size = 10                 
    page_size_query_param = "limit"   
    page_query_param = "page"        
    max_page_size = 100

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        limit = self.get_page_size(self.request)
        page = self.page.number
        total_pages = math.ceil(total_items / limit) if limit else 1

        return Response({
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages,
            "results": data,
        })

