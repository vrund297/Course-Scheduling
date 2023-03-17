# Course Scheduling

A simple course scheduling application that allows users to add course offerings, register for courses, allot courses to students, and cancel course registrations.

## Installation

1. Clone the repository: `git clone https://github.com/vrund297/course-scheduling.git`
2. Install the required packages: `pip install -r requirements.txt`

## Usage

To run the application, execute the following command: `python main.py`

## Functionality

### Add Course Offering

To add a course offering, use the following command: `add_course(course_name, instructor, offering_date, min_employees, max_employees)`

### Register for a Course

To register for a course, use the following command: `register_course(email, course_name)`

### Allot Course to Students

To allot a course to students, use the following command: `allot_course(course_name)`

### Cancel Course Registration

To cancel a course registration, use the following command: `cancel_registration(course_registration_id)`

## Tests

To run the unit tests, execute the following command: `python testunit.py`
