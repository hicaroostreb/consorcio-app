import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate


class ConsortiumSimulator:
    """Simulates a consortium with given financial parameters."""

    def __init__(
        self,
        credit,
        months,
        admin_fee,
        reserve_fee,
        readjust_rate,
        bid_pct,
        bid_month,
    ):
        """
        Initialize consortium simulator with financial parameters.

        Args:
            credit (float): Total credit amount.
            months (int): Number of months for the consortium.
            admin_fee (float): Administrative fee percentage.
            reserve_fee (float): Reserve fee percentage.
            readjust_rate (float): Readjustment rate percentage.
            bid_pct (float): Percentage of the initial credit for the bid.
            bid_month (int): The month in which the bid is applied.
        """
        self.original_credit = credit
        self.months = months
        self.admin_fee = admin_fee / 100
        self.reserve_fee = reserve_fee / 100
        self.readjust_rate = readjust_rate / 100
        self.bid_pct = bid_pct / 100
        self.bid_month = bid_month

        # Calcular os valores iniciais
        self.total_cost = credit * (1 + self.admin_fee + self.reserve_fee)
        self.original_total_cost = self.total_cost
        self.initial_monthly_payment = self.total_cost / months

    def apply_readjustment(self, remaining_balance, month):
        """Apply readjustment to balance and recalculate monthly payment.

        Args:
            remaining_balance (float): Current remaining balance.
            month (int): Current month number.

        Returns:
            tuple: (adjusted_balance, new_monthly_payment)
        """
        remaining_months = self.months - month
        if remaining_months <= 0:
            return remaining_balance, remaining_balance

        # Aplicar reajuste ao saldo devedor
        adjusted_balance = remaining_balance * (1 + self.readjust_rate)
        new_monthly_payment = adjusted_balance / remaining_months

        return adjusted_balance, new_monthly_payment

    def generate_schedule(self):
        """Generate payment schedule with readjustments and bid application.

        Returns:
            pd.DataFrame: Payment schedule as DataFrame.
        """
        schedule = []
        current_date = datetime.now()

        # Inicializar valores
        remaining_balance = self.total_cost
        monthly_payment = self.initial_monthly_payment
        payments_count = 0  # Contador para reajuste a cada 6 pagamentos

        for month in range(1, self.months + 1):
            current_balance = (
                remaining_balance  # Salvar o saldo atual antes das operações
            )

            # Determinar o valor do pagamento
            payment = monthly_payment

            # Para o último mês, o pagamento deve ser igual ao saldo remanescente
            if month == self.months:
                payment = current_balance

            # Verificar se é o mês do lance
            bid_amount = 0
            bid_value = ""
            if month == self.bid_month:
                bid_amount = self.original_total_cost * self.bid_pct
                bid_value = f"R${bid_amount:,.2f}"
                print(f"Applying bid of R${bid_amount:,.2f} in month {month}")

            # Aplicar pagamento mensal
            remaining_balance -= payment
            payments_count += 1  # Incrementar contador de pagamentos

            # Aplicar o lance após o pagamento mensal (se for o mês do lance)
            if month == self.bid_month:
                remaining_balance -= bid_amount
                # Recalcular a parcela imediatamente após aplicar o lance
                remaining_months = self.months - month
                monthly_payment = remaining_balance / remaining_months
                print(
                    f"Recalculating monthly payment after bid: R${monthly_payment:,.2f}"
                )
                print(f"New balance: R${remaining_balance:,.2f}")
                print(f"Remaining months: {remaining_months}")

            # Aplicar reajuste semestral (a cada 6 pagamentos)
            if payments_count == 6:
                remaining_balance, monthly_payment = self.apply_readjustment(
                    remaining_balance, month
                )
                payments_count = 0  # Reiniciar contador de pagamentos

            # Adicionar registro ao cronograma
            schedule.append(
                {
                    "Month": month,
                    "Remaining": self.months - month,
                    "Date": (current_date + timedelta(days=30 * (month - 1))).strftime(
                        "%Y-%m-%d"
                    ),
                    "Payment": f"R${payment:,.2f}",
                    "Bid": bid_value,
                    "Balance": f"R${current_balance:,.2f}",
                }
            )

        return pd.DataFrame(schedule)


def print_schedule(df, title):
    """
    Print formatted payment schedule.

    Args:
        df (pd.DataFrame): DataFrame containing the schedule.
        title (str): Title of the schedule.
    """
    print(f"\n{title}:")
    if len(df) > 20:
        df_head = df.head(10)
        df_tail = df.tail(10)
        df_subset = pd.concat([df_head, df_tail])
        print(tabulate(df_subset, headers="keys", tablefmt="pretty", showindex=False))
    else:
        print(tabulate(df, headers="keys", tablefmt="pretty", showindex=False))


def main():
    """Run consortium simulation with example parameters."""
    simulator = ConsortiumSimulator(
        credit=1_000_000,
        months=240,
        admin_fee=26,
        reserve_fee=0.5,
        readjust_rate=2,
        bid_pct=30,
        bid_month=9,
    )

    schedule = simulator.generate_schedule()
    print_schedule(schedule, "Consortium Payment Schedule with Bid")


if __name__ == "__main__":
    main()
