from celery import Celery
from celery.schedules import crontab
from applications.worker import celery
from applications.model import db, Professional,Customer,Admin,Service,Main_Services,ServiceBooking
from flask import request
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
import csv


def send_mail(email_id, subject, email_content, attachment=None):
    smtp_server_host = "localhost"
    smtp_port = 1025
    sender_email = "abc@gmain.com"
    sender_password = ""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email_id
    msg["Subject"] = subject
    msg.attach(MIMEText(email_content, "html"))

    # Attach the HTML content to the email
    msg.attach(MIMEText(email_content, "html"))
    
    # Attach file if provided
    if attachment:
        with open(attachment, "rb") as attachment_content:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_content.read())
            encoders.encode_base64(part)
            print(os.path.basename(attachment))
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
            msg.attach(part)  

    try:
        server = smtplib.SMTP(smtp_server_host, smtp_port)
        server.send_message(msg)
        server.quit()
        print("Mail sent")
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_html_report(customer,data):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", "report.html")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r") as file:
        jinja_template = Template(file.read())
        html_report =jinja_template.render(customer=customer, data=data)
        return html_report


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(10.0, daily_reminder.s(), name='daily_reminder for testing')
    #sender.add_periodic_task(10.0,  monthly_report.s(), name='monthly_report for testing')


    #Executes monthly_report at 1st day of every month
    sender.add_periodic_task(
        crontab(day_of_month='1',month_of_year='*'),
        monthly_report.s(),
        name='monthly_report at 1st day of every month'
    )
    #Executes daily_reminder at 8:00 PM
    sender.add_periodic_task(
        crontab(hour=20, minute=0),
        daily_reminder.s(),
        name='daily_reminder timed'
    )

@celery.task
def test(arg):
    print(arg)

@celery.task
def daily_reminder():
    professionals = Professional.query.all()
    for professional in professionals:
        main_service_id = professional.MainServices_id
        services = Service.query.filter_by(MainServices_id=main_service_id).all()
        service_ids = [service.service_id for service in services]
        bookings = ServiceBooking.query.filter(ServiceBooking.service_id.in_(service_ids)).all()
        requested_bookings = []
        assigned_bookings = []
        for booking in bookings:
            if booking.status == 'requested':
                requested_bookings.append(booking)
            elif booking.status == 'assigned' and booking.professional_id == professional.Professional_id:
                assigned_bookings.append(booking)

        msg= f"<h2>REMINDER: Hi {professional.full_name}, you have {len(requested_bookings)} requested bookings and {len(assigned_bookings)} assigned bookings</h2>"
        send_mail(email_id=professional.email_id, email_content=msg, subject="Daily Reminder")
    print("Daily Reminders sent at 8:00 PM.")

@celery.task
def monthly_report():
    customer = Customer.query.all()
    for customer in customer:
        bookings = ServiceBooking.query.filter_by(customer_id=customer.Customer_id).all()
        total_requested = len(bookings)
        total_closed = sum(1 for booking in bookings if booking.status == 'completed')
        total=f'Hi {customer.full_name},        Your total bookings are: {total_requested},        Your total completed bookings are: {total_closed}'
        book=[]
        book.append(total)
        for booking in bookings:
            temp=[]
            temp.append(booking.booking_id)
            temp.append(booking.date_of_request)
            temp.append(booking.date_of_completion)
            temp.append(booking.phone_number)
            temp.append(booking.location)
            temp.append(booking.pincode)
            temp.append(booking.rating)
            temp.append(booking.professional_id)
            temp.append(booking.service_id)
            temp.append(booking.status)
            book.append(temp)
        html_report = get_html_report(customer=customer.full_name, data=book)
        send_mail(email_id=customer.email_id, email_content=html_report, subject="Monthly Activity Report")
        print("Report Sent")


@celery.task
def data_export(bookings, email_id):
    with open('data_export.csv', 'w', newline='') as csvfile:
        fieldnames = ['booking_id', 'service_id', 'customer_id', 'date_of_request', 'date_of_completion', "rating","status",'location','phone_number','pincode']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bookings)
    send_mail(email_id=email_id, email_content="Please find the exported completed service requests attached.", subject="Completed Service Requests Export", attachment='data_export.csv')
    return "Completed Service Requests Exported!"
