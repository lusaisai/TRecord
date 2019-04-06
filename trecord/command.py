from trecord import Database, get_database_by_url, TRecordError
from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.styles import Style, style_from_pygments_cls, merge_styles
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import TransactSqlLexer
from pygments.styles.rainbow_dash import RainbowDashStyle
import sys
from tabulate import tabulate


class Command:
    """This class is an interactive command line client with Database"""
    def __init__(self, database: Database):
        self.database = database
        self.limit = 100
        self.message = None
        self.style = None
        self.setup_prompt()
        self.session = PromptSession(style=self.style, lexer=PygmentsLexer(TransactSqlLexer))

    def set_limit(self, limit):
        self.limit = limit

    def setup_prompt(self):
        self.style = merge_styles([
            style_from_pygments_cls(RainbowDashStyle),

            Style.from_dict({
                'username': '#8dc3fc',
                'punctuation': '#090908',
                'host': '#8dc3fc',
                'database': '#aa83fc'
            })
        ])

        self.message = [
            ('class:username', self.database.database_url.username),
            ('class:punctuation', '@'),
            ('class:host', self.database.database_url.host),
            ('class:punctuation', ':'),
            ('class:database', self.database.get_current_db()),
            ('class:punctuation', '> '),
        ]

    @staticmethod
    def exit():
        print_formatted_text(HTML('<b>Quit.</b>'))
        sys.exit()

    def run_query_to_output(self, query):
        try:
            result = self.database.query(query, limit=self.limit)
            if result:
                headers = ['{}({})'.format(*item) for item in result[0]]
                records = result[1:]
                print(tabulate(records, headers=headers, tablefmt='psql'))
                print('\n{} rows returned'.format(len(records)))
            else:
                print('no rows returned')
        except TRecordError as err:
            print(err)

    def run_command(self, command):
        pass

    @staticmethod
    def help():
        print('This list of commands:')
        print('?\tPrint this help document.')
        print('help\tPrint this help document.')
        print('<query>\tAny valid SQL query.')

    def loop(self):
        query_lines = []
        while True:
            try:
                this_line = self.session.prompt(self.message)
                this_line = this_line.strip()

                if this_line in ['help', '?']:
                    self.help()
                elif this_line.startswith('.'):
                    self.run_command(this_line)
                else:
                    query_lines.append(this_line)
                    if this_line.endswith(';'):
                        query = '\n'.join(query_lines).strip()
                        self.run_query_to_output(query)
                        query_lines = []

                        if query.lower().startswith('use'):  # reset the database at the prompt
                            self.setup_prompt()
            except KeyboardInterrupt:
                query_lines = []
                continue
            except EOFError:
                self.exit()


if __name__ == '__main__':
    db = get_database_by_url('mysql+pymysql://lusaisai:lusaisai@198.58.115.91/employees')
    cmd = Command(db)
    cmd.loop()

