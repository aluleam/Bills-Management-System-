#include "Management.h"
#include <iostream>
#include <fstream>
#include <limits>
#include <ctime>
#include <iomanip>
#include <sstream>

using namespace std;

Management::Management() {}

void Management::manageIncome(double hourlyRate, double hoursWorked, double weekendHours, char workedWeekend, double weekendAdditionalRate)
{
    // Calculate total payment
    double regularHours = (hoursWorked > 40) ? 40 : hoursWorked;
    double overtimeHours = (hoursWorked > 40) ? (hoursWorked - 40) : 0;
    double totalPayment = (hourlyRate * regularHours) + (hourlyRate * 1.5 * overtimeHours);
    if (workedWeekend == 'Y' || workedWeekend == 'y') {
        totalPayment += ((hourlyRate + weekendAdditionalRate) * weekendHours);
    }

    // Get current date
    time_t t = time(0);
    tm* now = localtime(&t);
    string date = to_string(now->tm_year + 1900) + '-' + to_string(now->tm_mon + 1) + '-' + to_string(now->tm_mday);

    // Create income record
    IncomeRecord record = {hourlyRate, hoursWorked, weekendHours, totalPayment, date};
    incomeRecords.push_back(record);
    saveIncomeRecord(record);
}

void Management::saveIncomeRecord(const IncomeRecord& record)
{
    ofstream file("income_records.txt", ios::app);
    if (file.is_open()) {
        file << fixed << setprecision(2)
             << record.date << ","
             << record.hourlyRate << ","
             << record.hoursWorked << ","
             << record.weekendHours << ","
             << record.totalPayment << endl;
        file.close();
    } else {
        cerr << "Unable to open file for writing." << endl;
    }
}

void Management::saveWeeklyData()
{
    // ......
}

void Management::displayMonthlySummary()
{
    ifstream file("income_records.txt");
    if (file.is_open()) {
        string line;
        double totalPayment = 0.0;
        while (getline(file, line)) {
            size_t pos = 0;
            string token;
            vector<string> tokens;
            while ((pos = line.find(',')) != string::npos) {
                token = line.substr(0, pos);
                tokens.push_back(token);
                line.erase(0, pos + 1);
            }
            tokens.push_back(line);

            double payment = stod(tokens[4]);
            totalPayment += payment;
        }
        file.close();
        cout << "Total Payment for the Month: $" << totalPayment << endl;
    } else {
        cerr << "Unable to open file for reading." << endl;
    }
}

std::string Management::getMonthlySummary() {
    ifstream file("income_records.txt");
    stringstream summary;
    if (file.is_open()) {
        string line;
        double totalPayment = 0.0;
        while (getline(file, line)) {
            size_t pos = 0;
            string token;
            vector<string> tokens;
            while ((pos = line.find(',')) != string::npos) {
                token = line.substr(0, pos);
                tokens.push_back(token);
                line.erase(0, pos + 1);
            }
            tokens.push_back(line);

            double payment = stod(tokens[4]);
            totalPayment += payment;
        }
        file.close();
        summary << "Total Payment for the Month: $" << totalPayment;
    } else {
        summary << "Unable to open file for reading.";
    }
    return summary.str();
}

std::vector<Management::IncomeRecord> Management::getIncomeRecords() {
    vector<IncomeRecord> records;
    ifstream file("income_records.txt");
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            size_t pos = 0;
            string token;
            vector<string> tokens;
            while ((pos = line.find(',')) != string::npos) {
                token = line.substr(0, pos);
                tokens.push_back(token);
                line.erase(0, pos + 1);
            }
            tokens.push_back(line);

            IncomeRecord record;
            record.date = tokens[0];
            record.hourlyRate = stod(tokens[1]);
            record.hoursWorked = stod(tokens[2]);
            record.weekendHours = stod(tokens[3]);
            record.totalPayment = stod(tokens[4]);

            records.push_back(record);
        }
        file.close();
    }
    return records;
}

void Management::addExpense(double amount, ExpenseCategory category, const std::string& date)
{
    ExpenseRecord record = {amount, category, date};
    expenseRecords.push_back(record);
    saveExpenseRecord(record);
}

void Management::saveExpenseRecord(const ExpenseRecord& record)
{
    ofstream file("expense_records.txt", ios::app);
    if (file.is_open()) {
        file << fixed << setprecision(2)
             << record.date << ","
             << record.amount << ","
             << record.category << endl;
        file.close();
    } else {
        cerr << "Unable to open file for writing." << endl;
    }
}

void Management::provideRecommendations()
{
   
}
