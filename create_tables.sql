-- Create student table
CREATE TABLE student (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL
);

-- Create course table
CREATE TABLE course (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX)
);

-- Create enrollment table
CREATE TABLE enrollment (
    id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    timestamp DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_enrollment_student FOREIGN KEY (student_id)
        REFERENCES student(id) ON DELETE CASCADE,
    CONSTRAINT FK_enrollment_course FOREIGN KEY (course_id)
        REFERENCES course(id) ON DELETE CASCADE
);