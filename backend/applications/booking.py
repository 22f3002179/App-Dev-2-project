from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required,get_jwt
from applications.model import db,Professional,Customer,Admin,Service,Main_Services,ServiceBooking
from flask import request
from flask.views import MethodView
from applications.task import *
from datetime import date
import re

def get_booking_by_id(booking_id):
    booking = ServiceBooking.query.get(booking_id)
    if booking:
        return {
            "booking_id": booking.booking_id,
            "date_of_request": str(booking.date_of_request),
            "date_of_completion": booking.date_of_completion,
            "phone_number": booking.phone_number,
            "status": booking.status,
            "location": booking.location,
            "pincode": booking.pincode,
            "rating": booking.rating,
            "professional_id": booking.professional_id,
            "customer_id": booking.customer_id,
            "service_id": booking.service_id
        }
    return None

def get_all_bookings(customer_id=None):
    if customer_id:
        bookings = ServiceBooking.query.filter_by(customer_id=customer_id).all()
    else:
        bookings = ServiceBooking.query.all()
    return [{
        "booking_id": b.booking_id,
        "date_of_request": str(b.date_of_request),
        "date_of_completion": b.date_of_completion,
        "phone_number": b.phone_number,
        "status": b.status,
        "location": b.location,
        "pincode": b.pincode,
        "rating": b.rating,
        "professional_id": b.professional_id,
        "customer_id": b.customer_id,
        "service_id": b.service_id
    } for b in bookings] 
class bookingAPI(MethodView):
    def get(self, booking_id=None):
        try:
            customer_id = request.args.get('customer_id', type=int)  # Get customer_id from query parameters
            if booking_id:
                booking = get_booking_by_id(booking_id)
                if booking:
                    return booking, 200
                return {"message": "Booking not found"}, 404
            # Fetch all bookings or those filtered by customer_id
            bookings = get_all_bookings(customer_id)
            return bookings, 200
        except Exception as e:
            return {"message": f"Internal server error: {str(e)}"}, 500

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')
        if role != 'customer':
            return {'message': 'You do not have permission'}, 403
        data = request.json
        required_fields = ['phone_number', 'location', 'pincode', 'service_id']
        if not all(field in data for field in required_fields):
            return {'message': 'Bad request! All required fields must be provided.'}, 400
        if not re.fullmatch(r'^\d{10}$', data['phone_number']):
         return {'message': 'Invalid phone number. It must be exactly 10 digits.'}, 400
        if not re.fullmatch(r'^\d{6}$', data['pincode']):
         return {'message': 'Invalid pincode. It must be exactly 6 digits.'}, 400
        customer = Customer.query.filter_by(email_id=current_user).first()
        if not customer:
           return {'message': 'Customer not found!'}, 404
        
        new_booking = ServiceBooking(
            date_of_request=date.today(),
            phone_number=data['phone_number'],
            location=data['location'],
            pincode=data['pincode'],
            service_id=data['service_id'],
            customer_id=customer.Customer_id,
            status='requested'
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        return {'message': 'Booking created successfully.', 'booking_id': new_booking.booking_id}, 201


    def put(self, booking_id):
        booking = ServiceBooking.query.get(booking_id)
        
        if not booking:
            return {'message': 'Booking not found.'}, 404
        
        data = request.json
        
        
        if 'phone_number' in data:
            if not re.fullmatch(r'^\d{10}$', data['phone_number']):
               return {'message': 'Invalid phone number. It must be exactly 10 digits.'}, 400
            booking.phone_number = data['phone_number']
        if 'location' in data:
            booking.location = data['location']
        if 'pincode' in data:
         if not re.fullmatch(r'^\d{6}$', data['pincode']):
          return {'message': 'Invalid pincode. It must be exactly 6 digits.'}, 400
         booking.pincode = data['pincode']
        if 'rating' in data:
            booking.rating = data['rating']
        if 'status' in data:
            booking.status = data['status']
        if 'professional_id' in data:
            booking.professional_id = data['professional_id']
        if 'date_of_completion' in data:
            booking.date_of_completion = data['date_of_completion']
        db.session.commit()
        return {'message': 'Booking updated successfully.'}, 200

    @jwt_required()
    def delete(self, booking_id):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')
        if role != 'customer':
            return {'message': 'You do not have permission'}, 403
        booking = ServiceBooking.query.get(booking_id)
        
        if not booking:
            return {'message': 'Booking not found.'}, 404
        
        customer = Customer.query.filter_by(email_id=current_user).first()
        if not customer:
           return {'message': 'Customer not found!'}, 404
        
        if booking.customer_id != customer.Customer_id:
          return {'message': 'Access denied.'}, 403
        
        db.session.delete(booking)
        db.session.commit()
        
        return {'message': 'Booking deleted successfully.'}, 200