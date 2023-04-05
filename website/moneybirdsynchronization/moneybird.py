from moneybirdsynchronization.administration import HttpsAdministration

from thaliawebsite import settings


class MoneybirdAPIService:
    def __init__(self, administration_id, api_key):
        self._administration = HttpsAdministration(api_key, administration_id)

    def create_contact(self, contact_data):
        return self._administration.post("contacts", contact_data)

    def update_contact(self, contact_id, contact_data):
        return self._administration.patch(f"contacts/{contact_id}", contact_data)

    def delete_contact(self, contact_id):
        self._administration.delete(f"contacts/{contact_id}")

    def get_or_create_project(self, name):
        if name is None:
            return None

        for project in self._administration.get("projects"):
            if project["name"] == name:
                return project["id"]

        return self._administration.post("projects", {"project": {"name": name}})["id"]

    def create_external_sales_invoice(self, invoice_data):
        return self._administration.post("external_sales_invoices", invoice_data)

    def update_external_sales_invoice(self, invoice_id, invoice_data):
        return self._administration.patch(
            f"external_sales_invoices/{invoice_id}", invoice_data
        )

    def delete_external_invoice(self, invoice_id):
        self._administration.delete(f"external_sales_invoices/{invoice_id}")

    def register_external_invoice_payment(self, invoice_id, payment_data):
        return self._administration.post(
            f"external_sales_invoices/{invoice_id}/payments", payment_data
        )

    def delete_external_invoice_payment(self, invoice_id, payment_id):
        self._administration.delete(
            f"external_sales_invoices/{invoice_id}/payments/{payment_id}"
        )

    def create_financial_statement(self, statement_data):
        return self._administration.post("financial_statements", statement_data)

    def update_financial_statement(self, statement_id, statement_data):
        return self._administration.patch(
            f"financial_statements/{statement_id}", statement_data
        )

    def delete_financial_statement(self, statement_id):
        return self._administration.delete(f"financial_statements/{statement_id}")

    def link_mutation_to_booking(
        self, mutation_id, booking_id, price_base, booking_type="ExternalSalesInvoice"
    ):
        return self._administration.patch(
            f"financial_mutations/{mutation_id}/link_booking",
            {
                "booking_type": booking_type,
                "booking_id": booking_id,
                "price_base": price_base,
            },
        )

    def get_financial_mutation_info(self, mutation_id):
        return self._administration.post(
            "financial_mutations/synchronization", data={"ids": [mutation_id]}
        )

    def unlink_mutation_from_booking(
        self, mutation_id, booking_id, booking_type="Payment"
    ):
        return self._administration.delete(
            f"financial_mutations/{mutation_id}/unlink_booking",
            {"booking_type": booking_type, "booking_id": booking_id},
        )

    # def link_transaction_to_financial_account(self, account_id, new_cash_payments):
    #     financial_mutations_attributes = []
    #     if account_id is None:
    #         return
    #
    #     for payment in new_cash_payments:
    #         payment_response = self._administration.post(
    #             f"external_sales_invoices/{payment.moneybird_external_invoice.moneybird_invoice_id}/payments",
    #             {
    #                 "payment": {
    #                     "payment_date": payment.created_at.strftime("%Y-%m-%d"),
    #                     "price": str(payment.amount),
    #                     "financial_account_id": account_id,
    #                     "invoice_id": payment.moneybird_external_invoice.moneybird_invoice_id,
    #                 }
    #             },
    #         )
    #
    #         financial_mutations_attributes.append(
    #             {
    #                 "date": payment.created_at.strftime("%Y-%m-%d"),
    #                 "amount": str(payment.amount),
    #                 "message": payment.topic,
    #             }
    #         )
    #
    #     if len(financial_mutations_attributes) > 0:
    #         statement_response = self._administration.post(
    #             "financial_statements",
    #             {
    #                 "financial_statement": {
    #                     "financial_account_id": account_id,
    #                     "reference": f"Card payments {datetime.date.today()}",
    #                     "financial_mutations_attributes": financial_mutations_attributes,
    #                 }
    #             },
    #         )
    #         for x, payment in enumerate(new_cash_payments):
    #             payment.moneybird_external_invoice.moneybird_financial_statement_id = (
    #                 statement_response["id"]
    #             )
    #             payment.moneybird_external_invoice.moneybird_financial_mutation_id = (
    #                 statement_response["financial_mutations"][x]["id"]
    #             )
    #             payment.moneybird_external_invoice.save()
    #
    #             mutation_response = self._administration.patch(
    #                 f"financial_mutations/{payment.moneybird_external_invoice.moneybird_financial_mutation_id}/link_booking",
    #                 {
    #                     "booking_type": "ExternalSalesInvoice",
    #                     "booking_id": payment.moneybird_external_invoice.moneybird_invoice_id,
    #                     "price": str(payment.amount),
    #                     "description": payment.topic,
    #                 },
    #             )


def get_moneybird_api_service():
    if (
        settings.MONEYBIRD_ADMINISTRATION_ID is None
        or settings.MONEYBIRD_API_KEY is None
    ):
        raise RuntimeError("Moneybird API key or administration ID not set")
    return MoneybirdAPIService(
        administration_id=settings.MONEYBIRD_ADMINISTRATION_ID,
        api_key=settings.MONEYBIRD_API_KEY,
    )
