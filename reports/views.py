
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from transactions.models import Transaction
from django.db.models import Sum
from decimal import Decimal
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class SummaryReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date', type=OpenApiTypes.DATE, description='Başlangıç tarihi (YYYY-MM-DD)'),
            OpenApiParameter(name='end_date', type=OpenApiTypes.DATE, description='Bitiş tarihi (YYYY-MM-DD)'),
        ]
    )

    def get(self, request):
        user = request.user
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')
        if not start or not end:
            return Response({'detail':'start_date and end_date required'}, status=400)


        qs = Transaction.objects.filter(user=user, date__range=(start, end))
        income = qs.filter(type='credit').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        expense = qs.filter(type='debit').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        net = income - expense
        top = qs.filter(type='debit').values('category').annotate(total=Sum('amount')).order_by('-total')[:5]
        top_list = [{'category': t['category'] or 'Uncategorized', 'amount': str(t['total'] or 0)} for t in top]
        return Response({
            'start_date': start,
            'end_date': end,
            'total_income': str(income),
            'total_expense': str(expense),
            'net_cash_flow': str(net),
            'top_expense_categories': top_list
        })
