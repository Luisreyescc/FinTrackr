import random
import time
import pytz
from io import BytesIO
from datetime import datetime, timedelta
from collections import defaultdict
from threading import Event, Thread

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status


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
from .serializers import SendCodeSerializer, ValidateCodeSerializer, ChangePasswordSerializer, RegisterSerializer

# Recovery password views
RECOVERY_CODES = {}

class CheckUserEmailAssociationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_name = request.data.get("user_name")
        email = request.data.get("email")
        
        try:
            user = Users.objects.get(user_name=user_name, email=email)
            return Response({"message": "Username and email are associated."}, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({"error": "Username and email are not associated."}, status=status.HTTP_400_BAD_REQUEST)

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
                    message=(
                        f"Hello {user_name},\n\n"
                        "We received a request to reset your password. Please use the following recovery code to reset your password:\n\n"
                        f"Recovery Code: {code}\n\n"
                        "If you did not request a password reset, please ignore this email or contact support.\n\n"
                        "Best regards,\n"
                        "The FinTrackr Team"
                    ),
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


# Register view
RECOVERY_CODES_SIGN = {}

class CheckAvailabilityView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_name = request.data.get("user_name")
        email = request.data.get("email")
        
        if Users.objects.filter(user_name=user_name).exists():
            return Response({"error": "Username is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        if Users.objects.filter(email=email).exists():
            return Response({"error": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Username and email are available."}, status=status.HTTP_200_OK)

class SendCodeSignView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data["user_name"]
            email = serializer.validated_data["email"]
            try:
                code = str(random.randint(100000, 999999)) 
                RECOVERY_CODES_SIGN[user_name] = code
                send_mail(
                    subject="Account Verification Code",
                    message=(
                        f"Hello {user_name},\n\n"
                        "Thank you for signing up for FinTrackr! To complete your registration, please use the following verification code:\n\n"
                        f"Verification Code: {code}\n\n"
                        "Enter this code in the application to verify your account and start using FinTrackr.\n\n"
                        "If you did not sign up for a FinTrackr account, please ignore this email or contact our support team.\n\n"
                        "Best regards,\n"
                        "The FinTrackr Team"
                    ),
                    from_email=None,
                    recipient_list=[email],
                )
                return Response({"message": "Verification code sent successfully."}, status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                return Response({"error": "User with provided details not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateCodeSignView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ValidateCodeSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data['user_name']
            recovery_code = serializer.validated_data['recovery_code']
            if user_name in RECOVERY_CODES_SIGN and RECOVERY_CODES_SIGN[user_name] == recovery_code:
                return Response({"message": "Code validated successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid recovery code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_mail(
            subject="Welcome to FinTrackr",
            message=(
                "Welcome to FinTrackr!\n\n"
                "We're excited to have you on board. FinTrackr is your go-to solution for managing your finances safely, quickly, and easily. "
                "With our platform, you can keep track of your income and expenses and gain insights into your spending habits.\n\n"
                "Here are some features you can start exploring:\n"
                "- Track your income and expenses\n"
                "- Generate detailed financial reports\n"
                "Thank you for choosing FinTrackr. We're here to help you achieve your financial goals!\n\n"
                "Best regards,\n"
                "The FinTrackr Team"
            ),
            from_email=None,
            recipient_list=[user.email],
        )

# Edit profile view
class CheckAvailabilityForEditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.user_id
        user_name = request.data.get("user_name")
        email = request.data.get("email")
        
        if Users.objects.filter(user_name=user_name).exclude(user_id=user_id).exists():
            return Response({"error": "Username is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        if Users.objects.filter(email=email).exclude(user_id=user_id).exists():
            return Response({"error": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Username and email are available."}, status=status.HTTP_200_OK)

# PDF view
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
        # Calculate the start and end date for the last month
        now = datetime.now()
        one_month_ago = now - timedelta(days=30)

        user = Users.objects.get(pk=user_id)

        # Fetch incomes and expenses with categories for the last month
        incomes = Incomes.objects.filter(user = user, date__gte=one_month_ago)
        serialized_incomes = IncomeSerializer(incomes, many=True).data

        expenses = Expenses.objects.filter(user=user, date__gte=one_month_ago)
        serialized_expenses = ExpenseSerializer(expenses, many=True).data 

        # Calculate the sum of all incomes manually
        total_income = sum(float(income["amount"]) for income in serialized_incomes)

        # Calculate the sum of all expenses manually
        total_expense = sum(float(expense["amount"]) for expense in serialized_expenses)

        # Aggregated data for line charts
        incomes_grouped_by_date = (
            Incomes.objects.filter(user=user, date__gte=one_month_ago)
            .values("date")
            .annotate(total_amount=Sum("amount"))
            .order_by("date")
        )

        expenses_grouped_by_date = (
            Expenses.objects.filter(user=user, date__gte=one_month_ago)
            .values("date")
            .annotate(total_amount=Sum("amount"))
            .order_by("date")
        )

        # Prepare data for tables
        income_table_data = [["Date", "Categories", "Amount"]]
        expense_table_data = [["Date", "Categories", "Amount"]]
        income_pie_data = defaultdict(float)  # Default to 0 for aggregation
        expense_pie_data = defaultdict(float)

        if serialized_incomes: 
            # Process incomes
            for income in serialized_incomes:
                categories = income["categories"] or ["Uncategorized"]  
                categories = sorted(categories)
                concatenated_categories = ", ".join(categories)

                #update data
                income_table_data.append([income["date"], concatenated_categories, float(income["amount"])])
                income_pie_data[concatenated_categories] += float(income["amount"])
        
        else:
            income_table_data.append(["No data available", "-", "-"])

        if serialized_expenses:
            # Process expenses, i threat the expenses categories as a single string
            for expense in serialized_expenses:
                categories = expense["categories"] or ["Uncategorized"]  
                categories = sorted(categories)
                concatenated_categories = ", ".join(categories)

                #updating data
                expense_table_data.append([expense["date"], concatenated_categories, float(expense["amount"])])
                expense_pie_data[concatenated_categories] += float(expense["amount"])
        
        else:
            expense_table_data.append(["No data available", "-", "-"])

        # Prepare line chart data
        income_line_data = []
        for income in incomes_grouped_by_date:
            try:
                date_ordinal = income["date"].toordinal()
                income_line_data.append((date_ordinal, float(income["total_amount"])))
            except (ValueError, TypeError):
                continue  # Skip invalid or missing dates

        expense_line_data = []
        for expense in expenses_grouped_by_date:
            try:
                date_ordinal = expense["date"].toordinal()
                expense_line_data.append((date_ordinal, float(expense["total_amount"])))
            except (ValueError, TypeError):
                continue  # Skip invalid or missing dates

        # Handle empty line data
        if not income_line_data:
            income_line_data = [(datetime.now().toordinal(), 0.1)]  

        if not expense_line_data:
            expense_line_data = [(datetime.now().toordinal(), 0.1)]  

        # Handle single-point data
        if len(income_line_data) == 1:
            single_point = income_line_data[0]
            income_line_data.append((single_point[0] + 1, single_point[1]))  # Add a dummy point

        if len(expense_line_data) == 1:
            single_point = expense_line_data[0]
            expense_line_data.append((single_point[0] + 1, single_point[1]))  # Add a dummy point

        # Debug output
        print("Final Income Line Data:", income_line_data)
        print("Final Expense Line Data:", expense_line_data)

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
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Spacer(1, 0.5 * inch))
        
        # Create tables for total incomes, total expenses, and balance
        total_income_table = Table([[f"Total incomes: {total_income}"]], colWidths=[500])  # Set table width explicitly
        total_income_table.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Align content to the left
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black)  # Optional: Set text color
            ])
        )

        total_expense_table = Table([[f"Total expenses: {total_expense}"]], colWidths=[500])
        total_expense_table.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black)
            ])
        )

        balance_table = Table([[f"Balance: {total_income - total_expense}"]], colWidths=[500])
        balance_table.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black)
            ])
        )

        # Add tables to elements
        elements.append(total_income_table)
        elements.append(total_expense_table)
        elements.append(balance_table)

        # Build and return the PDF
        doc.build(elements)
        return response
    

    def periodic_email_task(self, stop_event, user_id, first, months, day, hour, minute):
        sleep_interval = 0.5
        

        while not stop_event.is_set():
            now = datetime.now(pytz.timezone('America/Mexico_City'))  # Here we fix the hour and the date for our country;
            
            if (now.month in months and now.day == day and now.hour == hour and now.minute == minute and now.second == 00) or (first == 0):
                first = 1
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
                        body=(
                            f"Hello {user.user_name},\n\n"
                            "Attached is your periodic income and expense report. This report provides a detailed overview of your financial activities, "
                            "including a breakdown of your incomes and expenses by category, as well as visual charts to help you understand your financial trends.\n\n"
                            "If you have any questions or need further assistance, please do not hesitate to contact our support team.\n\n"
                            "Best regards,\n"
                            "The FinTrackr Team"
                        ),
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
            
            time.sleep(sleep_interval)

    def start_email_task(self, request):
        # Get interval and unit from query parameters
        interval = int(request.GET.get("interval", 1))
        first = int(request.GET.get("first", 0))
        day = int(request.GET.get("day", 1))
        hour = int(request.GET.get("hour", 0))
        minute = int(request.GET.get("minute", 0))
        user_id = request.user.id

        if user_id in threads:
            threads[user_id]["stop_event"].set()
            threads[user_id]["thread"].join(timeout=1) 
            del threads[user_id]

        months = []
        current_month = datetime.now(pytz.timezone('America/Mexico_City')).month
        while len(months) < 12 // interval:
            months.append(current_month)
            current_month = (current_month + interval - 1) % 12 + 1

        print(f"Email configured to the monts: {months} \nThe day: {day} \nThe hour: {hour} \nThe minute: {minute}")

        stop_event = Event()
        thread = Thread(target=self.periodic_email_task, args=(stop_event, user_id, first, months, day, hour, minute))
        thread.daemon = True
        thread.start()

        threads[user_id] = {"thread": thread, "stop_event": stop_event}
        return JsonResponse({"message": f"Periodic email task started successfully for {interval} {day} : {hour}.{minute}."})
    
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
    