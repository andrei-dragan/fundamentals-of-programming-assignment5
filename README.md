# 💻 Assignment 05
## Requirements
- You will solve the problem below using simple feature-driven development
- Your program must provide a menu-driven console-based user interface. Implementation details are up to you
- Implementation must employ layered architecture and classes
- Have at least 20 procedurally generated items in your application at startup
- Provide specification and tests for all non-UI classes and methods for the first functionality
- Implement and use your own exception classes
- Implement **PyUnit test cases**
- 95% unit test code coverage for all modules except the UI (use *PyCharm Professional*, the *[coverage](https://coverage.readthedocs.io/en/coverage-5.3/)* or other modules)
- implement persistent storage for all entities using file-based repositories
- implement a `settings.properties` file to configure your application

## Problem Statement
### Students Register Management
A faculty stores information about:
- **Student**: `student_id`, `name`
- **Discipline**: `discipline_id`, `name`
- **Grade**: `discipline_id`, `student_id`, `grade_value`

Create an application to:
1. Manage students and disciplines. The user can add, remove, update, and list both students and disciplines.
2. Grade students at a given discipline. Any student may receive one or several grades at any discipline. Deleting a student also removes their grades. Deleting a discipline deletes all grades at that discipline for all students.
3. Search for disciplines/students based on ID or name/title. The search must work using case-insensitive, partial string matching, and must return all matching disciplines/students.
4. Create statistics:
    - All students failing at one or more disciplines (students having an average <5 for a discipline are failing it)
    - Students with the best school situation, sorted in descending order of their aggregated average (the average between their average grades per discipline)
    - All disciplines at which there is at least one grade, sorted in descending order of the average grade(s) received by all students
5. Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade and have a memory-efficient implementation (no superfluous list copying)
6. You must implement two additional repository sets: one using text files for storage, and one using binary files (e.g. using object serialization with [Pickle](https://docs.python.org/3.8/library/pickle.html)).
7. The program must work the same way using in-memory repositories, text-file repositories and binary file repositories.
8. The decision of which repositories are employed, as well as the location of the repository input files will be made in the program’s `settings.properties` file.
