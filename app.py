import logging
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample data structures for demonstration
fiat_deposits = [
    {'reference_id': '12345', 'amount': 1000.00, 'currency': 'USD', 'timestamp': datetime(2024, 11, 1, 10, 30)},
    {'reference_id': '12346', 'amount': 500.00, 'currency': 'USD', 'timestamp': datetime(2024, 11, 1, 11, 15)},
]

usdc_transfers = [
    {'reference_id': '12345', 'amount': 1000.00, 'currency': 'USDC', 'timestamp': datetime(2024, 11, 1, 10, 45)},
    {'reference_id': '12346', 'amount': 500.00, 'currency': 'USDC', 'timestamp': datetime(2024, 11, 1, 11, 30)},
]

# Function to reconcile fiat deposits with USDC transfers
def reconcile_transactions(fiat_deposits, usdc_transfers):
    matched_transactions = []
    discrepancies = []

    for deposit in fiat_deposits:
        match_found = False
        for transfer in usdc_transfers:
            if deposit['reference_id'] == transfer['reference_id']:
                if deposit['amount'] == transfer['amount']:
                    logging.info(f"Match found for Reference ID {deposit['reference_id']}")
                    matched_transactions.append({
                        'reference_id': deposit['reference_id'],
                        'fiat_amount': deposit['amount'],
                        'usdc_amount': transfer['amount'],
                        'status': 'Matched',
                        'match_time': datetime.now()
                    })
                    usdc_transfers.remove(transfer)
                    match_found = True
                    break
                else:
                    logging.warning(f"Amount mismatch for Reference ID {deposit['reference_id']}: "
                                    f"Fiat {deposit['amount']} vs USDC {transfer['amount']}")
                    discrepancies.append({
                        'reference_id': deposit['reference_id'],
                        'issue': 'Amount mismatch',
                        'fiat_amount': deposit['amount'],
                        'usdc_amount': transfer['amount'],
                        'timestamp': datetime.now()
                    })
                    match_found = True
                    usdc_transfers.remove(transfer)
                    break
        
        if not match_found:
            logging.error(f"No matching transfer found for Reference ID {deposit['reference_id']}")
            discrepancies.append({
                'reference_id': deposit['reference_id'],
                'issue': 'No matching transfer found',
                'fiat_amount': deposit['amount'],
                'usdc_amount': None,
                'timestamp': datetime.now()
            })

    if discrepancies:
        logging.error(f"Reconciliation completed with {len(discrepancies)} discrepancies found.")
    else:
        logging.info("Reconciliation completed successfully with all matches found.")

    return {
        'matched_transactions': matched_transactions,
        'discrepancies': discrepancies
    }

# Running the function and printing results
result = reconcile_transactions(fiat_deposits, usdc_transfers)
print("Matched Transactions:")
for match in result['matched_transactions']:
    print(match)

print("\nDiscrepancies:")
for discrepancy in result['discrepancies']:
    print(discrepancy)
