#!/usr/bin/env python3
#
# MIT License
#
# Copyright (c) 2022 Fabricio Batista Narcizo
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""A script with methods to manage an SQLite database."""

from sqlite3 import connect


# Create the ITU's students database.
DB_NAME = "db/students_records.db" 
connection = connect(DB_NAME)
cursor = connection.cursor()


def create_students_table():
    """Create a table called `students` inside the SQLite database."""
    # create table user inside database if not exists
    query = '''CREATE TABLE IF NOT EXISTS students(
        uid INTEGER PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(150)
    );'''
    cursor.executescript(query)
    connection.commit()


def insert_student_record(name: str, email: str):
    """Insert a new student record in the `students` table."""
    query = '''INSERT INTO students(name, email) VALUES(?, ?)'''
    cursor.execute(query, (name, email))
    connection.commit()


def delete_student_record(uid: str):
    """Delete a selected student record from the `students` table."""
    query = '''DELETE FROM students WHERE uid = ?'''
    cursor.execute(query, (uid))
    connection.commit()


def fetch_students_records():
    """Fetch all ITU's students records available in the `students` table."""
    query = '''SELECT * FROM students'''
    data = cursor.execute(query)
    return data
