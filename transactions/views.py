# transactions/views.py
import csv
from decimal import Decimal, InvalidOperation
from io import TextIOWrapper
from django.db import transaction as db_transaction, IntegrityError
from rest_framework import generics, permissions, serializers, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.dateparse import parse_date
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Transaction, ImportBatch
from .serializers import TransactionSerializer
import requests


def get_category_from_description(description: str) -> str:
    description = description.lower()
    if "kira" in description:
        return "Kira Gideri"
    elif "fatura" in description:
        return "Fatura"
    elif "satış" in description:
        return "Gelir"
    elif "market" in description:
        return "Market"
    elif "maaş" in description:
        return "Maaş"
    return "Diğer"


def convert_currency_to_try(amount: float, currency: str) -> float:
    if currency.upper() == "TRY":
        return amount
    try:
        response = requests.get(
            f"https://api.exchangerate.host/latest?base={currency.upper()}&symbols=TRY"
        )
        data = response.json()
        rate = data["rates"]["TRY"]
        return round(amount * rate, 2)
    except Exception:
        return amount


class TransactionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TransactionPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['type', 'category', 'currency']
    search_fields = ['description']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(user=user)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)

        return queryset



class TransactionUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {'type': 'string', 'format': 'binary'}
                }
            }
        },
        responses={201: TransactionUploadSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = TransactionUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csvfile = serializer.validated_data['file']

        try:
            text_file = TextIOWrapper(csvfile.file, encoding='utf-8-sig')
        except Exception:
            text_file = TextIOWrapper(csvfile, encoding='utf-8-sig')

        reader = csv.DictReader(text_file)
        rows = list(reader)
        if not rows:
            return Response({'detail':'empty file'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                batch = ImportBatch.objects.create(
                    user=request.user,
                    row_count=len(rows),
                    inserted_count=0,
                    error_summary={}
                )

                hashes, parsed, errors = [], [], []

                for idx, row in enumerate(rows, start=1):
                    d = row.get('date')
                    amt_s = row.get('amount')
                    curr = (row.get('currency') or '').strip()
                    desc = (row.get('description') or '').strip()
                    typ = (row.get('type') or '').strip().lower()
                    ctgry = get_category_from_description(desc)

                    pd = parse_date(d)
                    if not pd:
                        errors.append({'row':idx,'error':'invalid date','value':d})
                        break
                    try:
                        amt = Decimal(amt_s)
                    except (InvalidOperation, TypeError):
                        errors.append({'row':idx,'error':'invalid amount','value':amt_s})
                        break
                    if typ not in ('credit','debit'):
                        errors.append({'row':idx,'error':'invalid type','value':typ})
                        break

                    if amt < 0:
                        amt = abs(amt)

                    unique = Transaction.make_hash(request.user.id, pd.isoformat(), str(amt), curr, desc)
                    hashes.append(unique)
                    parsed.append({
                        'date': pd,
                        'amount': amt,
                        'currency': curr,
                        'category': ctgry,          # ✅ düzeltildi
                        'description': desc,
                        'type': typ,
                        'unique': unique
                    })

                if errors:
                    raise ValueError({'errors': errors})

                existing = set(Transaction.objects.filter(user=request.user, unique_hash__in=hashes).values_list('unique_hash', flat=True))
                to_create = [
                    Transaction(
                        user=request.user,
                        date=p['date'],
                        amount=p['amount'],
                        currency=p['currency'],
                        description=p['description'],
                        type=p['type'],
                        category=p['category'],
                        unique_hash=p['unique']
                    )
                    for p in parsed if p['unique'] not in existing
                ]

                Transaction.objects.bulk_create(to_create, batch_size=500)
                batch.inserted_count = len(to_create)
                batch.save()

                return Response({
                    'batch_id': batch.id,
                    'row_count': batch.row_count,
                    'inserted_count': batch.inserted_count
                }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({'detail':'Integrity error'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'detail':'validation error','errors': ve.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({'detail':'unexpected error','error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
