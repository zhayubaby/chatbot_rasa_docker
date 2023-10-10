# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import sqlite3


class QueryOrderDetailsAction(Action):
    def name(self):
        return "query_order_details"

    def run(self, dispatcher, tracker, domain):
        # Replace with your logic to query order details based on slot value
        order_number = tracker.get_slot("order_number")
        # Perform the query and obtain order details
        order_details = self.query_order_from_database(order_number)

        # Check if order details were successfully obtained
        if order_details:
            dispatcher.utter_message(f"Here are the details for your order {order_number}: {order_details}")
        else:
            dispatcher.utter_message("I'm sorry, but I couldn't retrieve the order details.")

        return [SlotSet("order_number", order_number)]  # Optionally update the slot

    # Replace this with your actual logic to query order details
    def query_order_from_database(self, order_number):
        if order_number == "1234567890":
            return "Your order will be delivered tomorrow."
        else:
            return None
        

conn = sqlite3.connect("teacher_database.db")
cursor = conn.cursor()

# Create the 'teachers' table
cursor.execute('''CREATE TABLE IF NOT EXISTS teachers (
                  id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  subject TEXT NOT NULL,
                  contact TEXT NOT NULL
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                  id INTEGER PRIMARY KEY,
                  course_name TEXT NOT NULL,
                  subject TEXT NOT NULL,
                  time TEXT NOT NULL,
                  description TEXT NOT NULL,
                  teacher_in_charge TEXT NOT NULL,
                  learning_style TEXT NOT NULL,
                  remarks TEXT NOT NULL
                )''')
# cursor.execute("DROP TABLE courses")

conn.commit()

def add_teacher(name, subject, contact):
    cursor.execute("INSERT INTO teachers (name, subject, contact) VALUES (?, ?, ?)",
                   (name, subject, contact))
    conn.commit()

def add_course(course_name, subject, time, description, teacher_in_charge, learning_style, remarks):
    cursor.execute("INSERT INTO courses (course_name, subject, time, description, teacher_in_charge, learning_style, remarks) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (course_name, subject, time, description, teacher_in_charge, learning_style, remarks))
    conn.commit()

# def get_teacher_by_id(teacher_id):
#     cursor.execute("SELECT * FROM teachers WHERE id=?", (teacher_id,))
#     teacher = cursor.fetchone()
#     return teacher

# def get_teachers_by_subject(subject):
#     cursor.execute("SELECT * FROM teachers WHERE subject=?", (subject,))
#     teachers = cursor.fetchall()
#     return teachers

# def get_teacher_by_name(name):
#     cursor.execute("SELECT * FROM teachers WHERE name=?", (name,))
#     teacher = cursor.fetchone()
#     return teacher

# def update_teacher_contact(teacher_id, new_contact):
#     cursor.execute("UPDATE teachers SET contact=? WHERE id=?", (new_contact, teacher_id))
#     conn.commit()

# def delete_teacher(teacher_id):
#     cursor.execute("DELETE FROM teachers WHERE id=?", (teacher_id,))
#     conn.commit()

class ActionAddTeacher(Action):
    def name(self) -> Text:
        return "action_add_teacher"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Use the add_teacher function to insert data into the database (implement this function)
        conn = DbQueryingMethods.create_connection(db_file="teacher_database.db")
        add_teacher("John Doe", "ML Fundamentals", "john@brainiac.com")
        add_teacher("Mary Hernandez", "Intro to AI", "mary@brainiac.com")
        add_teacher("Stuart Russell", "AI Superpowers", "stuart@brainiac.com")
        add_teacher("Geoffrey Hinton", "AI learning advanced", "geoffrey@brainiac.com")
        add_teacher("Nick Bostrom", "ML operation practice", "nick@brainiac.com")

        dispatcher.utter_message("Teacher added successfully!")
        return []

class ActionAddCourse(Action):
    def name(self) -> Text:
        return "action_add_course"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Use the add_teacher function to insert data into the database (implement this function)
        conn = DbQueryingMethods.create_connection(db_file="teacher_database.db")
        add_course("ML Fundamentals", "Machine Learning", "You need to learn 60 online hours and it can be teached in-person", "This course provides fundamental knowledge to Machine Learning.", "Joe Doe", "Online or in-person", "Charge extra $50 if chosen in-person.")
        add_course("Intro to AI", "Artificial Intelligence", "You need to learn 100 online hours and it can be teached in-person", "This course provides a basic introduction to Artificial Intelligence.", "Mary Hernandez", "Online or in-person", "No extra costs if chosen in-person.")
        add_course("AI Superpowers", "Artificial Intelligence", "You need to learn 150 online hours and it can be teached in-person", "You can learn about the deeds of some people or countries who have made important contributions to promoting the development of AI in today's world.", "Stuart Russell", "Online or in-person", "Charge extra $75 if chosen in-person.")
        add_course("AI learning advanced", "Artificial Intelligence", "You need to learn 200 online hours and it can be teached in-person", "This course provides some advanced knowledge of AI algorithms and deep learning algorithms.", "Geoffrey Hinton", "Online or in-person", "Charge extra $150 if chosen in-person.")
        add_course("ML operation practice", "Machine Learning", "You need to learn 175 online hours and it can be teached in-person", "This course provides practical knowledge about machine learning.", "Nick Bostrom", "Online or in-person", "Charge extra $90 if chosen in-person.")
        dispatcher.utter_message("Course added successfully!")
        return []

class DbQueryingMethods:
    def create_connection(db_file):
        """ 
        create a database connection to the SQLite database
        specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)

        return conn
    

class QueryTeacherInfoAction(Action):
    def name(self) -> Text:
        return "action_query_teacher_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the teacher's name from the user's message
        teacher_name = tracker.get_slot("teacher_name")

        # Replace this with your logic to query teacher information
        teacher_info = self.query_teacher_info(teacher_name)

        if teacher_info:
            # Respond with teacher information
            dispatcher.utter_message(response="utter_teacher_info", teacher_name=teacher_name, teacher_info=teacher_info)
        else:
            dispatcher.utter_message("I couldn't find information about that teacher. Please check the name and try again.")

        return []

    # Replace this with your actual logic to query teacher information
    def query_teacher_info(self, teacher_name: str) -> Dict[str, Any]:
        conn = sqlite3.connect("teacher_database.db")
        cursor = conn.cursor()

        # Query the database for teacher information based on the teacher_name
        cursor.execute("SELECT subject, contact FROM teachers WHERE name = ?", (teacher_name,))
        teacher_data = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Check if teacher_data is not empty
        if teacher_data:
            # Create a dictionary with the retrieved data
            teacher_details = {
                "course_in_charge": teacher_data[0],
                "contact": teacher_data[1],
            }
            return teacher_details
        else:
            return None

subscription_plan_database = {
    "one_course_free": "Our free one-course plan allows you to access a single course for free. You can view up to three chapters of the course content.",
    "pay as you go": "With our pay-as-you-go plan, you pay for courses individually. You get full access to any course you purchase, giving you flexibility in your learning journey.",
    "monthly": "The monthly subscription plan costs $50 per month and allows you to access up to 10 courses each month. It's a great choice for those who want access to multiple courses.",
    "yearly": "Our yearly subscription plan costs $450 per year and offers unlimited access to all our courses. It's perfect for those committed to long-term learning."
}

class SearchCourseTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_course_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve course type from slots
        course_type = tracker.get_slot("course_type")
        if course_type == "Artificial Intelligence" or "Machine Learning":
            dispatcher.utter_message(response="utter_ask_course_name", course_type=course_type)
        else:
            dispatcher.utter_message("I'm sorry, I couldn't find any course type you just provided to me.")
        # dispatcher.utter_message(text=f"course_type: {course_type}")

        return []


class SearchCourseAction(Action):
    def name(self) -> Text:
        return "action_search_course"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve course name from slots
        course_name = tracker.get_slot("course_name")

        course_info = self.query_course_info(course_name)
        if course_info:
            # Respond with course information
            dispatcher.utter_message(response="utter_give_course_info", course_name=course_name, course_info=course_info)
        else:
            dispatcher.utter_message(response="utter_course_not_found")

        return []


    def query_course_info(self, course_name: str) -> Dict[str, Any]:
            conn = sqlite3.connect("teacher_database.db")
            cursor = conn.cursor()

            # Query the database for course information based on the course_name
            cursor.execute("SELECT subject, time, description, teacher_in_charge, learning_style, remarks FROM courses WHERE course_name = ?", (course_name,))
            course_data = cursor.fetchone()

            # Close the database connection
            conn.close()

            # Check if course_data is not empty
            if course_data:
                # Create a dictionary with the retrieved data
                course_details = {
                    "subject": course_data[0],
                    "time": course_data[1],
                    "description": course_data[2],
                    "teacher_in_charge": course_data[3],
                    "learning_style": course_data[4],
                }
                return course_details
            else:
                return None
            
class SearchCourseLearningStyleAction(Action):
    def name(self) -> Text:
        return "action_search_course_learning_style"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve course type from slots
        course_name = tracker.get_slot("course_name")
        course_learning_style = tracker.get_slot("course_learning_style")
        course_remarks = self.query_course_remarks_info(course_name)

        if course_learning_style == "in-person":
            dispatcher.utter_message(f"The learning style of the course {course_name} you choose is {course_learning_style}, here is some extra detailed remarks: {course_remarks} ", course_name=course_name, course_learning_style=course_learning_style, course_remarks=course_remarks)
        elif course_learning_style == "online":
            dispatcher.utter_message(f"you do not need to pay anything extra for the course {course_name} you choose", course_name=course_name)
        else:
            dispatcher.utter_message("I'm sorry, we do not have such learning style, please choose others.")
        # dispatcher.utter_message(text=f"course_type: {course_type}")

        return []
    
    def query_course_remarks_info(self, course_name: str) -> Dict[str, Any]:
            conn = sqlite3.connect("teacher_database.db")
            cursor = conn.cursor()

            # Query the database for course information based on the course_name
            cursor.execute("SELECT subject, teacher_in_charge, remarks FROM courses WHERE course_name = ?", (course_name,))
            course_data = cursor.fetchone()

            # Close the database connection
            conn.close()

            # Check if course_data is not empty
            if course_data:
                # Create a dictionary with the retrieved data
                course_details = {
                    "subject": course_data[0],
                    "teacher_in_charge": course_data[1],
                    "remarks": course_data[2],
                }
                return course_details
            else:
                return None
    
class SearchSubscriptionPlanAction(Action):
    def name(self) -> Text:
        return "action_subscription_plan"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve course name from slots
        subscription_plan = tracker.get_slot("subscription_plan")

        if subscription_plan in subscription_plan_database:
            subscription_plan_info = subscription_plan_database[subscription_plan]
            dispatcher.utter_message(response="utter_subscription_plan_info", subscription_plan=subscription_plan, subscription_plan_info=subscription_plan_info)
        else:
            dispatcher.utter_message("I'm sorry, I couldn't find any subscription plan you just provided to me.")

        return []
    
class ActionComplaintReply(Action):
    def name(self) -> Text:
        return "action_utter_reply"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # You can generate or fetch the manager's name and email here
        manager_name = "Mr.Tom Green" 
        manager_email = "TomGreentg@outlook.com"

        dispatcher.utter_message(f"I'm sorry for the trouble, you can contact our senior manager {manager_name} at {manager_email}.")

        return []


class ActionConnectToSupervisor(Action):
    def name(self) -> Text:
        return "action_connect_to_supervisor"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # You can generate or fetch the supervisor's name here
        supervisor_name = "David Suarez" 

        # Send a message indicating the connection to the supervisor
        dispatcher.utter_message(f"I'm connecting you to our human supervisor, {supervisor_name}. Please hold on for a moment.")

        return []
    
class ActionEmailQueryInstruction(Action):
    def name(self) -> Text:
        return "action_email_query_instructions"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # You can generate or fetch the email id here
        email_id = "cusqueryhelp@brainiac.com" 

        dispatcher.utter_message(f"If you prefer to email your query, you can send it to {email_id}. Please include as much detail as possible in your email, and our team will get back to you soon.")

        return []

class ActionPhoneCallQueryInstruction(Action):
    def name(self) -> Text:
        return "action_phone_call_query_instructions"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("If you'd like to speak to an executive over a phone call, please provide your phone number, and we'll arrange a call with one of our team members.")

        return []