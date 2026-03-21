# expense_agent/enums.py

from enum import StrEnum


class TaxRate(StrEnum):
    STANDARD_10 = "10%"
    REDUCED_8 = "8%"


class TaxCategory(StrEnum):
    TAXABLE_10 = "課税仕入10%"
    TAXABLE_8_REDUCED = "課税仕入8%(軽減)"
    NON_TAXABLE = "非課税"
    OUT_OF_SCOPE = "不課税"


class DebitAccount(StrEnum):
    TRAVEL = "旅費交通費"
    MEETING = "会議費"
    ENTERTAINMENT = "接待交際費"
    SUPPLIES = "消耗品費"
    COMMUNICATION = "通信費"
    BOOKS = "新聞図書費"
    WELFARE = "福利厚生費"
    RENT = "地代家賃"
    UTILITIES = "水道光熱費"
    FEES = "支払手数料"


class CreditAccount(StrEnum):
    CASH = "現金"
    BANK = "普通預金"
    ACCOUNTS_PAYABLE = "未払金"


class PaymentMethod(StrEnum):
    CASH = "現金"
    BANK_TRANSFER = "銀行振込"
    CREDIT_CARD = "クレジットカード"
    IC_CARD = "交通系IC"
    UNKNOWN = "不明"