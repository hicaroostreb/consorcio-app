import argparse
import math

def calculate_installment(credit_value, duration, admin_fee_total, reserve_fund_total):
    """
    Calculates the monthly installment for a consortium.

    Args:
        credit_value (float): The total value of the credit.
        duration (int): The duration of the consortium in months.
        admin_fee_total (float): The total administration fee as a
            percentage of the credit value.
        reserve_fund_total (float): The total reserve fund as a
            percentage of the credit value.

    Returns:
        float: The monthly installment amount.
    """
    taxa_adm = (admin_fee_total / 100) * credit_value
    fundo_reserva = (reserve_fund_total / 100) * credit_value
    total_a_pagar = credit_value + taxa_adm + fundo_reserva
    installment = total_a_pagar / duration
    return installment


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate a consortium installment calculation."
    )
    parser.add_argument(
        "--credit_value", type=float, required=True,
        help="The total value of the credit."
    )
    parser.add_argument(
        "--duration", type=int, required=True,
        help="The duration of the consortium in months."
    )
    parser.add_argument(
        "--admin_fee_total", type=float, required=True,
        help="The total administration fee as a percentage of the credit value."
    )
    parser.add_argument(
        "--reserve_fund_total", type=float, required=True,
        help="The total reserve fund as a percentage of the credit value."
    )
    args = parser.parse_args()

    installment = calculate_installment(
        args.credit_value, args.duration, args.admin_fee_total, args.reserve_fund_total
    )

    print(f"Monthly Installment: R$ {installment:.2f}")
