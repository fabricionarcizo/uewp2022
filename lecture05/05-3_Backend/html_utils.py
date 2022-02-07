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

"""A script with utility methods to generate HTML documents."""

from db.sqlite_db import fetch_students_records


class HTML_Utils:
    """A class with a set of static methods to create HTML documents and fetch data from an SQLite database."""

    @staticmethod
    def read_template(filepath: str) -> str:
        """A static method to read the content of an HTML file or CSS file.

        Args:
            filepath (str): The absolute or relative path of an HTML file or CSS
                file. You have to define the path of any HTML template available
                on `html` folder.

        Returns:
            str: The content of an HTML file or CSS file as a string.
        """
        try:
            with open(filepath) as f:
                file = f.read()
        except Exception as ex:
            file = ex
        return file


    def show_db_records(filepath: str = "./html/records.html") -> str:

        """A static method to show all records available in an SQLite database into an HTML template.

        Args:
            filepath (str, optional): The absolute or relative path of an HTML
                file. You have to define the path of any HTML template available
                on `html` folder. Defaults to "./html/records.html".

        Returns:
            str: The content of an HTML template file as a string.
        """
        # Reads the HTML template file.
        html = HTML_Utils.read_template(filepath)

        # Fetch all records from an SQLite database.
        data = fetch_students_records()

        # Create the HTML table elements.
        table = ""
        for elements in data:
            table += "\n            <tr>\n"
            for item in elements:
                table += "                <td>"
                table += str(item)
                table += "</td>\n"
            table += "            </tr>"

        # Replace the dynamic variable `{{students_records}}` in the HTML 
        # template file by the Python variable `table`.
        return html.replace("{{students_records}}", table)
