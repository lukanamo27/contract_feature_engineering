from typing import TypedDict, Optional


class Contract(TypedDict, total=False):
    claim_date: Optional[str]
    bank: Optional[str]
    loan_summa: Optional[str]
    contract_date: Optional[str]
    summa: Optional[str]


Contracts = list[Contract]
