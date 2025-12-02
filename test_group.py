import pandas as pd

# simple categorize function matching the one added to main.py

def categorize_details(details: str) -> str:
    d = str(details).lower()
    if any(k in d for k in ["lulu", "spinneys", "noon", "amazon", "book", "supermarket", "hypermarket"]):
        return "Groceries & Shopping"
    if any(k in d for k in ["uber", "taxi", "careem", "metro", "transport"]):
        return "Transport"
    if any(k in d for k in ["etihad", "booking", "hilton", "airways", "hotel", "flight"]):
        return "Travel"
    if any(k in d for k in ["netflix", "spotify", "apple.com bill", "subscription"]):
        return "Subscriptions"
    if any(k in d for k in ["adcb bank fee", "bank fee", "fee"]):
        return "Bank Fees"
    if any(k in d for k in ["card payment received", "payment received", "refund"]):
        return "Income"
    if any(k in d for k in ["insurance", "emirates insurance"]):
        return "Insurance"
    if any(k in d for k in ["zomato", "uber eats", "restaurant", "dining"]):
        return "Food & Dining"
    return "Other"


def main():
    df = pd.read_csv('sample_data.csv')
    df.columns = [c.strip() for c in df.columns]
    # clean Amount
    df['Amount'] = df['Amount'].astype(str).str.replace(',', '').astype(float)
    df['Category'] = df['Details'].apply(categorize_details)
    grouped = df.groupby('Category', as_index=False)['Amount'].sum().sort_values('Amount', ascending=False)
    print(grouped.to_string(index=False))

if __name__ == '__main__':
    main()
