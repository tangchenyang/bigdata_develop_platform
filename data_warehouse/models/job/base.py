class Job:
    name = None
    input_tables = None
    output_table = None

    def __init__(self):
        if self.name is None:
            self.name = self.__class__.__name__

    def process(self):
        pass

    def execute(self):
        print(f"Executing job {self.name}")
        print(f"Input tables: {self.input_tables}")
        print(f"Output table: {self.input_tables}")
        self.process()
