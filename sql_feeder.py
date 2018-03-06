import sqlite3
import os.path

class SQL_Feeder:
    """Used to break down SQL code with many queries and feed one query
    at a time. This will avoid the quries stop being executed if one is
    corrupt."""

    def __init__(self):
        # No config needed
        pass

    def file_feed(self, filename):
        """Reads a file with SQL-queries and yields them one at a time.
        The only syntax checked is that single line comments are ignored
        and checking for ; to see when SQL-query ends. """
        # Make sure we can open file 
        if not os.path.isfile(filename):
            raise ValueError

        # SQL query starts of as empty
        SQL_query = ''
        
        # Open file
        with open(filename, 'r') as sql_file:
            # For each line
            for line in sql_file:
                # Make sure it's not a commented line
                if not self.is_comment(line):
                    # Non-comments get's added to query
                    SQL_query += line.strip()

                    # If we are at the end of sql statement, yield
                    if self.is_query_end(line):
                        yield SQL_query
                        # Empty the query
                        SQL_query = ''

    def string_feed(self, sql_string):
        """ Reads a string with SQL-queries and yields them one at a time.
        The only syntax checked is that single line comments are ignored
        and checking for ; to see when SQL-query ends. """
        pass

    def is_comment(self, string):
        """Returns True if string is a commented line in SQL-syntax (starts
        with -- ). Otherwise return False"""
        return string.lstrip().startswith('--')

    def is_query_end(self, string):
        """Returns True if string is the end of a query in SQL (ends with ; )
        otherwise returns False"""
        return string.rstrip().endswith(';')

