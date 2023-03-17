import unittest
from geektrust import add_course, register_course, allot_course, cancel_registration


class TestCourses(unittest.TestCase):
    def test_entire_course_scheduling_success_flow(self):
        # Test adding a course offering
        course_name = "Data-Structures"
        instructor = "John"
        offering_date = "28032023"
        self.assertEqual(add_course(course_name, instructor, offering_date, "3", "20"),
                         f"{course_name}-{instructor}-{offering_date}")

        # Test registering for a course
        self.assertEqual(register_course("mike@example.com", "Data-Structures-John-28032023")["course_registration_id"],
                         "REG-COURSE-mike-Data-Structures")
        self.assertEqual(register_course("paul@example.com", "Data-Structures-John-28032023")["course_registration_id"],
                         "REG-COURSE-paul-Data-Structures")
        self.assertEqual(
            register_course("vrund@example.com", "Data-Structures-John-28032023")["course_registration_id"],
            "REG-COURSE-vrund-Data-Structures")
        self.assertEqual(
            register_course("aesha@example.com", "Data-Structures-John-28032023")["course_registration_id"],
            "REG-COURSE-aesha-Data-Structures")

        # Test allotting a course
        resutls = allot_course("Data-Structures-John-28032023")
        print(resutls)
        for allotment in resutls:
            self.assertEqual(allotment[7], "ALLOTTED")

        # Test canceling a registration
        self.assertEqual(cancel_registration("REG-COURSE-paul-Data-Structures"),
                         {"course_registration_id": "REG-COURSE-paul-Data-Structures", "status": "CANCEL_ACCEPTED"})

    def test_add_course_offering_failure(self):
        # Test adding a course offering with invalid inputs
        self.assertEqual(add_course("", "John", "28032023", "3", "20"), None)
        self.assertEqual(add_course("Data-Structures", "", "28032023", "3", "20"), None)
        self.assertEqual(add_course("Data-Structures", "John", "", "3", "20"), None)
        self.assertEqual(add_course("Data-Structures", "John", "invalid_date", "3", "20"), None)
        self.assertEqual(add_course("Data-Structures", "John", "28032023", "invalid_capacity", "20"), None)
        self.assertEqual(add_course("Data-Structures", "John", "28032023", "3", "invalid_duration"), None)

    def test_register_course_failure(self):
        # Test registering for a course with invalid inputs
        self.assertEqual(register_course("", "Data-Structures-John-28032023"), None)

    def test_allot_course_failure(self):
        # Test allotting a course with invalid inputs
        self.assertEqual(allot_course("invalid_course_name"), None)
        self.assertEqual(allot_course(""), None)
