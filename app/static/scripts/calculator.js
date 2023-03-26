function calculation(){
    // Test log to make sure function call works
    //console.log('test')
    const home = document.getElementById('HomeVal').value;
    const down = document.getElementById('DownPay').value;
    const loan = document.getElementById('LoanAmt').value;
    const interest = document.getElementById('InterestRate').value / 100;
    const loanTerm = document.getElementById('LoanTerm').value;
    const prop = document.getElementById('PropTax').value;
    const loanType = document.getElementById('LoanType').value;
    let n = loanTerm * 12;


    let propPay = prop / 12
    // Fixed Rate Loan
    let total =(loan * (interest/12) * Math.pow(1 + interest/12, n)) / (Math.pow(1 + interest/12, n) - 1)
    total += propPay
    // Proof of concept of the math
    //let total = (100000 * (.06/12)*Math.pow(1+.06/12, 30*12)) / (Math.pow(1+.06/12, 30*12) - 1)

    //document.getElementById('MortTotal').textContent=L
    document.getElementById('MortTotal').textContent=Number(total.toFixed(2)).toLocaleString()

    return false
}