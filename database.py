import mysql.connector
db_config = {
    'user': 'root',
    'password': 'password', # Enter correct username & password here.
    'host': 'localhost',
    'port' : 3306,
    'database': 'e_learning',
}

# Function to create a database connection
def create_connection():
    return mysql.connector.connect(**db_config)

def create_tables(db):
    cursor = db.cursor()

    # Create the User table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            User_ID INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(20) NOT NULL,
            Password VARCHAR(20) NOT NULL
        )
    ''')

    # Create the Account table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Account (
            Account_No INT AUTO_INCREMENT PRIMARY KEY,
            Account_Type ENUM('student','instructor','administrator') NOT NULL,
            User_ID INT,
            Instructor_ID INT,
            FOREIGN KEY(User_ID) REFERENCES User(User_ID),
            FOREIGN KEY(Instructor_ID) REFERENCES Instructor(Instructor_ID)
        )
    ''')

    # Create the Instructor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Instructor (
            Instructor_ID INT AUTO_INCREMENT PRIMARY KEY,
            Instructor_Name VARCHAR(20) NOT NULL,
            PASSWORD VARCHAR(20) NOT NULL
        )
    ''')

    # Create the Course table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Course (
            Course_ID INT AUTO_INCREMENT PRIMARY KEY,
            Course_Name VARCHAR(50) NOT NULL,
            Instructor_ID INT NOT NULL,
            FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
        )
    ''')

    # Enrollment Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Enrollment (
    Enrollment_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,
    Course_ID INT NOT NULL,
    Course_Status enum('Completed','Ongoing') DEFAULT 'Ongoing',
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
    )
    ''')


    # Create the Admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            Admin_ID INT AUTO_INCREMENT PRIMARY KEY,
            Admin_Name VARCHAR(20) NOT NULL,
            Password VARCHAR(20) NOT NULL
        )
    ''')

    # Create the Content table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Content (
            Content_ID INT AUTO_INCREMENT PRIMARY KEY,
            Content_Details VARCHAR(100),
            Course_ID INT NOT NULL,
            Admin_ID INT NOT NULL,
            Approval_Status enum('Approved','Pending') NOT NULL,
            FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
            FOREIGN KEY (Admin_ID) REFERENCES Admin(Admin_ID)
        )
    ''')

    # Create the Support table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Support (
            Admin_ID INT NOT NULL,
            Support_No INT AUTO_INCREMENT PRIMARY KEY,
            Request VARCHAR(255) NOT NULL,
            Reply VARCHAR(255) NOT NULL,
            User_ID INT NOT NULL,
            FOREIGN KEY (Admin_ID) REFERENCES Admin(Admin_ID),
            FOREIGN KEY (User_ID) REFERENCES User(User_ID)
        )
    ''')

    # Create the Test table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Test (
            Test_ID INT AUTO_INCREMENT PRIMARY KEY,
            User_ID INT NOT NULL,
            Course_ID INT NOT NULL,
            Test_Details VARCHAR(255),
            Instructor_ID INT NOT NULL,
            Test_Status enum('Completed','Available') DEFAULT 'Available',
            final_test BOOLEAN NOT NULL,
            FOREIGN KEY (User_ID) REFERENCES User(User_ID),
            FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
            FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
        )
    ''')

    # Create the Evaluation table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Evaluation (
            Test_ID INT NOT NULL,
            Test_Grade VARCHAR(1) NOT NULL,
            Instructor_ID INT NOT NULL,
            Test_response VARCHAR(255),
            User_ID INT NOT NULL,
            FOREIGN KEY (Test_ID) REFERENCES Test(Test_ID),
            FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
        )
    ''')

    # Create the Feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Feedback (
            Test_ID INT,
            Feedback_No INT PRIMARY KEY,
            Feedback_Text text,
            FOREIGN KEY (Test_ID) REFERENCES Test(Test_ID)
        )
    ''')

    # Create the Certificate table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Certificate (
            Certificate_ID INT AUTO_INCREMENT PRIMARY KEY,
            Test_ID INT NOT NULL,
            Certificate_Date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            User_ID INT NOT NULL,
            FOREIGN KEY (Test_ID) REFERENCES Test(Test_ID),
            FOREIGN KEY (User_ID) REFERENCES User(User_ID)
        )
    ''')

    """# Create the GetStudentCountForCourse procedure
    cursor.execute('''
        DELIMITER //
        CREATE PROCEDURE GetStudentCountForCourse(IN courseID INT)
        BEGIN
            SELECT COUNT(*) AS student_count FROM Enrollment WHERE Course_ID = courseID;
        END //
        DELIMITER ;
    ''')

    # Create the generate_certificate_after_grading trigger
    cursor.execute('''
        DELIMITER //
        CREATE TRIGGER generate_certificate_after_grading
        AFTER UPDATE ON Evaluation
        FOR EACH ROW
        BEGIN
            DECLARE is_final_test INT;
            
            IF NEW.Test_Grade = 'S' THEN
                SELECT final_test INTO is_final_test FROM Test WHERE Test_ID = NEW.Test_ID;
                
                IF is_final_test = 1 THEN
                    INSERT INTO Certificate (User_ID, Course_ID, Certificate_Date)
                    VALUES (NEW.User_ID, (SELECT Course_ID FROM Test WHERE Test_ID = NEW.Test_ID), NOW());
                END IF;
            END IF;
        END //
        DELIMITER ;
    ''')

    # Create the GetCourseCountForInstructor Function
    cursor.execute('''
        DELIMITER //

        CREATE FUNCTION GetCourseCountForInstructor(instructorID INT)
        RETURNS INT
        DETERMINISTIC
        READS SQL DATA
        BEGIN
            DECLARE course_count INT;
            SELECT COUNT(*) INTO course_count FROM Course WHERE Instructor_ID = instructorID;
            RETURN course_count;
        END //

        DELIMITER ;
    ''')"""

    db.commit()
    cursor.close()

    