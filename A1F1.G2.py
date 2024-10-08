import time

class Route:
    def __init__(self, number, route_name, price, discount, bus_type, max_regular_seat, max_member_seat):
        # Public attribute
        self.number = number 
        self.route_name = route_name 
        self.price = price 
        self.discount = discount
        self.bus_type = bus_type   
        self.max_regular_seat = max_regular_seat
        self.max_member_seat = max_member_seat 
        
        # Private attributes (for internal calculations)
        # For updating seats for regular and reserve
        self._regular_seats_booked = 0 # Tracks regular seats book and update max seats
        self._member_seats_booked = 0 # Tracks reserve seats book and update max seats
        # For tracking amount of tickets booked by member or non-member
        self._total_regular_seats_booked = 0 # Tracks how many non-member booking has been made
        self._total_member_seats_booked = 0 # Tracks how many member booking has been made
        # For tracking total sales of member and non-member
        self._regular_total_sales = 0.0 # Tracks non-member sales
        self._member_total_sales = 0.0 # Tracks member sales

        # Private attributes to keep a copy of max seats
        self._total_max_seats = self.max_regular_seat + self.max_member_seat
        
    # Booking Function
    def book_seats(self, user_type, seats):
        # Handles both member and non-member booking
        # Checks for errors - user input negative or zero
        if seats <= 0:
            print("ERROR! Number of seats must be greater than zero.")
            return

        # Add a variable to track available seats in the system
        total_available_seats = self.max_regular_seat + self.max_member_seat

        if user_type == "yes":  # Member booking
            # Initialize discounted tickets
            price_after_discount = self.price * (1 - self.discount / 100)
            
            if seats <= total_available_seats:  # Check total available seats
                if seats <= self.max_regular_seat:  # Book regular seats first
                    # Update regular seats availability
                    self.max_regular_seat -= seats 
                    self._regular_seats_booked += seats
                    self._total_member_seats_booked += seats # Keep track of member total booking
                    # Update price
                    total_cost = seats * price_after_discount
                    self._member_total_sales += total_cost # Keep track of member total cost

                    booking_outline()
                    print(f"Booking Successful for {self.route_name}!")
                    print(f"Member booking: {seats} seat(s)\nTotal cost: RM {total_cost:.2f}")
                    booking_outline()
                else:
                    # Books regular and reserve seats
                    # Process to check if remaining seats are in range of reserve seat availability
                    regular_booked = self.max_regular_seat
                    remaining_seats = seats - regular_booked

                    # Book remaining from member seats
                    if remaining_seats <= self.max_member_seat:
                        # Update regular and member seats availability
                        self.max_regular_seat = 0 # Update regular seats to 0
                        self.max_member_seat -= remaining_seats # Update member seats availability
                        # Update seats availability for regular and reserve
                        self._regular_seats_booked += regular_booked
                        self._member_seats_booked += remaining_seats
                        # Update price
                        total_cost = (regular_booked * price_after_discount) + (remaining_seats * price_after_discount)
                        self._member_total_sales += total_cost
                        self._total_member_seats_booked += seats # Keep track of member total booking

                        booking_outline()
                        print(f"Booking Successful for {self.route_name}!")
                        print(f"Member booking: {regular_booked + remaining_seats} seat(s)")
                        print(f"Total cost: RM {total_cost:.2f}")
                        booking_outline()
            
            # Checks for errors - if user input is greater than max seat for route
            elif seats > self._total_max_seats:
                print(f"ERROR! Cannot over book max seats available for {self.route_name}.")
            else:
                print("ERROR! Not enough regular and reserve seats available.")

        else:  # Non-member booking
            if seats <= self.max_regular_seat:  # Only regular seats for non-members
                self.max_regular_seat -= seats # Update regular seats availability
                total_cost = seats * self.price
                self._regular_seats_booked += seats
                self._regular_total_sales += total_cost
                self._total_regular_seats_booked += seats # Keep track of non-member total bookings

                booking_outline()
                print(f"Booking Successful for {self.route_name}!")
                print(f"Non-member booking: {seats} seat(s)\nTotal cost: RM {total_cost:.2f}")
                booking_outline()

            # Checks for errors - if user input is greater than max seat for route
            elif seats > self._total_max_seats:
                print(f"ERROR! Cannot over book max seats available for {self.route_name}.")
            else:
                print("ERROR! Not enough regular seats available. Non-members cannot book reserve seats.")

    # Cancel Seat Function
    def cancel_seats(self, user_type, seats):
        # Handles both member and non-member cancellations
        # Variable to track total booked seats 
        total_booked = self._member_seats_booked + self._regular_seats_booked
        
        # Checks for errors - user input negative or zero
        if seats <= 0:
            print("ERROR! Number of seats to cancel must be greater than zero.")
            system_timer()
            return

        if user_type == "yes":  # Member cancellation

            # Checks if seats are available to cancel based on amount of total member bookings
            if seats <= self._total_member_seats_booked:
                
                # Initialize refund for members
                refund_amount = 0.0
                price_after_discount = self.price * (1 - self.discount / 100)

                # Cancel and update reserve seats before regular seat
                if seats <= self._member_seats_booked:
                    # Update the reserve seats
                    self._member_seats_booked -= seats 
                    self.max_member_seat += seats
                    refund_amount = seats * price_after_discount
                else:
                    # First - Cancel all reserve seats
                    member_cancelled = self._member_seats_booked
                    # Update reserve seats
                    self._member_seats_booked = 0 
                    self.max_member_seat += member_cancelled
                    refund_amount = member_cancelled * price_after_discount

                    # Second - Cancel the remaining seats from regular seats
                    remaining_seats = seats - member_cancelled
                    # Update regular seats
                    self._regular_seats_booked -= remaining_seats
                    refund_amount += remaining_seats * price_after_discount
                    self.max_regular_seat += remaining_seats

                self._total_member_seats_booked -= seats # Update total member bookings
                self._member_total_sales -= refund_amount

                cancel_outline()
                print(f"Cancel Booking Successful for {self.route_name}!")
                print(f"Member cancellation: {seats} seat(s)\nRefund amount: RM {refund_amount:.2f}")
                cancel_outline()
                system_timer()

            # Checks for error
            elif total_booked == 0: # Checks if any bookings has been made for route
                print(f"ERROR! No sales have been made for {self.route_name}. Cannot cancel.")
                system_timer()
            elif seats > self._total_max_seats: # User input is greater than max seat for route
                print(f"ERROR! Cannot over cancel max seats available for {self.route_name}.")
                system_timer()
            else:
                print("ERROR! Not enough seats booked to cancel for member.")
                system_timer()
                
        else:  # Non-member cancellation
            # Checks if seats are available to cancel based on amount of total non-member bookings
            if seats <= self._total_regular_seats_booked:
                # Update regular seats
                self._regular_seats_booked -= seats
                self.max_regular_seat += seats
                self._total_regular_seats_booked -= seats # Update total seats of non-member
                refund_amount = seats * self.price
                self._regular_total_sales -= refund_amount

                cancel_outline()
                print(f"Cancel Booking Successful for {self.route_name}!")
                print(f"Non-member cancellation: {seats} seat(s)\nRefund amount: RM {refund_amount:.2f}")
                cancel_outline()
                system_timer()

            # Check for errors
            elif total_booked == 0: # Checks if any bookings has been made for route
                print(f"ERROR! No sales have been made for {self.route_name}. Cannot cancel.")
                system_timer()
            elif seats > self._total_max_seats: # User input is greater than max seat for route
                print(f"ERROR! Cannot over cancel max seats available for {self.route_name}.")
                system_timer()
            else:
                print("ERROR! Not enough seats booked to cancel for non-member.")
                system_timer()

    # Total Seats Booked Function
    def total_seats_booked(self):
        return self._regular_seats_booked + self._member_seats_booked

    # Total Sales Function
    def total_sales(self):
        return self._regular_total_sales + self._member_total_sales
    
# Creating an instance for all the routes
ipoh_route = Route(1, "Ipoh", 49.70, 10, "Platinum", 31, 4)
melaka_route = Route(2, "Melaka", 39.80, 5, "Express", 42, 0)
johor_route = Route(3, "Johor", 66.60, 10, "Platinum", 31, 4)
penang_route = Route(4, "Penang", 58.30, 5, "Express", 42, 0 )
singapore_route = Route(5, "Singapore", 98.90, 15, "Business", 24, 5)

# Other variables for the system
is_running = True # Helps loops the main system
is_booking = True # Helps loops the booking system
system_time = 3 # Predefined time

# System Functions
# Output Display of Bus Menu Choice for the user
def bus_menu_user():
    print("Bus Booking System Menu")
    print("1. View Available Routes")
    print("2. Book a Seat")
    print("3. Cancel a Booking")
    print("4. End of Day Report")
    print("5. Exit")

# Output Display Categories Title of Bus Booking System
def bus_route_title():
    print(
        f"{'No.':<5}{'Route':<10}{'Price (Regular)':>15}"
        f"{'Discount (Member)':>20}{'Bus Type':>15}"
        f"{'Regular Seats':>20}{'Reserve Seats':>20}"
    )

# Output of Route Information for Bus Booking System
def route_display_menu():
    bus_route_title()
    print(
        f"{ipoh_route.number:<5}{ipoh_route.route_name:<10}{ipoh_route.price:>15.2f}"
        f"{ipoh_route.discount:>20}%{ipoh_route.bus_type:>15}"
        f"{ipoh_route.max_regular_seat:>20}{ipoh_route.max_member_seat:>20}"
    )
    print(
        f"{melaka_route.number:<5}{melaka_route.route_name:<10}{melaka_route.price:>15.2f}"
        f"{melaka_route.discount:>20}%{melaka_route.bus_type:>15}"
        f"{melaka_route.max_regular_seat:>20}{melaka_route.max_member_seat:>20}"
    )
    print(
        f"{johor_route.number:<5}{johor_route.route_name:<10}{johor_route.price:>15.2f}"
        f"{johor_route.discount:>20}%{johor_route.bus_type:>15}"
        f"{johor_route.max_regular_seat:>20}{johor_route.max_member_seat:>20}"
    )
    print(
        f"{penang_route.number:<5}{penang_route.route_name:<10}{penang_route.price:>15.2f}"
        f"{penang_route.discount:>20}%{penang_route.bus_type:>15}"
        f"{penang_route.max_regular_seat:>20}{penang_route.max_member_seat:>20}"
    )
    print(
        f"{singapore_route.number:<5}{singapore_route.route_name:<10}{singapore_route.price:>15.2f}"
        f"{singapore_route.discount:>20}%{singapore_route.bus_type:>15}"
        f"{singapore_route.max_regular_seat:>20}{singapore_route.max_member_seat:>20}"
    )

# Output Display of Routes to cancel 
def info_display_menu():
    info_outline()
    print(
        f"{"No.":<5}{"Route":<10}"
    )
    print(
        f"{ipoh_route.number:<5}{ipoh_route.route_name:<10}"
    )
    print(
        f"{melaka_route.number:<5}{melaka_route.route_name:<10}"
    )
    print(
        f"{johor_route.number:<5}{johor_route.route_name:<10}"
    )
    print(
        f"{penang_route.number:<5}{penang_route.route_name:<10}"
    )
    print(
        f"{singapore_route.number:<5}{singapore_route.route_name:<10}"
    )
    info_outline()

# Output Display Categories Title for Report
def title_report():
    print(
        f"{"Route":<10}"
        f"{"Regular Seats":>15}{"Reserve Seats":>15}"
        f"{"Non-Member Book":>20}{"Member Book":>15}"
        f"{"Total Seats Booked":>20}{"Total Sales (RM)":>20}"
    )

# Calculation of total sum of each routes for end of day report
def price_calculation():
    total_sales = 0  # Initialize total sales for all routes
    
    # Manually sum the total sales for each route
    total_sales += ipoh_route.total_sales()
    total_sales += melaka_route.total_sales()
    total_sales += johor_route.total_sales()
    total_sales += penang_route.total_sales()

    print(f"\nTotal sales for the day: RM {total_sales:.2f}\n")

# Output Display of End of Day Report
def end_of_day_report_display():
    report_outline()
    title_report()
    print(
        f"{ipoh_route.route_name:<10}"
        f"{ipoh_route.max_regular_seat:>15}{ipoh_route.max_member_seat:>15}"
        f"{ipoh_route._total_regular_seats_booked:>20}"
        f"{ipoh_route._total_member_seats_booked:>15}"
        f"{ipoh_route.total_seats_booked():>20}"
        f"{ipoh_route.total_sales():>20.2f}"
    )
    print(
        f"{melaka_route.route_name:<10}"
        f"{melaka_route.max_regular_seat:>15}{melaka_route.max_member_seat:>15}"
        f"{melaka_route._total_regular_seats_booked:>20}"
        f"{melaka_route._total_member_seats_booked:>15}"
        f"{melaka_route.total_seats_booked():>20}"
        f"{melaka_route.total_sales():>20.2f}"
    )
    print(
        f"{johor_route.route_name:<10}"
        f"{johor_route.max_regular_seat:>15}{johor_route.max_member_seat:>15}"
        f"{johor_route._total_regular_seats_booked:>20}"
        f"{johor_route._total_member_seats_booked:>15}"
        f"{johor_route.total_seats_booked():>20}"
        f"{johor_route.total_sales():>20.2f}"
    )
    print(
        f"{penang_route.route_name:<10}"
        f"{penang_route.max_regular_seat:>15}{penang_route.max_member_seat:>15}"
        f"{penang_route._total_regular_seats_booked:>20}"
        f"{penang_route._total_member_seats_booked:>15}"
        f"{penang_route.total_seats_booked():>20}"
        f"{penang_route.total_sales():>20.2f}"
    )
    print(
        f"{singapore_route.route_name:<10}"
        f"{singapore_route.max_regular_seat:>15}{singapore_route.max_member_seat:>15}"
        f"{singapore_route._total_regular_seats_booked:>20}"
        f"{singapore_route._total_member_seats_booked:>15}"
        f"{singapore_route.total_seats_booked():>20}"
        f"{singapore_route.total_sales():>20.2f}"
    )
    report_outline()
    price_calculation()

# System timer
def system_timer():
    for x in range(system_time, 0, -1):
        seconds = x % 60
        print(f"Returning to menu in {seconds}")
        time.sleep(1)
    print()

# Output Outline for UI:
# Bus Menu
def menu_outline():
    print("=" * 107)
# Report Menu
def report_outline():
    print("=" * 115)
# Cancel Menu
def info_outline():
    print("=" * 15)
# Successful Booking Tickets
def booking_outline():
    print("=" * 35)
# Successful Cancelling Booking Tickets
def cancel_outline():
    print("=" * 42)

# Main Program for Bus Booking System
while is_running:
    bus_menu_user()

    try:
        choice = int(input("Enter your choice: "))

        # Choice 1 - Display Available Routes for the User
        if choice == 1:
            print()
            menu_outline()
            route_display_menu()
            menu_outline()
            print()

        # Choice 2 - Booking Tickets
        elif choice == 2:
            # Booking Initialize again if booking == False 
            is_booking = True
            
            while is_booking:
                menu_outline()
                route_display_menu()
                menu_outline()
                try:
                    route_number = int(input("Enter the route number (1-5): "))

                    # Determine the selected route instance
                    if route_number == 1:
                        selected_route = ipoh_route
                    elif route_number == 2:
                        selected_route = melaka_route
                    elif route_number == 3:
                        selected_route = johor_route
                    elif route_number == 4:
                        selected_route = penang_route
                    elif route_number == 5:
                        selected_route = singapore_route

                    # Checks for route errors in booking tickets
                    elif route_number > 5:
                        print("Invalid route number.")
                        is_booking = False
                        system_timer()
                        continue
                    else:
                        print("ERROR! CANNOT BE NEGATIVE OR ZERO")
                        is_booking = False
                        system_timer()
                        continue

                    user_type = input("Are you a member? (yes/no): ").lower()

                    # Validate the user input
                    if user_type == "yes" or user_type == "no": 
                        seats = int(input("How many seats do you want to book?: "))
                        selected_route.book_seats(user_type, seats)
                    else:
                        print("ERROR! ONLY ACCEPT VALUE (yes/no)")
                        is_booking = False
                        system_timer()
                        continue

                    # Ask if the user wants to book another seat
                    while True:
                        another_booking = input("Do you want to book another seat? (yes/no): ").lower()
        
                        # Check if the input is valid
                        if another_booking == "yes":
                            print()
                            break # Exit the loop and book again
                        elif another_booking == "no":
                            print()
                            is_booking = False
                            break  # Exit the loop and return back to bus menu
                        else:
                            print("ERROR! INCORRECT INPUT! Please enter 'yes' or 'no'.")

                # Handles Value Error in Booking Function
                except ValueError:
                    print("ERROR! WRONG VALUE TYPE ENTERED!")
                    is_booking = False
                    system_timer()
                    continue

        # Choice 3 - Cancelling Booking Tickets
        elif choice == 3:
            info_display_menu()
            try:
                route_number = int(input("Enter the route number (1-5) for cancellation: "))

                # Determine the selected route instance
                if route_number == 1:
                    selected_route = ipoh_route
                elif route_number == 2:
                    selected_route = melaka_route
                elif route_number == 3:
                    selected_route = johor_route
                elif route_number == 4:
                    selected_route = penang_route
                elif route_number == 5:
                    selected_route = singapore_route

                # Checks for errors
                elif route_number > 5:
                    print("Invalid route number")
                    system_timer()
                    continue
                else:
                    print("ERROR. CANNOT BE NEGATIVE OR ZERO")
                    system_timer()
                    continue  # Continue to the next iteration of the loop

                # Prompt user if member or not
                user_type = input("Are you a member? (yes/no): ").lower()
                
                # Checks if it is a valid input
                if user_type == "yes" or user_type == "no":
                    # Prompt for the number of seats to cancel
                    seats_to_cancel = int(input("How many seats do you want to cancel?: "))
                    # Call the cancel_seats method
                    selected_route.cancel_seats(user_type,seats_to_cancel)
                else:
                    print("ERROR! ONLY ACCEPT VALUE (yes/no)")
                    system_timer()
                    continue

            # Handles Value Error during seat cancelling
            except ValueError:
                print("INVALID VALUE ENTERED!")
                system_timer()

        # Choice 4 - End of Day Report 
        elif choice == 4:
            end_of_day_report_display()

        # Choice 5 - Exit the system
        elif choice == 5:
            is_running = False

        else:
            print("ERROR! PLEASE ENTER A VALID MENU NUMBER (1-5)\n")

    # Handles Value Error in Bus Menu
    except ValueError:
        print("INVALID VALUE. PLEASE ENTER A VALID MENU NUMBER (1-5)\n")

print("Exiting the system. Goodbye!")