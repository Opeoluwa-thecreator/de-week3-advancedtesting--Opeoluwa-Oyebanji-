ShopLink is an online marketplace where thousands of orders are processed daily.
This week’s task was to build and test a data pipeline that ensures all order data is valid, normalized, and reliable before analytics are performed.

Even though the raw data looked “clean,” it still contained hidden issues such as:

Negative prices or quantities

Currency symbols in the price field (N2500, $40, 35 dollars)

Mixed casing in payment status (Paid, REFUND, pending)

The goal was to design a modular, testable pipeline that validates and transforms the data correctly — and to write pytest unit tests to ensure every stage performs as expected.


Pipeline Components Overview
1. Reader

Reads the input JSON file (shoplink.json).

Returns a list of dictionaries (rows).

Raises a ValueError for unsupported formats or empty files.

2. Validator

Checks that required fields exist:
order_id, timestamp, item, quantity, price, payment_status, total

Ensures numeric fields are positive.

Skips invalid or incomplete records.

3. Transformer

Converts prices and totals to numeric values (removes symbols like “₦” or “$”).

Normalizes payment status to lowercase (paid, pending, refunded).

Recalculates totals for consistency.

Cleans text fields (trims extra spaces, fixes casing).

4. Analyzer

Calculates overall statistics:

Total revenue

Average revenue

Count of each payment status (paid, pending, refunded)

5. Exporter

Saves the cleaned and validated data to a new JSON file (shoplink_cleaned.json).

6. Pipeline (Integration Layer)

Runs all the above components in order.

Returns a summary dictionary with counts and computed statistics.
