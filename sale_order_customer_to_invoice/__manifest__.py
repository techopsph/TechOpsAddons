{
    "name": "Sale Order Customer to Invoice",
    "summary": """
        Set a separate field to display the Customer of a Sale Order to an invoice. 
        The serves as a helper field for scenarios where Sale Orders are paid by a different partner.
    """,
    "version": "16.0",
    "category": "Sale",
    "website": "https://techops.ph",
    "author": "EL Abquina, Tech Ops PH",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale_management", "account"],
    "data": [
        "views/account_move.xml",
    ],
}
