class FlexibleExpenseSharing:
    def __init__(self, friends):
        self.friends = friends
        self.balances = {friend: 0.0 for friend in friends}

    def add_expense(self, payer, total_amount, shares):
        """
        shares is a dictionary mapping each participant to the exact amount they owe.
        """
        for participant, owed_amount in shares.items():
            self.balances[participant] -= owed_amount
        self.balances[payer] += total_amount

    def calculate_settlement(self):
        creditors = []
        debtors = []

        for friend, balance in self.balances.items():
            rounded_bal = round(balance, 2)
            if rounded_bal > 0.01:
                creditors.append([friend, rounded_bal])
            elif rounded_bal < -0.01:
                debtors.append([friend, -rounded_bal])

        if not debtors and not creditors:
            print("Everyone is settled up!")
            return

        while debtors and creditors:
            debtor, debt_amount = debtors.pop()
            creditor, credit_amount = creditors.pop()

            payment = round(min(debt_amount, credit_amount), 2)
            print(f"{debtor} owes {creditor} : Rs. {payment:.2f}")

            remaining_debt = round(debt_amount - payment, 2)
            remaining_credit = round(credit_amount - payment, 2)

            if remaining_debt > 0.01:
                debtors.append([debtor, remaining_debt])
            if remaining_credit > 0.01:
                creditors.append([creditor, remaining_credit])


if __name__ == "__main__":
    friends = [f.strip() for f in input("Enter names of friends (comma-separated): ").split(",")]
    tracker = FlexibleExpenseSharing(friends)

    while True:
        payer = input("\nWho paid? (or type 'done' to finish): ").strip()
        if payer.lower() == "done":
            break
        if payer not in tracker.balances:
            print(f"'{payer}' is not in the friends list. Try again.")
            continue

        base_amount = float(input("Enter base bill amount (before tax/tip): "))
        tax_percent = float(input("Enter tax/tip percentage (0 if none): "))
        total_amount = round(base_amount * (1 + tax_percent / 100), 2)

        participants = [
            p.strip() for p in input("Enter participants (comma-separated): ").split(",")
        ]

        print("Choose split type: [1] Equal  [2] Exact Amounts  [3] Percentages")
        choice = input("Enter 1, 2, or 3: ").strip()

        shares = {}

        if choice == "1":
            each_share = total_amount / len(participants)
            for p in participants:
                shares[p] = each_share

        elif choice == "2":
            print(f"Enter each person's base share (must add up to {base_amount}):")
            for p in participants:
                person_base = float(input(f"  {p}'s base amount: "))
                # Apply the same tax/tip proportion to each person's item
                shares[p] = person_base * (1 + tax_percent / 100)

        elif choice == "3":
            print("Enter percentage share for each person (must add up to 100):")
            for p in participants:
                pct = float(input(f"  {p}'s percentage: "))
                shares[p] = total_amount * (pct / 100)

        else:
            print("Invalid choice. Skipping this expense.")
            continue

        tracker.add_expense(payer, total_amount, shares)
        print(f"Added expense of Rs. {total_amount:.2f} (including tax/tip).")

    print("\n--- Final Settlement ---")
    tracker.calculate_settlement()