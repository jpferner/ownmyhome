function calculation(){
    // Test log to make sure function call works
    //console.log('test')

    const h = document.getElementById('HomeVal').value;
    const d = document.getElementById('DownPay').value;
    const L = document.getElementById('LoanAmt').value;
    const I = document.getElementById('InterestRate').value / 100;
    const LT = document.getElementById('LoanTerm').value;
    const P = document.getElementById('PropTax').value;
    const LTE = document.getElementById('LoanType').value;
    const n = LT * 12;


    // Fixed Rate Loan
    let total =(L * (I/12) * Math.pow(1 + I/12, n)) / (Math.pow(1 + I/12, n) - 1)
    // Proof of concept of the math
    //let total = (100000 * (.06/12)*Math.pow(1+.06/12, 30*12)) / (Math.pow(1+.06/12, 30*12) - 1)

    //document.getElementById('MortTotal').textContent=L
    document.getElementById('MortTotal').textContent=total.toFixed(2)

    return false
}