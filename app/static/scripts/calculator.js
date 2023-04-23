const csrf_token = $('meta[name=csrf-token]').attr('content');
/**
 * Validates all input fields and calls the calculation function if all fields are valid.
 * @param {Event} event - The event object representing the form submission.
 */
$(document).submit(function(event){
    event.preventDefault()
    let check;
    let test = true;

    check = document.querySelector('input[id="HomeVal"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="DownPay"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="LoanAmt"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="InterestRate"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="LoanTerm"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="PropTax"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="Income"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="Credit"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="CarPay"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="StudentPay"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="HomeInsurance"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="PrivateMortInsurance"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}
    check = document.querySelector('input[id="HOA"]');
    if (!check.checkValidity()){check.reportValidity(); test = false}

    if (test) {
        calculation()
        updateUserDB()
    }
})

/**
 * Updates the loan amount field based on the values of the home value and down payment fields.
 */
function updateLoanAmt() {
    const homeVal = parseFloat(document.getElementById("HomeVal").value);
    const downPay = parseFloat(document.getElementById("DownPay").value);
    document.getElementById("LoanAmt").value = homeVal - downPay;
        }

        /**
         * Calls the calculation function on window load to prime outputs.
         * Attaches event listeners to the HomeVal and DownPay fields on window load.
         * These event listeners will call the updateLoanAmt function when their values change.
         */
        window.onload = function() {
            calculation()
            document.getElementById("HomeVal").addEventListener("input", updateLoanAmt);
            document.getElementById("DownPay").addEventListener("input", updateLoanAmt);
            document.getElementById("DownPay").addEventListener("input", validateDownPayment);

        };

/**
 * Validates that down payment is not greater than home value.
 */
function validateDownPayment() {
    const homeVal = parseFloat(document.getElementById("HomeVal").value);
    const downPay = parseFloat(document.getElementById("DownPay").value);
    const downAlert = document.querySelector('input[id="DownPay"]');
    if (downPay > homeVal) {
        downAlert.setCustomValidity("Cannot be greater than home value.");
        downAlert.reportValidity()
    } else {
        downAlert.setCustomValidity("")
    }
}

/**
 * Validates a given input field and reports its validity status.
 * @param {HTMLElement} input - The input field to be validated.
 */
function validateInput(input) {
  const valid = input.checkValidity();
  if (!valid) {
    input.reportValidity();
  }
}

/**
 * Sends validated data in JSON form to update database for logged-in users.
 */
function updateUserDB(){
    const home = document.getElementById('HomeVal').value;
    const down = document.getElementById('DownPay').value;
    const loan = document.getElementById('LoanAmt').value;
    const interest = document.getElementById('InterestRate').value;
    const loanTerm = document.getElementById('LoanTerm').value;
    const prop = document.getElementById('PropTax').value;
    const an_income = document.getElementById('Income').value;
    const credit = document.getElementById('Credit').value;
    const carPay = document.getElementById('CarPay').value;
    const studentPay = document.getElementById('StudentPay').value;
    const PMI = document.getElementById('PrivateMortInsurance').value;
    const home_insurance = document.getElementById('HomeInsurance').value;
    const HOA = document.getElementById('HOA').value;

    // Sends POST request to update user info in the database
    $.ajax({
    url: '/update_calculator_info',
    type: 'POST',
    contentType: "application/json",
    headers: {'X-CSRFToken': csrf_token},
    data: JSON.stringify({an_income: an_income, home: home, down: down, loan: loan, interest: interest,
        loanTerm: loanTerm, prop: prop, credit: credit, carPay: carPay, studentPay: studentPay, PMI: PMI,
        home_insurance: home_insurance, HOA: HOA})
    })
}

/**
 * Performs mortgage calculations based on user input, updates the UI with calculated values.
 */
function calculation(){

    const home = document.getElementById('HomeVal').value;
    const down = document.getElementById('DownPay').value;
    const loan = document.getElementById('LoanAmt').value;
    const interest = document.getElementById('InterestRate').value / 100;
    const loanTerm = document.getElementById('LoanTerm').value;
    const prop = document.getElementById('PropTax').value;
    const an_income = document.getElementById('Income').value;
    const credit = document.getElementById('Credit').value;
    const carPay = document.getElementById('CarPay').value;
    const studentPay = document.getElementById('StudentPay').value;
    const PMI = document.getElementById('PrivateMortInsurance').value / 100;
    const home_insurance = document.getElementById('HomeInsurance').value;
    const HOA = document.getElementById('HOA').value;

    const mon_income = an_income / 12;
    const mon_payments = (Number(credit) + Number(carPay) + Number(studentPay))
    const loanTermMonth = loanTerm * 12;
    const mon_int = interest / 12;
    const mon_prop_pay = prop / 12;
    const mon_PMI = (loan * PMI) / 12;
    const mon_home_insurance = home_insurance / 12;

    // Fixed Rate Loan
    let mort_Mon_Total = (loan * mon_int * Math.pow(1 + mon_int, loanTermMonth)) / (Math.pow(1 + mon_int, loanTermMonth) - 1);
    let total_mort = mort_Mon_Total * loanTermMonth;

    // Monthly Payments total
    let total_mon_payment= mort_Mon_Total + mon_prop_pay + mon_payments + mon_home_insurance + mon_PMI + Number(HOA)

    let mort_interest = total_mort - loan
    total_mort = total_mort + (prop * 30)

    // Debt to income
    let debt_income_percent = (mon_payments / mon_income) * 100
    let debt_income_budget = (mon_income - mon_payments)
    let debt_income_percent_mort = (total_mon_payment / mon_income) * 100
    let debt_income_mort_budget = mon_income - total_mon_payment

    // Down payment percent
    let down_pay_percent = (down / home) * 100

    document.getElementById('MonPayTotal').textContent=Number(total_mon_payment.toFixed(2)).toLocaleString()
    document.getElementById('MortMonTotal').textContent=Number(mort_Mon_Total.toFixed(2)).toLocaleString()
    document.getElementById('TotalMort').textContent=Number(total_mort.toFixed(2)).toLocaleString()
    document.getElementById('TotalInterest').textContent=Number(mort_interest.toFixed(2)).toLocaleString()
    document.getElementById('Debt').textContent=Number(debt_income_percent.toFixed(2)).toLocaleString()
    document.getElementById('DebtBudget').textContent=Number(debt_income_budget.toFixed(2)).toLocaleString()
    document.getElementById('DebtMort').textContent=Number(debt_income_percent_mort.toFixed(2)).toLocaleString()
    document.getElementById('DebtMortBudget').textContent=Number(debt_income_mort_budget.toFixed(2)).toLocaleString()
    document.getElementById('DownPayPercent').textContent=Number(down_pay_percent.toFixed(2)).toLocaleString()

}