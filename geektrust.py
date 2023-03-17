import sys
from datetime import datetime
import re

DATE_FORMAT = "%d%m%Y"
courses = {}
"""
"course_offering_id": {
    "title": "",
    "instructor": "",
    "offering_date": "",
    "max_employees": "",
    "min_employees": "",
    "registered_employees": {
        "email_id": {
            "course_registration_id": "",
            "status": "",  # ACCEPTED, COURSE_FULL_ERROR , COURSE_CANCELED, EMPLOYEE_CANCELED
            "name": ""
        }
    },
    "status": "",  # CANCEL_ACCEPTED, CANCEL_REJECTED,ACCEPTED
    "registered_count": 0
}
"""

employees = {}
"""
    "email_id": {
        "course_registration_id": {
            "status": "",  # ACCEPTED, COURSE_FULL_ERROR , COURSE_CANCELED, EMPLOYEE_CANCELED
        },
        "name": ""
    }
"""

registrations = {}

"""
(email_id, course_offering_id) = {
            "course_registration_id": course_registration_id,
            "status": status
        }
"""


def main():
    # Define input and output file paths
    input_file_path = "input.txt"
    output_file_path = "output.txt"

    # Open input and output files
    with open(input_file_path, "r") as input_file, open(output_file_path, "a+") as output_file:

        # Check if the input file is empty
        if not input_file.readable():
            print("Error: Input file is empty.")
            sys.exit()

        # Loop through each line in the input file
        for line in input_file:
            # Strip whitespace and split the line into tokens
            tokens = line.strip().split()

            # Execute the corresponding function based on the first token
            if len(tokens) == 6 and tokens[0] == "ADD-COURSE-OFFERING":
                course_name = tokens[1]
                instructor = tokens[2]
                date = tokens[3]
                min_employees = tokens[4]
                max_employees = tokens[5]
                result = add_course(course_name, instructor, date, min_employees, max_employees)
            elif len(tokens) == 3 and tokens[0] == "REGISTER":
                email_id = tokens[1]
                course_offering_id = tokens[2]
                result = register_course(email_id, course_offering_id)
            elif len(tokens) == 2 and tokens[0] == "ALLOT-COURSE":
                course_offering_id = tokens[1]
                result = allot_course(course_offering_id)
            elif len(tokens) == 2 and tokens[0] == "CANCEL":
                course_registration_id = tokens[1]
                result = cancel_registration(course_registration_id)
            else:
                # If the command is not recognized or the number of parameters is incorrect, print an error message
                result = "INVALID_COMMAND"
                print(result)

            # Write the result and the command to the output file
            output_file.write(f"{line.strip()} : {result}\n")
            print(f"{line.strip()} : {result}")


def is_validate_date(date_string):
    try:
        datetime.strptime(date_string, DATE_FORMAT)
        return True
    except ValueError:
        return False


def is_validate_min_max(min_employees, max_employees):
    if not isinstance(min_employees, int) or not isinstance(max_employees, int):
        return False
    if min_employees < 0 or max_employees < 1 or min_employees > max_employees:
        return False
    return True


def is_validate_future_date(date_string):
    date = datetime.strptime(date_string, DATE_FORMAT)
    if date < datetime.now():
        return False
    return True


def is_valid_email(email):
    """
    This function takes an email id as input and returns True if the email id is valid, else False.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return True if re.match(pattern, email) else False


def print_input_error():
    print("INPUT_DATA_ERROR")


def add_course(course_name, instructor, offering_date, min_employees, max_employees):
    try:
        course_offering_id = f"{course_name}-{instructor}-{offering_date}"
        if course_offering_id in courses:
            print_input_error()
            return None
        else:
            # Validate the offering date, min and max employees
            if not course_name or not instructor or not offering_date or not min_employees or not max_employees \
                    and not is_validate_date(offering_date) \
                    and not is_validate_min_max(min_employees, max_employees) \
                    and not is_validate_future_date(offering_date):
                print_input_error()
                return None

            # Add the new course offering to the courses dictionary
            courses[course_offering_id] = {
                "title": course_name,
                "instructor": instructor,
                "offering_date": datetime.strptime(offering_date, '%d%m%Y').strftime('%d-%b-%Y'),
                "max_employees": int(max_employees),
                "min_employees": int(min_employees),
                "registered_count": 0,
                "registered_employees": {},
                "status": "ACCEPTED"
            }
            return course_offering_id
    except:
        return None


def register_course(email_id, course_offering_id):
    try:
        # Check if the combination of email-id and course-offering-id is unique
        if not email_id \
                or course_offering_id not in courses \
                or (email_id, course_offering_id) in registrations:
            print_input_error()
            return None

        employee_name = email_id.split("@")[0]
        course_registration_id = f"REG-COURSE-{employee_name}-{courses[course_offering_id]['title']}"
        status = ""
        date_now = datetime.now().strftime(DATE_FORMAT)
        current_course_config = courses[course_offering_id]

        if current_course_config["registered_count"] < current_course_config["max_employees"]:
            if datetime.strptime(date_now, DATE_FORMAT) > datetime.strptime(current_course_config["offering_date"],
                                                                            '%d-%b-%Y') \
                    and current_course_config["registered_count"] < current_course_config["min_employees"]:
                status = "COURSE_CANCELED"
            else:
                status = "ACCEPTED"
        else:
            status = "COURSE_FULL_ERROR"

        if status == "ACCEPTED":
            # Add the registration to the registrations dictionary
            registrations[(email_id, course_offering_id)] = {
                "course_registration_id": course_registration_id,
                "status": status
            }
            # Update the registered_count and registered_employees for the course offering
            courses[course_offering_id]["registered_count"] += 1
            courses[course_offering_id]["registered_employees"][email_id] = {
                "course_registration_id": course_registration_id,
                "name": employee_name,
                "status": status
            }

            return {"course_registration_id": course_registration_id, "status": status}
        return {"status": status}
    except:
        return None


def allot_course(course_offering_id):
    try:
        # Check if the course offering exists
        if course_offering_id not in courses:
            print_input_error()
            return None

        # Get the course offering details
        course_title = courses[course_offering_id]["title"]
        instructor = courses[course_offering_id]["instructor"]
        offering_date = courses[course_offering_id]["offering_date"]

        # Check if minimum employees are registered
        min_employees = courses[course_offering_id]["min_employees"]
        registered_employees = courses[course_offering_id]["registered_employees"]
        if len(registered_employees) < min_employees:
            print("Minimum employees not registered yet.")
            return None

        # Sort the registrations by course_registration_id in ascending order
        sorted_registrations = sorted(registrations, key=lambda r: r[1][0])

        # Create a list to store the course allotment details
        course_allotments = []

        # Loop through each registration and allot the course if the status is ACCEPTED
        for registration in sorted_registrations:
            current_email_id, current_course_offering_id = registration
            registration_details = registrations[(current_email_id, course_offering_id)]
            status = registration_details["status"]
            print(registration_details)

            # Allot the course if the status is ACCEPTED
            if status == "ACCEPTED" and course_offering_id == current_course_offering_id:
                course_registration_id = registration_details["course_registration_id"]
                allotment_date = datetime.now().strftime(DATE_FORMAT)
                status = "ALLOTTED"

                # Update the registration status to ALLOTTED
                registration_details["status"] = "ALLOTTED"

                # Update the course offering details
                courses[course_offering_id]["registered_employees"][current_email_id]["status"] = "ALLOTTED"
                courses[course_offering_id]["status"] = "ALLOTTED"

                # Add the course allotment details to the list
                course_allotments.append((course_offering_id, course_registration_id,
                                          current_email_id, course_title, instructor,
                                          offering_date, allotment_date, status))

        # Return the list of course allotment details
        return course_allotments
    except:
        return None


def cancel_registration(course_registration_id):
    try:
        for registration in registrations:
            email_id = registration[0]
            current_course_offering_id = registration[1]
            current_course_registration_id = registrations[registration]["course_registration_id"]
            print(current_course_registration_id)
            if current_course_registration_id == course_registration_id:
                if courses[current_course_offering_id]["registered_employees"][email_id]["status"] \
                        in ("ACCEPTED", "ALLOTTED"):

                    # Update course offering information
                    courses[current_course_offering_id]["registered_count"] -= 1
                    del courses[current_course_offering_id]["registered_employees"][email_id]

                    # Update registration information
                    del registrations[registration]

                    return {"course_registration_id": course_registration_id, "status": "CANCEL_ACCEPTED"}
                else:
                    return {"course_registration_id": course_registration_id, "status": "CANCEL_REJECTED"}
        return None
    except:
        return None


if __name__ == "__main__":
    main()
