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

    if (test) {
        calculation()
    }
    return false


}

function validateInput(input) {
  const valid = input.checkValidity();
  if (!valid) {
    input.reportValidity();
    return false
  }
}
function calculation(){

    const home = document.getElementById('HomeVal').value;
    const down = document.getElementById('DownPay').value;
    const loan = document.getElementById('LoanAmt').value;
    const interest = document.getElementById('InterestRate').value / 100;
    const loanTerm = document.getElementById('LoanTerm').value;
    const prop = document.getElementById('PropTax').value;
    const loanType = document.getElementById('LoanType').value;
    const loanTermMonth = loanTerm * 12;
    const mon_int = interest / 12;
    const mon_prop_pay = prop / 12


    // Fixed Rate Loan
    let mort_Mon_Total = (loan * mon_int * Math.pow(1 + mon_int, loanTermMonth)) / (Math.pow(1 + mon_int, loanTermMonth) - 1)

    // Adds Property Tax onto monthly total
    mort_Mon_Total += mon_prop_pay

    let total_mort = mort_Mon_Total * loanTermMonth
    let mort_interest = total_mort - loan


    document.getElementById('MortMonTotal').textContent=Number(mort_Mon_Total.toFixed(2)).toLocaleString()
    document.getElementById('TotalInterest').textContent=Number(mort_interest.toFixed(2)).toLocaleString()

    return false
}