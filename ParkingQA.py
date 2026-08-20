# Smart Parking Management System
# QA Testing Program

from ParkingManagement import (
    vehicle_entry,
    vehicle_exit,
    calculate_fee,
    check_slot,
    PARKING_SLOTS
)


passed = 0
failed = 0


def check_test(test_name, condition):

    global passed
    global failed

    if condition:

        print(f"{test_name}: PASS")
        passed += 1

    else:

        print(f"{test_name}: FAIL")
        failed += 1


print("==============================================")
print("SMART PARKING MANAGEMENT - QA TESTING")
print("==============================================")


# =================================================
# TEST 1 - Bike Entry
# =================================================

result = vehicle_entry(
    "T001",
    "TN01AA1111",
    "Bike",
    "2026-08-20 09:00"
)

check_test(
    "Test 1 - Bike Entry",
    result["status"] == "SUCCESS"
)


# =================================================
# TEST 2 - Car Entry
# =================================================

result = vehicle_entry(
    "T002",
    "TN01AA2222",
    "Car",
    "2026-08-20 09:00"
)

check_test(
    "Test 2 - Car Entry",
    result["status"] == "SUCCESS"
)


# =================================================
# TEST 3 - SUV Entry
# =================================================

result = vehicle_entry(
    "T003",
    "TN01AA3333",
    "SUV",
    "2026-08-20 09:00"
)

check_test(
    "Test 3 - SUV Entry",
    result["status"] == "SUCCESS"
)


# =================================================
# TEST 4 - Truck Entry
# =================================================

result = vehicle_entry(
    "T004",
    "TN01AA4444",
    "Truck",
    "2026-08-20 09:00"
)

check_test(
    "Test 4 - Truck Entry",
    result["status"] == "SUCCESS"
)


# =================================================
# TEST 5 - EV Entry
# =================================================

result = vehicle_entry(
    "T005",
    "TN01AA5555",
    "Electric Vehicle",
    "2026-08-20 09:00"
)

check_test(
    "Test 5 - EV Entry",
    result["status"] == "SUCCESS"
)


# =================================================
# TEST 6 - Duplicate Vehicle
# =================================================

result = vehicle_entry(
    "T006",
    "TN01AA2222",
    "Car",
    "2026-08-20 10:00"
)

check_test(
    "Test 6 - Duplicate Vehicle",
    result["status"] == "FAILED"
)


# =================================================
# TEST 7 - Wrong Vehicle Type
# =================================================

result = vehicle_entry(
    "T007",
    "TN01AA7777",
    "Bus",
    "2026-08-20 10:00"
)

check_test(
    "Test 7 - Wrong Vehicle Type",
    result["status"] == "FAILED"
)


# =================================================
# TEST 8 - Wrong Vehicle-Slot Combination
# =================================================

# Directly verify that a Car receives a Car slot
car_slot = None

for slot_id, slot in PARKING_SLOTS.items():

    if (
        slot["occupied"]
        and slot["type"] == "Car"
    ):

        car_slot = slot_id
        break


check_test(
    "Test 8 - Correct Vehicle-Slot Combination",
    car_slot is not None
)


# =================================================
# TEST 9 - Normal Parking Fee
# =================================================

fee = calculate_fee(
    "Car",
    "2026-08-20 10:00",
    "2026-08-20 12:00"
)

check_test(
    "Test 9 - Normal Parking Fee",
    fee["total_fee"] == 100
)


# =================================================
# TEST 10 - Early Exit
# =================================================

result = vehicle_exit(
    "T002",
    "2026-08-20 09:30"
)

check_test(
    "Test 10 - Early Exit",
    result["status"] == "FAILED"
)


# =================================================
# TEST 11 - Normal Exit
# =================================================

result = vehicle_exit(
    "T002",
    "2026-08-20 12:00"
)

check_test(
    "Test 11 - Normal Exit",
    result["status"] == "SUCCESS"
)


# =================================================
# TEST 12 - Lost Ticket
# =================================================

result = vehicle_exit(
    "T001",
    "2026-08-20 12:00",
    lost_ticket=True
)

check_test(
    "Test 12 - Lost Ticket",
    result["status"] == "SUCCESS"
    and result["lost_ticket_charge"] == 200
)


# =================================================
# TEST 13 - Overnight Parking
# =================================================

result = vehicle_entry(
    "T008",
    "TN01AA8888",
    "Car",
    "2026-08-20 22:00"
)

exit_result = vehicle_exit(
    "T008",
    "2026-08-21 06:00"
)

check_test(
    "Test 13 - Overnight Parking",
    exit_result["status"] == "SUCCESS"
    and exit_result["hours"] == 8
)


# =================================================
# TEST 14 - Peak Hour Pricing
# =================================================

fee = calculate_fee(
    "Car",
    "2026-08-20 17:00",
    "2026-08-20 19:00"
)

check_test(
    "Test 14 - Peak Hour Pricing",
    fee["peak_charge"] > 0
)


# =================================================
# TEST 15 - EV Charging Fee
# =================================================

fee = calculate_fee(
    "Electric Vehicle",
    "2026-08-20 10:00",
    "2026-08-20 12:00",
    ev_charging=True
)

check_test(
    "Test 15 - EV Charging Fee",
    fee["ev_charging_fee"] == 100
)


# =================================================
# TEST 16 - VIP Discount
# =================================================

normal_fee = calculate_fee(
    "Car",
    "2026-08-20 10:00",
    "2026-08-20 12:00",
    vip=False
)

vip_fee = calculate_fee(
    "Car",
    "2026-08-20 10:00",
    "2026-08-20 12:00",
    vip=True
)

check_test(
    "Test 16 - VIP Discount",
    vip_fee["total_fee"]
    < normal_fee["total_fee"]
)


# =================================================
# TEST 17 - VIP Entry
# =================================================

result = vehicle_entry(
    "T009",
    "TN01AA9999",
    "SUV",
    "2026-08-20 10:00",
    vip=True
)

check_test(
    "Test 17 - VIP Entry",
    result["status"] == "SUCCESS"
)


# =================================================
# TEST 18 - Invalid Ticket
# =================================================

result = vehicle_exit(
    "T999",
    "2026-08-20 12:00"
)

check_test(
    "Test 18 - Invalid Ticket",
    result["status"] == "FAILED"
)


# =================================================
# TEST 19 - Invalid Exit Time
# =================================================

result = vehicle_entry(
    "T010",
    "TN02BB1010",
    "Bike",
    "2026-08-20 15:00"
)

exit_result = vehicle_exit(
    "T010",
    "2026-08-20 14:00"
)

check_test(
    "Test 19 - Invalid Exit Time",
    exit_result["status"] == "FAILED"
)


# =================================================
# TEST 20 - Fully Booked Parking Lot
# =================================================

# Fill all available bike slots
vehicle_entry(
    "T011",
    "TN02BB1111",
    "Bike",
    "2026-08-20 10:00"
)

vehicle_entry(
    "T012",
    "TN02BB1212",
    "Bike",
    "2026-08-20 10:00"
)

result = vehicle_entry(
    "T013",
    "TN02BB1313",
    "Bike",
    "2026-08-20 10:00"
)

check_test(
    "Test 20 - Full Parking Lot",
    result["status"] == "FAILED"
)


# =================================================
# TEST 21 - Duplicate Ticket
# =================================================

result = vehicle_entry(
    "T003",
    "TN02CC3333",
    "SUV",
    "2026-08-20 11:00"
)

check_test(
    "Test 21 - Duplicate Ticket",
    result["status"] == "FAILED"
)


# =================================================
# TEST 22 - Minimum One Hour Charge
# =================================================

fee = calculate_fee(
    "Bike",
    "2026-08-20 10:00",
    "2026-08-20 10:30"
)

check_test(
    "Test 22 - Minimum One Hour Charge",
    fee["hours"] == 1
)


# =================================================
# SUMMARY
# =================================================

print("\n==============================================")
print("QA SUMMARY")
print("==============================================")

print(f"Total Tests : {passed + failed}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")

if failed == 0:

    print("\nALL TESTS PASSED")

else:

    print("\nSOME TESTS FAILED")