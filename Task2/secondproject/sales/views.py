import tempfile
from rest_framework import generics
from .models import SalesData
from django.http import FileResponse
from .serializers import SalesDataSerializer
from django.db.models import Count, Sum
from django.http import HttpResponse
from rest_framework.views import APIView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import io
import os
from .models import SalesData


class SalesDataListCreateView(generics.ListCreateAPIView):
    queryset = SalesData.objects.all()
    serializer_class = SalesDataSerializer


class SalesDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalesData.objects.all()
    serializer_class = SalesDataSerializer



class GenerateReportAPI(APIView):
    def get(self, request):
        # Total number of orders count per year
        orders_per_year = SalesData.objects.values('order_date__year').annotate(count=Count('id'))

        # Total count of distinct customers
        distinct_customers_count = SalesData.objects.values('customer_id').distinct().count()

        # Top 3 customers who have ordered the most with their total amount of transactions
        top_customers = (
            SalesData.objects.values('customer_id', 'customer_name')
            .annotate(total_amount=Sum('sales'))
            .order_by('-total_amount')[:3]
        )

        # Customer Transactions per Year (from the beginning year to last year)
        customer_transactions_per_year = (
            SalesData.objects.values('customer_id', 'order_date__year')
            .annotate(count=Count('id'))
            .order_by('order_date__year')
        )

        # Most selling items sub-category names
        subcategory_names = (
            SalesData.objects.values('sub_category')
            .annotate(count=Count('id'))
            .order_by('-count')
            .values_list('sub_category', flat=True)[:5]
        )

        # Region basis sales performance pie chart
        region_sales = (
            SalesData.objects.values('region')
            .annotate(sales=Sum('sales'))
            .order_by('-sales')
        )
        regions = [entry['region'] for entry in region_sales]
        sales = [entry['sales'] for entry in region_sales]
        plt.pie(sales, labels=regions, autopct='%1.1f%%')
        plt.axis('equal')
        plt.title('Sales Performance by Region')

        # Save the pie chart to a buffer
        pie_chart_buffer = io.BytesIO()
        plt.savefig(pie_chart_buffer, format='png')
        plt.close()

        # Sales performance line chart over the years
        sales_over_years = (
            SalesData.objects.values('order_date__year')
            .annotate(sales=Sum('sales'))
            .order_by('order_date__year')
        )
        years = [entry['order_date__year'] for entry in sales_over_years]
        sales = [entry['sales'] for entry in sales_over_years]
        plt.plot(years, sales)
        plt.xlabel('Year')
        plt.ylabel('Sales')
        plt.title('Sales Performance Over the Years')

        # Save the line chart to a buffer
        line_chart_buffer = io.BytesIO()
        plt.savefig(line_chart_buffer, format='png')
        plt.close()

       # Generate the PDF report
        buffer = io.BytesIO()
        report = canvas.Canvas(buffer, pagesize=letter)

        # Set up the report content
        report.setTitle("Sales Report")

       #total number of orders count per year
        report.setFont("Helvetica", 12)
        report.drawString(50, 700, "Total Number of Orders Count per Year:")
        y = 680
        for entry in orders_per_year:
         year = entry['order_date__year']
         count = entry['count']
         report.drawString(50, y, f"{year}: {count} orders")
         y -= 20

       # Add the total count of distinct customers
        report.setFont("Helvetica", 12)
        report.drawString(50, 600, f"Total Count of Distinct Customers: {distinct_customers_count}")

       #  top 3 customers who have ordered the most with their total amount of transactions
        report.setFont("Helvetica", 12)
        report.drawString(50, 550, "Top 3 Customers with Total Amount of Transactions:")
        y = 530
        for entry in top_customers:
         customer_name = entry['customer_name']
         total_amount = entry['total_amount']
         report.drawString(50, y, f"{customer_name}: ${total_amount}")
         y -= 20

       # Add the customer transactions per year
        report.setFont("Helvetica", 12)
        report.drawString(50, 450, "Customer Transactions per Year:")
        y = 430
        current_year = None
        for entry in customer_transactions_per_year:
         year = entry['order_date__year']
         count = entry['count']
         if year != current_year:
          report.drawString(50, y, f"{year}: {count} transactions")
          y -= 20
          current_year = year
         else:
          report.drawString(70, y, f"{count} transactions")
          y -= 20

        # Add the most selling items sub-category names
        report.setFont("Helvetica", 12)
        report.drawString(50, 350, "Most Selling Items Sub-Category Names:")
        y = 330
        for subcategory in subcategory_names:
         report.drawString(50, y, subcategory)
         y -= 20

        # Add the region basis sales performance pie chart
        report.setFont("Helvetica", 12)
        report.drawString(50, 200, "Region Basis Sales Performance Pie Chart:")
        report.drawImage(pie_chart_buffer, 50, 220, width=400, height=300)

        # Add the sales performance line chart over the years
        report.setFont("Helvetica", 12)
        report.drawString(50, 50, "Sales Performance Line Chart Over the Years:")
        report.drawImage(line_chart_buffer, 50, 70, width=400, height=300)

        # Save the report to the PDF buffer
        report.showPage()
        report.save()

       # Set the buffer's file pointer at the beginning
        
        # pdf_bytes = buffer.getvalue()
        # buffer.close()

        buffer.seek(0)


        # Save the PDF buffer contents to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(buffer.getvalue())

        # Return the temporary file as a file response
        pdf_response = FileResponse(open(temp_file.name, 'rb'), content_type='application/pdf')
        pdf_response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        # Clean up the temporary file
        os.unlink(temp_file.name)

        return pdf_response

