from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import connection_string
from models.TestCaseCBE import TestCaseDetails

# Function to create SQLAlchemy session
def create_sqlalchemy_session():
    """
    Creates a SQLAlchemy session.
    """
    try:
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("SQLAlchemy session created successfully")
        return session
    except Exception as e:
        print(f"Error creating SQLAlchemy session: {e}")
        return None


# Function to close the database connection
def close_db_connection(connection):
    """
    Closes the given database connection.
    """
    if connection:
        connection.close()
        print("SQL Server connection is closed")


def write_to_database(session, test_result):
    from utils.helpers import parse_datetime, parse_numeric
    from utils.logger import log_info, log_error
    """
    Writes the test results to the TestCaseDetails table using SQLAlchemy.
    """
    try:

        # Example of how you might use the parse_numeric function
        test_case = TestCaseDetails(
            SL_No=test_result.get('SL_No'),
            Module=test_result.get('Module'),
            Skin=test_result.get('Skin'),
            Cruise_Line=test_result.get('Cruise_Line'),
            Ship=test_result.get('Ship'),
            Sailing_Date=parse_datetime(test_result.get('Sailing_Date')),
            Remarks=test_result.get('Remarks'),
            Session_ID=test_result.get('Session_ID'),
            Test_Cases=test_result.get('Test_Cases'),
            Testing_Comments=test_result.get('Testing_Comments'),
            Load_CS_Result=test_result.get('Load_CS_Result'),
            Load_CS_TimeTaken=parse_numeric(test_result.get('Load_CS_TimeTaken')),
            Cruise_Search_Result=test_result.get('Cruise_Search_Result'),
            Cruise_Search_TimeTaken=parse_numeric(test_result.get('Cruise_Search_TimeTaken')),
            Cruise_Result=test_result.get('Cruise_Result'),
            Cruise_Result_TimeTaken=parse_numeric(test_result.get('Cruise_Result_TimeTaken')),
            Cruise_Details_Result=test_result.get('Cruise_Details_Result'),
            Cruise_Details_TimeTaken=parse_numeric(test_result.get('Cruise_Details_TimeTaken')),
            Category_Avail_Result=test_result.get('Category_Avail_Result'),
            Category_Avail_TimeTaken=parse_numeric(test_result.get('Category_Avail_TimeTaken')),
            Cabin_Selection_Result=test_result.get('Cabin_Selection_Result'),
            Cabin_Selection_TimeTaken=parse_numeric(test_result.get('Cabin_Selection_TimeTaken')),
            Login_Result=test_result.get('Login_Result'),
            Login_TimeTaken=parse_numeric(test_result.get('Login_TimeTaken')),
            Passenger_Details_Result=test_result.get('Passenger_Details_Result'),
            Passenger_Details_TimeTaken=parse_numeric(test_result.get('Passenger_Details_TimeTaken')),
            Payment_Page_Result=test_result.get('Payment_Page_Result'),
            Payment_Page_TimeTaken=parse_numeric(test_result.get('Payment_Page_TimeTaken')),
            Final_Results=test_result.get('Final_Results'),
            Final_Results_TimeTaken=parse_numeric(test_result.get('Final_Results_TimeTaken')),
            Error_Img=test_result.get('Error_Img'),
            Tested_On=test_result.get('Tested_On')
        )

        print(
            "********************** SQL Results, Print all attributes of the test_case object *******************************")
        print(test_case.__dict__)
        log_info(
            "********************** SQL Results, Print all attributes of the test_case object *******************************")
        log_info(test_case.__dict__)
        # Print all attributes of the test_case object
        for attr, value in vars(test_case).items():
            print(f"{attr}: {value}")

        # Add and commit the transaction
        session.add(test_case)
        session.commit()
        print("Test results inserted successfully into the database using SQLAlchemy")
        log_info("Test results inserted successfully into the database using SQLAlchemy")

    except Exception as e:
        print(f"Error inserting into database using SQLAlchemy: {e}")
        log_error(f"Error inserting into database using SQLAlchemy: {e}")
        session.rollback()

