class Base:
    def __init__(self, env: str):
        self.env = env
                  
    def extract(self, s3_path):
        return None

    def transform(self, df):
        return None

    def load(self, table_name):
        return None

    def etl(self, s3_path, table_name):
        try:
            df = self.extract(s3_path)
            df = self.transform(df)
            self.load(df, table_name)
        except:
            print("An exception occurred")