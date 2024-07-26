Example Usage:

```python
# Initialize the FeatureClass object
features = FeatureClass(r"path_to_features")

# Get the FeatureClass record count
len(features)
>>> 56743

# Ask the FeatureClass for a generator object of FEATURE_ID values
features["FEATURE_ID"]
>>> <generator object Table.__getitem__ at 0x00000000001>

# Ask the FeatureClass for the next FEATURE_ID value
next(features["FEATURE_ID"])
>>> '000001'

# If called on the FeatureClass object, the generator will always yield the first row
next(features["FEATURE_ID"])
>>> '000001'

# Store the feature id generator in a variable
feature_id_iterator = features["FEATURE_ID"]

# Now calling next will maintain the state of the generator
next(feature_id_iterator)
>>> '000001'
next(feature_id_iterator)
>>> '000002'

# Get the sum of the lengths of all shapes in the featureclass
sum(features.getLength(units="FEET") for feature in features["SHAPE@"])
>>> 700378.849

# Ask the FeatureClass for a generator sorted in descending order on FEATURE_ID
reverse_sorted = features.dsort("FEATURE_ID")
next(reverse_sorted)
>>> '056743'

# Ask the FeatureClass for a generator sorted in forward order on FEATURE_ID
forward_sorted = features.asort("FEATURE_ID")
next(forward_sorted)
>>> '000001'

# Each generator maintains their state
next(reverse_sorted)
>>> '056742'
next(forward_sorted)
>>> '000002'

# Grab the top 5 features by a numeric field and store them in a list
# This specific example will be very memory efficient as it only ever loads
# 5 rows into memory
forward_sorted = features.asort("CALCULATED_LENGTH")
top_5 = [next(forward_sorted) for _ in range(5)]
top_5
>>> [156.04, 155.24, 149.75, 148.0, 144.89]

# If you want a less memory efficient, but more flexible and time efficient solution, 
# you can also load the entire table directly into memory in one line of code:
all_rows = list(features)

# The general idea of this Feature model is to allow you to rapidly create a lot of
# very memory efficient representations of your features and then only consume them
# when needed See below.

# Create a new text field
features.add_field("COMMENTS", type="TEXT")

# Set the default value
features["COMMENTS"] = "NO COMMENT"

# Create iterators
reverse_sorted = features.dsort("FEATURE_ID")
forward_sorted = features.asort("FEATURE_ID")

# All comments are 'NO COMMENT'
next(reverse_sorted)["COMMENTS"]
>>> 'NO COMMENT'
next(forward_sorted)["COMMENTS"]
>>> 'NO COMMENT'

# Update all comments to read 'NEW COMMENT'
with features.editor:
    with features.update_cursor() as cursor:
        for row in as_dict(cursor):
            row['COMMENTS'] = 'NEW COMMENT'
            cursor.updateRow(list(row.values()))

# Get the next value in the existing iterators
next(reverse_sorted)["COMMENTS"]
>>> 'NEW COMMENT'
next(forward_sorted)["COMMENTS"]
>>> 'NEW COMMENT'

# Being able to maintain position in a table while edits are preformed is valuable.
# Just remember that if you do have to do insertions or deletions, iterating through
# a table in this way can cause unexpected side effects.
```
