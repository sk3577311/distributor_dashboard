import csv
from django.core.management.base import BaseCommand
from dashboard.models import Transaction, Customer, Product, Merchant, Distributor,Commission
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Import transactions from a CSV file, allowing duplicates for non-unique fields'
    def add_arguments(self, parser):
        parser.add_argument('transaction_data', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['transaction_data']
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)

            # Loop through each row in the CSV
            for row in reader:
                try:
                    # Get or create related Distributor
                    distributor, distributor_created = Distributor.objects.get_or_create(
                        distributor_id=row['distributor_id'],
                        defaults={
                            'distributor_name': row['distributor_name'],
                            'username': row['distributor_name']}
                    )

                    # Get or create related Merchant
                    merchant, merchant_created = Merchant.objects.get_or_create(
                        merchant_id=row['merchant_id'],
                        defaults={'merchant_name': row['merchant_name']}
                    )

                    # Get or create related Customer
                    customer, customer_created = Customer.objects.get_or_create(
                        customer_id=row['customer_id'],
                        defaults={'customer_name': row['customer_name']}
                    )

                    # Get or create related Transaction
                    commission, commission_created = Commission.objects.get_or_create(
                        commission_percentage = row['commission_percentage'],
                        category =  row['category'],
                    )
                    # Get or create related Product
                    product, product_created = Product.objects.get_or_create(
                        product_id=row['product_id'],
                        defaults={
                            'product_name': row['product_name'], 
                            'category': commission,
                            'price':row['price']}
                    )
                    product.save()
                    # Parse the date field to a datetime object
                    date = parse_datetime(row['date'])
                    
                    # Handle transaction creation or skipping
                    transaction, created = Transaction.objects.get_or_create(
                        transaction_id=row['transaction_id'],  # Ensure transaction_id is unique
                        date= date,
                        customer= customer,
                        product= product,
                        merchant= merchant,
                        distributor=distributor,
                        commission=commission
                        
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Transaction {row['transaction_id']} imported successfully."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Duplicate transaction {row['transaction_id']} found. Skipping."))

                except Exception as e:
                    # If an error occurs, log it
                    self.stdout.write(self.style.ERROR(f"Failed to import transaction {row['transaction_id']}: {e}"))

#     help = 'Loads data from a CSV file into the database'

#     def add_arguments(self, parser):
#         parser.add_argument('transaction_data', type=str, help='Path to the CSV file')

#     def handle(self, *args, **options):
#         csv_file = options['transaction_data']

#         with open(csv_file, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:

#                 # Create or get existing related objects
#                 distributor,_ = Distributor.objects.get_or_create(distributor_name=row['distributor_name'],distributor_id=row['distributor_id'])
#                 customer,_ = Customer.objects.get_or_create(customer_name=row['customer_name'],customer_id=row['customer_id'])
#                 merchant,_ = Merchant.objects.get_or_create(merchant_name=row['merchant_name'],merchant_id=row['merchant_id'])
#                 product,_ = Product.objects.get_or_create(
#                     product_id=row['product_id'],
#                     product_name=row['product_name'],
#                     product_category=row['category'],
#                     price=row['price']
#                 )

#                 # Create the transaction
#                 Transaction(
#                     transaction_id = row['transaction_id'],
#                     date=row['date'],  # Assuming date format is YYYY-MM-DD
#                     customer=customer,
#                     product=product,
#                     merchant=merchant,
#                     distributor=distributor
#                 )

#                 # Create or update commission (if needed)
#                 ProductCategoryCommission.objects.update_or_create(
#                     category=product,
#                     defaults={'commission_percentage': row['commission_percentage']}
#                 )

#         self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {csv_file}'))


