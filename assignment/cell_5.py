import pandera as pa
from pandera import Column, DataFrameSchema, Check

# TODO: Define the schema
schema = DataFrameSchema({
    "Type": Column(str, Check.isin(["L", "M", "H"])),
    "Air temperature": Column(float, Check.in_range(295.0, 305.0)),
    "Process temperature": Column(float, Check.in_range(305.0, 315.0)),
    "Rotational speed": Column(int, Check.in_range(1000, 2900)),
    "Torque": Column(float, Check.in_range(3.0, 80.0)),
    "Tool wear": Column(int, Check.in_range(0, 253)),
    "Failure_Type": Column(int, Check.isin([0, 1, 2, 3, 4]))
})

def fix_dtypes(df):
    df = df.copy()
    df['Rotational speed'] = df['Rotational speed'].astype('int64')
    df['Tool wear']        = df['Tool wear'].astype('int64')
    df['Failure_Type']     = df['Failure_Type'].astype('int64')
    return df

train   = fix_dtypes(train)
current = fix_dtypes(current)
stress  = fix_dtypes(stress)

# TODO: Validate train and current
schema.validate(train)
schema.validate(current)
print("Train and current datasets validated successfully.")

# TODO: Validate stress with lazy=True and print violation summary
try:
    schema.validate(stress, lazy=True)
except pa.errors.SchemaErrors as err:
    print("Stress dataset validation errors summary:")
    print(err.failure_cases)

