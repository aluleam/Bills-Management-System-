#ifndef MANAGEMENT_H
#define MANAGEMENT_H

#include <string>
#include <vector>

enum ExpenseCategory { GROCERY, GAS, PERSONAL, OTHER_FOODS, MORE_STUFF };
enum Bill { MORTGAGE, ELECTRICITY, PHONE_BILL, PERSONAL_LOAN, CAR_LOAN, CREDIT_PAYMENT, TRASH };

class Management
{
private:
    struct IncomeRecord
    {
        double hourlyRate;
        double hoursWorked;
        double weekendHours;
        double totalPayment;
        std::string date;
    };

    struct ExpenseRecord
    {
        double amount;
        ExpenseCategory category;
        std::string date;
    };

    std::vector<IncomeRecord> incomeRecords;
    std::vector<ExpenseRecord> expenseRecords;

public:
    Management();
    void manageIncome(double hourlyRate, double hoursWorked, double weekendHours, char workedWeekend, double weekendAdditionalRate);
    void saveIncomeRecord(const IncomeRecord& record);
    void saveWeeklyData();
    void displayMonthlySummary();
    std::string getMonthlySummary();
    std::vector<IncomeRecord> getIncomeRecords();
    void addExpense(double amount, ExpenseCategory category, const std::string& date);
    void saveExpenseRecord(const ExpenseRecord& record);
    void provideRecommendations();
};

extern "C" {
    Management* Management_new() { return new Management(); }
    void Management_manageIncome(Management* m, double hourlyRate, double hoursWorked, double weekendHours, char workedWeekend, double weekendAdditionalRate) {
        m->manageIncome(hourlyRate, hoursWorked, weekendHours, workedWeekend, weekendAdditionalRate);
    }
    void Management_displayMonthlySummary(Management* m) { m->displayMonthlySummary(); }
    void Management_delete(Management* m) { delete m; }
    const char* Management_getMonthlySummary(Management* m) {
        static std::string summary;
        summary = m->getMonthlySummary();
        return summary.c_str();
    }
    IncomeRecord* Management_getIncomeRecords(Management* m, int* size) {
        static std::vector<IncomeRecord> records = m->getIncomeRecords();
        *size = records.size();
        return records.data();
    }
    void Management_addExpense(Management* m, double amount, int category, const char* date) {
        m->addExpense(amount, static_cast<ExpenseCategory>(category), date);
    }
    void Management_provideRecommendations(Management* m) {
        m->provideRecommendations();
    }
}

#endif