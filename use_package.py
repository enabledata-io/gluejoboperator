from packages.package.Base import Base

class FirstETL(Base):
    def transform(self, df):
        df['column_test'] = 'some value'

        return df

if __name__ == '__main__':
    first_etl = FirstETL(env='production')
    first_etl.etl(s3_path='', table_name='first_table')
