import random
import time
from io import BytesIO
from datetime import datetime
from collections import defaultdict
from threading import Event, Thread

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer

from core.models import Users, Incomes, Expenses
from core.serializers import IncomeSerializer, ExpenseSerializer
from .serializers import SendCodeSerializer, ValidateCodeSerializer, ChangePasswordSerializer


RECOVERY_CODES = {}

class SendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data["user_name"]
            email = serializer.validated_data["email"]
            try:
                user = Users.objects.get(user_name=user_name, email=email)
                code = str(random.randint(100000, 999999)) 
                RECOVERY_CODES[user.user_name] = code
                send_mail(
                    subject="Password Recovery Code",
                    message=f"Your recovery code is {code}",
                    from_email=None,
                    recipient_list=[email],
                )
                return Response({"message": "Recovery code sent successfully."}, status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                return Response({"error": "User with provided details not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ValidateCodeSerializer(data=request.data)
        if serializer.is_valid():
            recovery_code = serializer.validated_data["recovery_code"]
            user_name = serializer.validated_data["user_name"]
            if user_name in RECOVERY_CODES and RECOVERY_CODES[user_name] == recovery_code:
                return Response({"message": "Code validated successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid recovery code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import logging

logger = logging.getLogger(__name__)

class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info(f"Received data: {request.data}")
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_name = request.data.get("user_name")
            if user_name in RECOVERY_CODES:  # Ensure user validated the code
                try:
                    user = Users.objects.get(user_name=user_name)
                    logger.info(f"Changing password for user: {user_name}")
                    user.set_password(serializer.validated_data["password"])
                    user.save()
                    del RECOVERY_CODES[user_name]  # Remove code after success
                    return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
                except Users.DoesNotExist:
                    logger.error(f"User not found: {user_name}")
                    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            logger.error(f"No validated recovery code found for user: {user_name}")
            return Response({"error": "No validated recovery code found for user."}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UniqueLineChart(Drawing):
    def __init__(self, width=400, height=200, data=None, colors=None, title=""):
        super().__init__(width, height)

        # Create and configure LinePlot
        line_chart = LinePlot()
        line_chart.x = 50
        line_chart.y = 50
        line_chart.height = 150
        line_chart.width = 300

        # Assign data to LinePlot
        line_chart.data = data or []
        line_chart.lines[0].strokeColor = colors[0] if colors else colors.blue
        line_chart.lines[0].symbol = makeMarker("Circle")
        if len(line_chart.data) > 1:
            line_chart.lines[1].strokeColor = colors[1] if len(colors) > 1 else colors.red
            line_chart.lines[1].symbol = makeMarker("Square")

        # Configure x-axis to show dates
        line_chart.xValueAxis.labelTextFormat = lambda x: datetime.fromordinal(int(x)).strftime('%Y-%m-%d')
        line_chart.xValueAxis.forceZero = False  # Avoid forcing axis to start at zero

        # Configure y-axis to show only actual data values
        if data and data[0]:
            y_values = [point[1] for series in data for point in series]
            line_chart.yValueAxis.valueMin = min(y_values) * 0.9  # Add 10% padding below
            line_chart.yValueAxis.valueMax = max(y_values) * 1.1  # Add 10% padding above
            line_chart.yValueAxis.valueStep = (line_chart.yValueAxis.valueMax - line_chart.yValueAxis.valueMin) / 5
        else:
            line_chart.yValueAxis.valueMin = 0
            line_chart.yValueAxis.valueMax = 100
            line_chart.yValueAxis.valueStep = 100

        line_chart.yValueAxis.labelTextFormat = lambda y: f"${y:.2f}"
        
        # Add LinePlot to Drawing
        self.add(line_chart)

        if title:
            self.add(String(width / 2, height - 10, title, textAnchor="middle", fontSize=12))
    

threads = {}
class IncomeExpensePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def convert_to_seconds(self, interval, unit):
        units_in_seconds = {
            "seconds": 1,
            "minutes": 60,
            "hours": 3600,
            "days": 86400,
            "months": 2592000,  # Approximate value: 30 days
        }
        return interval * units_in_seconds.get(unit, 1)
    
    def generate_pdf(self, user_id):
        user = Users.objects.get(pk=user_id)
        # Fetch incomes and expenses with categories
        incomes = Incomes.objects.filter(user = user)
        serialized_incomes = IncomeSerializer(incomes, many=True).data

        expenses = Expenses.objects.filter(user=user)
        serialized_expenses = ExpenseSerializer(expenses, many=True).data 

        # Aggregated data for line charts
        incomes_grouped_by_date = (
            Incomes.objects.filter(user=user)
            .values("date")
            .annotate(total_amount=Sum("amount"))
            .order_by("date")
        )

        expenses_grouped_by_date = (
            Expenses.objects.filter(user=user)
            .values("date")
            .annotate(total_amount=Sum("amount"))
            .order_by("date")
        )

        # Prepare data for tables
        income_table_data = [["Date", "Categories", "Amount"]]
        expense_table_data = [["Date", "Categories", "Amount"]]
        income_pie_data = defaultdict(float)  # Default to 0 for aggregation
        expense_pie_data = defaultdict(float)

        # Process incomes
        for income in serialized_incomes:
            categories = income["categories"] or ["Uncategorized"]  
            categories = sorted(categories)
            concatenated_categories = ", ".join(categories)

            #update data
            income_table_data.append([income["date"], concatenated_categories, float(income["amount"])])
            income_pie_data[concatenated_categories] += float(income["amount"])

        # Process expenses, i threat the expenses categories as a single string
        for expense in serialized_expenses:
            categories = expense["categories"] or ["Uncategorized"]  
            categories = sorted(categories)
            concatenated_categories = ", ".join(categories)

            #updating data
            expense_table_data.append([expense["date"], concatenated_categories, float(expense["amount"])])
            expense_pie_data[concatenated_categories] += float(expense["amount"])
        

        # Prepare line chart data
        income_line_data = [(income["date"].toordinal(), float(income["total_amount"])) for income in incomes_grouped_by_date]
        expense_line_data = [(expense["date"].toordinal(), float(expense["total_amount"])) for expense in expenses_grouped_by_date]

        # Create the PDF response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="income_expense_report.pdf"'
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []

        # Add title
        elements.append(
            Table([["Income and Expense Report"]], style=[("ALIGN", (0, 0), (-1, -1), "CENTER")])
        )
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Spacer(1, 0.5 * inch))

        # Add income table
        col_widths = [100, 200, 100]
        income_table = Table(income_table_data, colWidths= col_widths)
        income_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ])
        )
        elements.append(Table([["Incomes"]], style=[("ALIGN", (0, 0), (-1, -1), "LEFT")]))
        elements.append(Spacer(1, 3))
        elements.append(income_table)
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(UniqueLineChart(data=[income_line_data], colors=[colors.green], title="Chart: Income Over Time"))
        elements.append(Spacer(1, 0.8 * inch))
        # Add pie chart for income categories
        income_pie_chart = Drawing(400, 200)
        income_pie = Pie()
        income_pie.x = 100
        income_pie.y = 0
        income_pie.width = 200  # Increase the width
        income_pie.height = 200  # Increase the height
        income_pie.data = list(income_pie_data.values())
        income_pie.labels = list(income_pie_data.keys())
        income_pie_chart.add(income_pie)

        # Create a table with the title and chart
        chart_table_data1 = [
            ["Income Categories"],  # Title
            [income_pie_chart]      # Pie chart
        ]

        # Define the table with alignment and styling
        chart_table1 = Table(chart_table_data1, colWidths=[400])  # Adjust width as needed
        chart_table1.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),  # Center the title
                ("ALIGN", (0, 1), (-1, -1), "CENTER"), # Center the chart
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for title
                ("FONTSIZE", (0, 0), (-1, 0), 14),  # Font size for title
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),  # Padding below title
            ])
        )

        # Append the table to the elements
        elements.append(chart_table1)

        elements.append(Spacer(1, 0.5 * inch))


        # Add expense table and add expense line chart
        expense_table = Table(expense_table_data, colWidths=col_widths)
        expense_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ])
        )
        elements.append(Table([["Expenses"]], style=[("ALIGN", (0, 0), (-1, -1), "CENTER")]))
        elements.append(expense_table)
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(UniqueLineChart(data=[expense_line_data], colors=[colors.red], title="Chart: Expenses Over Time"))
        elements.append(Spacer(1, 0.5 * inch)) 

        # Create the pie chart for expenses and categories
        expense_pie_chart = Drawing(400, 230)
        expense_pie = Pie()
        expense_pie.x = 100  # Center horizontally within the Drawing
        expense_pie.y = 0   # Leave space for the title
        expense_pie.width = 200
        expense_pie.height = 200
        expense_pie.data = list(expense_pie_data.values())
        expense_pie.labels = list(expense_pie_data.keys())
        expense_pie_chart.add(expense_pie)

        # Create a table with the title and chart
        chart_table_data = [
            ["Expense Categories"],  # Title
            [expense_pie_chart]      # Pie chart
        ]

        # Define the table with alignment and styling
        chart_table = Table(chart_table_data, colWidths=[400])  # Adjust width as needed
        chart_table.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),  # Center the title
                ("ALIGN", (0, 1), (-1, -1), "CENTER"), # Center the chart
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for title
                ("FONTSIZE", (0, 0), (-1, 0), 14),  # Font size for title
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),  # Padding below title
            ])
        )

        # Append the table to the elements
        elements.append(chart_table)

        # Build and return the PDF
        doc.build(elements)
        return response
    
    # the next steps on these code is to make it for one mont and in an specific hour
    # like been able to now if a mont has happend, and if so
    # been able to now the exact time and set it
    def periodic_email_task(self, interval, stop_event, user_id):
        sleep_interval = 0.5
        elapsed_time = interval

        while not stop_event.is_set():
            if elapsed_time >= interval:
                try:
                    # Fetch the latest user data
                    user = Users.objects.get(pk=user_id)
                    email = user.email

                    # Generate PDF in-memory
                    pdf_buffer = BytesIO()
                    response = self.generate_pdf(user_id)
                    pdf_buffer.write(response.content)
                    pdf_buffer.seek(0)

                    email_message = EmailMessage(
                        subject="Periodic Income and Expense Report",
                        body="Hello,\n\nPlease find attached your income and expense report.\n\nBest regards.",
                        from_email=None,
                        to=[email],
                    )
                    email_message.attach("income_expense_report.pdf", pdf_buffer.getvalue(), "application/pdf")
                    email_message.send()

                    pdf_buffer.close()
                    print(f"Email sent to {email}")
                except ObjectDoesNotExist:
                    # If the user does not exist, stop the thread
                    print(f"User {user_id} does not exist. Stopping email task.")
                    stop_event.set()  # Stop the thread
                    break
                except Exception as e:
                    print(f"Error sending email to {email}: {e}")

                elapsed_time = 0
            
            time.sleep(sleep_interval)
            elapsed_time += sleep_interval

    def start_email_task(self, request):
        # Get interval and unit from query parameters
        interval = int(request.GET.get("interval", 60))  # Default interval: 60 seconds
        unit = request.GET.get("unit", "seconds")  # Default unit: seconds
        user_id = request.user.id

        interval_in_seconds = self.convert_to_seconds(interval, unit)

        if user_id in threads:
            threads[user_id]["stop_event"].set()
            threads[user_id]["thread"].join(timeout=1) 
            del threads[user_id]

        stop_event = Event()
        thread = Thread(target=self.periodic_email_task, args=(interval_in_seconds, stop_event, user_id))
        thread.daemon = True
        thread.start()

        threads[user_id] = {"thread": thread, "stop_event": stop_event}
        return JsonResponse({"message": f"Periodic email task started successfully for {interval} {unit}."})
    
    def stop_email_task(self, request):
        user_id = request.user.id

        if user_id in threads:
            threads[user_id]["stop_event"].set()
            threads[user_id]["thread"].join(timeout=1)
            del threads[user_id]
            return JsonResponse({"message": "Periodic email task stopped successfully."})
        return JsonResponse({"error": "No running task found for this email."}, status=404)
    
    def get(self, request):
        action = request.GET.get("action", "start")  # Action (start or stop) from query parameters
        if action == "start":
            return self.start_email_task(request)
        elif action == "stop":
            return self.stop_email_task(request)
        return JsonResponse({"error": "Invalid action."}, status=400)
    