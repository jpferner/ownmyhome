function validate(event){
    event.preventDefault()

    let check;
    let test = true;

    check = document.querySelector('input[id="HomeVal"]');
    console.log(check.checkValidity())
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

    if (test) {
        calculation()
    }
    return false


}

function validateInput(input) {
  const valid = input.checkValidity();
  if (!valid) {
    input.reportValidity();
    return false;
  }
}
function calculation(){

    const home = document.getElementById('HomeVal').value;
    const down = document.getElementById('DownPay').value;
    const loan = document.getElementById('LoanAmt').value;
    const interest = document.getElementById('InterestRate').value / 100;
    const loanTerm = document.getElementById('LoanTerm').value;
    const prop = document.getElementById('PropTax').value;
    const loan_type = document.getElementById('LoanType').value;
    const an_income = document.getElementById('Income').value;
    const credit = document.getElementById('Credit').value;
    const carPay = document.getElementById('CarPay').value;
    const studentPay = document.getElementById('StudentPay').value;

    const mon_income = an_income / 12;
    const mon_payments = (Number(credit) + Number(carPay) + Number(studentPay)) * 100

    const loanTermMonth = loanTerm * 12;
    const mon_int = interest / 12;
    const mon_prop_pay = prop / 12;

    console.log(mon_payments)
    console.log(mon_income)

    // Debt to income
    let debt_income_percent = (mon_payments / mon_income)
    console.log(debt_income_percent)
    // Fixed Rate Loan
    let mort_Mon_Total = (loan * mon_int * Math.pow(1 + mon_int, loanTermMonth)) / (Math.pow(1 + mon_int, loanTermMonth) - 1);
    let total_mort = mort_Mon_Total * loanTermMonth;

    // Adds Property Tax onto monthly total
    let total_mon_payment= mort_Mon_Total + mon_prop_pay

    let mort_interest = total_mort - loan
    total_mort = total_mort + (prop * 30)

    document.getElementById('MonPayTotal').textContent=Number(total_mon_payment.toFixed(2)).toLocaleString()
    document.getElementById('MortMonTotal').textContent=Number(mort_Mon_Total.toFixed(2)).toLocaleString()
    document.getElementById('TotalMort').textContent=Number(total_mort.toFixed(2)).toLocaleString()
    document.getElementById('TotalInterest').textContent=Number(mort_interest.toFixed(2)).toLocaleString()
    document.getElementById('Debt').textContent=Number(debt_income_percent.toFixed(2)).toLocaleString()

    return false
}