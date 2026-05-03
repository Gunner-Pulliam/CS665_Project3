INSERT INTO Students VALUES
(1, 'Clark', 'Kent', 'superman@gmail.com', '2024-01-10', CURRENT_TIMESTAMP),
(2, 'Bruce', 'Wayne', 'batman@gmail.com', '2024-02-11', CURRENT_TIMESTAMP),
(3, 'Diana', 'Wonder', 'wonderwoman@gmail.com', '2024-03-12', CURRENT_TIMESTAMP),
(4, 'John', 'Jones', 'manhunter@gmail.com', '2024-04-13', CURRENT_TIMESTAMP),
(5, 'Hal', 'Jordan', 'greenlantern@gmail.com', '2024-05-14', CURRENT_TIMESTAMP);

INSERT INTO Instructors VALUES
(1, 'Dr.Doom', 'Math', '2020-06-15', CURRENT_TIMESTAMP),
(2, 'Dr.Manhattan', 'History', '2020-07-16', CURRENT_TIMESTAMP),
(3, 'Dr.Strange', 'Biology', '2020-08-17', CURRENT_TIMESTAMP),
(4, 'Dr.Richards', 'Physics', '2020-09-18', CURRENT_TIMESTAMP),
(5, 'Dr.Stark', 'Engineering', '2020-10-19', CURRENT_TIMESTAMP);

INSERT INTO Courses VALUES
(1, 'Calculus III', 3, 1, CURRENT_TIMESTAMP),
(2, 'World History', 4, 2, CURRENT_TIMESTAMP),
(3, 'Biology III', 3, 3, CURRENT_TIMESTAMP),
(4, 'Physics III', 3, 4, CURRENT_TIMESTAMP),
(5, 'Advanced Design', 4, 5, CURRENT_TIMESTAMP);

INSERT INTO Enrollments VALUES
(1, 1, 1, 92.5, '2024-01-15', CURRENT_TIMESTAMP),
(2, 2, 2, 90.0, '2024-02-16', CURRENT_TIMESTAMP),
(3, 3, 3, 80.0, '2024-03-17', CURRENT_TIMESTAMP),
(4, 4, 4, 85.5, '2024-04-18', CURRENT_TIMESTAMP),
(5, 5, 5, 75.0, '2024-05-19', CURRENT_TIMESTAMP);