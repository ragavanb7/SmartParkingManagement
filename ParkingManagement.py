# Smart Parking Management System
# Development Program

from datetime import datetime


# =========================================================
# PARKING SLOTS
# =========================================================

PARKING_SLOTS = {
    "B1": {"type": "Bike", "occupied": False},
    "B2": {"type": "Bike", "occupied": False},

    "C1": {"type": "Car", "occupied": False},
    "C2": {"type": "Car", "occupied": False},
    "C3": {"type": "Car", "occupied": False},

    "S1": {"type": "SUV", "occupied": False},
    "S2": {"type": "SUV", "occupied": False},

    "T1": {"type": "Truck", "occupied": False},

    "E1": {"type": "Electric Vehicle", "occupied": False},
    "E2": {"type": "Electric Vehicle", "occupied": False}
}


# =========================================================
# PARKING RATES
# =========================================================

BASE_RATES = {
    "Bike": 20,
    "Car": 50,
    "SUV": 70,
    "Truck": 100,
    "Electric Vehicle": 60
}


# =========================================================
# PARKING RECORDS
# =========================================================

PARKING_RECORDS = {}
VEHICLES = {}


# =========================================================
# PEAK HOURS
# =========================================================

PEAK_START = 17
PEAK_END = 21


# =========================================================
# FIND SUITABLE SLOT
# =========================================================

def find_slot(vehicle_type, vip=False):

    for slot_id, slot in PARKING_SLOTS.items():

        if (
            not slot["occupied"]
            and slot["type"] == vehicle_type
        ):
            return slot_id

    return None


# =========================================================
# VEHICLE ENTRY
# =========================================================

def vehicle_entry(
    ticket_id,
    vehicle_number,
    vehicle_type,
    entry_time,
    vip=False
):

    valid_types = [
        "Bike",
        "Car",
        "SUV",
        "Truck",
        "Electric Vehicle"
    ]

    # Check vehicle type
    if vehicle_type not in valid_types:

        return {
            "status": "FAILED",
            "message": "Invalid vehicle type"
        }


    # Check duplicate vehicle
    if vehicle_number in VEHICLES:

        return {
            "status": "FAILED",
            "message": "Vehicle already parked"
        }


    # Check duplicate ticket
    if ticket_id in PARKING_RECORDS:

        return {
            "status": "FAILED",
            "message": "Ticket already exists"
        }


    # Automatically allocate suitable slot
    slot_id = find_slot(
        vehicle_type,
        vip
    )

    if slot_id is None:

        return {
            "status": "FAILED",
            "message": "No suitable parking slot available"
        }


    # Occupy slot
    PARKING_SLOTS[slot_id]["occupied"] = True


    # Store parking record
    PARKING_RECORDS[ticket_id] = {
        "vehicle_number": vehicle_number,
        "vehicle_type": vehicle_type,
        "slot_id": slot_id,
        "entry_time": entry_time,
        "vip": vip,
        "status": "PARKED"
    }


    # Store active vehicle
    VEHICLES[vehicle_number] = ticket_id


    return {
        "status": "SUCCESS",
        "ticket_id": ticket_id,
        "vehicle_number": vehicle_number,
        "slot_id": slot_id,
        "message": "Vehicle parked successfully"
    }


# =========================================================
# CALCULATE PARKING FEE
# =========================================================

def calculate_fee(
    vehicle_type,
    entry_time,
    exit_time,
    vip=False,
    lost_ticket=False,
    ev_charging=False
):

    try:

        entry = datetime.strptime(
            entry_time,
            "%Y-%m-%d %H:%M"
        )

        exit = datetime.strptime(
            exit_time,
            "%Y-%m-%d %H:%M"
        )

    except ValueError:

        return None


    # Exit cannot be before entry
    if exit < entry:

        return None


    # Calculate duration
    duration_seconds = (
        exit - entry
    ).total_seconds()

    duration_hours = duration_seconds / 3600

    # Minimum 1 hour charge
    if duration_hours <= 1:

        hours = 1

    else:

        hours = int(duration_hours)

        if duration_hours > hours:
            hours += 1


    # Base parking fee
    base_fee = (
        BASE_RATES[vehicle_type]
        * hours
    )


    # =====================================================
    # PEAK-HOUR CHARGE
    # =====================================================

    peak_charge = 0

    current_time = entry

    while current_time < exit:

        if (
            PEAK_START
            <= current_time.hour
            < PEAK_END
        ):

            peak_charge += (
                BASE_RATES[vehicle_type]
                * 0.50
            )

        current_time = (
            current_time
            + __import__("datetime").timedelta(hours=1)
        )


    # =====================================================
    # VIP DISCOUNT
    # =====================================================

    vip_discount = 0

    if vip:

        vip_discount = base_fee * 0.20


    # =====================================================
    # LOST TICKET
    # =====================================================

    lost_ticket_charge = 0

    if lost_ticket:

        lost_ticket_charge = 200


    # =====================================================
    # EV CHARGING
    # =====================================================

    charging_fee = 0

    if (
        vehicle_type == "Electric Vehicle"
        and ev_charging
    ):

        charging_fee = 100


    # =====================================================
    # FINAL AMOUNT
    # =====================================================

    total_fee = (
        base_fee
        + peak_charge
        + lost_ticket_charge
        + charging_fee
        - vip_discount
    )


    return {
        "base_fee": round(base_fee, 2),
        "peak_charge": round(peak_charge, 2),
        "vip_discount": round(vip_discount, 2),
        "lost_ticket_charge": round(
            lost_ticket_charge,
            2
        ),
        "ev_charging_fee": round(
            charging_fee,
            2
        ),
        "total_fee": round(
            total_fee,
            2
        ),
        "hours": hours
    }


# =========================================================
# VEHICLE EXIT
# =========================================================

def vehicle_exit(
    ticket_id,
    exit_time,
    lost_ticket=False,
    ev_charging=False
):

    # Check ticket
    if ticket_id not in PARKING_RECORDS:

        return {
            "status": "FAILED",
            "message": "Invalid ticket"
        }


    record = PARKING_RECORDS[ticket_id]


    # Check already exited
    if record["status"] == "EXITED":

        return {
            "status": "FAILED",
            "message": "Vehicle already exited"
        }


    # Calculate fee
    fee_details = calculate_fee(
        record["vehicle_type"],
        record["entry_time"],
        exit_time,
        record["vip"],
        lost_ticket,
        ev_charging
    )


    # Invalid exit time
    if fee_details is None:

        return {
            "status": "FAILED",
            "message": "Invalid exit time"
        }


    # Release slot
    slot_id = record["slot_id"]

    PARKING_SLOTS[slot_id]["occupied"] = False


    # Remove active vehicle
    vehicle_number = record["vehicle_number"]

    if vehicle_number in VEHICLES:

        del VEHICLES[vehicle_number]


    # Update record
    record["status"] = "EXITED"
    record["exit_time"] = exit_time
    record["fee"] = fee_details["total_fee"]


    return {
        "status": "SUCCESS",
        "ticket_id": ticket_id,
        "slot_id": slot_id,
        "hours": fee_details["hours"],
        "base_fee": fee_details["base_fee"],
        "peak_charge": fee_details["peak_charge"],
        "vip_discount": fee_details["vip_discount"],
        "lost_ticket_charge":
            fee_details["lost_ticket_charge"],
        "ev_charging_fee":
            fee_details["ev_charging_fee"],
        "total_fee":
            fee_details["total_fee"]
    }


# =========================================================
# SAMPLE EXECUTION
# =========================================================

if __name__ == "__main__":

    print("==============================================")
    print("SMART PARKING MANAGEMENT SYSTEM")
    print("==============================================")


    print("\nVEHICLE ENTRY")

    entry = vehicle_entry(
        "T001",
        "TN01AB1234",
        "Car",
        "2026-08-20 10:00"
    )

    print(entry)


    print("\nVEHICLE EXIT")

    exit_result = vehicle_exit(
        "T001",
        "2026-08-20 12:00"
    )

    print(exit_result)