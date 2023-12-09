import unittest
from datetime import datetime
from CarAppointment import Vehicle, Customer, CustomerList, Appointment, AppointmentQueue


# Final Project Test Page, Not as much coverage, on time crunch
class TestVehicle(unittest.TestCase):
    # Tests creation of vehicle
    def test_vehicle_creation(self):

        vehicle = Vehicle("silver", "ford", "focus", 2010, "coolant leak")

        self.assertIsNotNone(vehicle)
        self.assertEqual("Silver", vehicle.color)
        self.assertEqual("Ford", vehicle.make)
        self.assertEqual("Focus", vehicle.model)
        self.assertEqual(2010, vehicle.year)
        self.assertEqual("coolant leak", vehicle.note)

    # Tests to make sure note is properly update
    def test_update_note(self):

        vehicle = Vehicle("silver", "ford", "focus", 2010, "coolant leak")

        vehicle.update_note("oil change")
        self.assertEqual("oil change", vehicle.note)


# Customer Class Testing
class TestCustomer(unittest.TestCase):

    # Tests Customer Creation
    def test_customer_creation(self):

        vehicle = Vehicle("silver", "ford", "focus", 2010, "coolant leak")
        customer = Customer("sarah", "smith", "5554441111", "saras@gmail.com", vehicle)

        self.assertIsNotNone(customer)
        self.assertEqual("Sarah", customer.fname)
        self.assertEqual("Smith", customer.lname)
        self.assertEqual("(515)444-1111", customer.phone)
        self.assertEqual("saras@gmail.com", customer.email)
        self.assertEqual(vehicle, customer.vehicle)

    # Test to make sure phone gets updated with proper format
    def test_update_phone(self):

        vehicle = Vehicle("silver", "ford", "focus", 2010, "coolant leak")
        customer = Customer("sarah", "smith", "5554441111", "saras@gmail.com", vehicle)

        customer.update_phone("2225550000")
        self.assertEqual("(222)555-0000", customer.phone)

    # Test to make sure email gets updated
    def test_update_email(self):

        vehicle = Vehicle("silver", "ford", "focus", 2010, "coolant leak")
        customer = Customer("sarah", "smith", "5554441111", "saras@gmail.com", vehicle)

        customer.update_email("ssmith@example.com")
        self.assertEqual("ssmith@example.com", customer.email)


# Appointment Class Test
class TestAppointment(unittest.TestCase):

    # Tests Appointment Creation
    def test_appointment_creation(self):

        vehicle = Vehicle("silver", "ford", "focus", 2010, "coolant leak")
        customer = Customer("sarah", "smith", "5554441111", "saras@gmail.com", vehicle)
        appointment = Appointment(customer, "2023-12-29", "11:00")

        self.assertIsNotNone(appointment)
        self.assertEqual(customer, appointment.customer)
        self.assertEqual("2023-12-29", appointment.date)
        self.assertEqual("11:00", appointment.time)


# Appointment Queue Test
class TestAppointmentQueue(unittest.TestCase):

    # Tests Adding to the Queue
    def test_add_appointment(self):
        customer_list = CustomerList()
        appointment_queue = AppointmentQueue(customer_list)

        vehicle = Vehicle("silver", "ford", "focus", 2010, "coolant leak")
        customer = Customer("sarah", "smith", "5554441111", "saras@gmail.com", vehicle)
        appointment = Appointment(customer, "2023-12-29", "11:00")

        appointment_queue.add_appointment(appointment)
        self.assertEqual(1, appointment_queue.get_length())

        appointment_queue.remove_appointment_by_name("sarah", "smith")
        self.assertEqual(0, appointment_queue.get_length())
