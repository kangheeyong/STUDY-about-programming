{
  function amountFor(aPerformance) {
    let result = 0;

    switch (playFor(aPerformance).type) {
      case "tragedy":
        result = 40000;
        if (aPerformance.audience > 30) {
          result += 1000 * (aPerformance.audience - 30);
        }
        break;
      case "comedy":
        result = 30000;
        if (aPerformance.audience > 20) {
          result += 10000 + 500 * (aPerformance.audience - 20);
        }
        result += 300 * aPerformance.audience;
        break;
      default:
        throw new Error(`알 수 없는 장르 : $(playFor(aPerformance).type)`);
    }
    return result;
  }

  function playFor(aPerformance) {
    return plays[aPerformance.playID];
  }

  function statement(invoices, plays) {
    let totalAmount = 0;
    let volumeCredits = 0;
    let result = `청구 내역 (고객명: ${invoices.customer})\n`;

    const format = new Intl.NumberFormat("es-US", {
      style: "currency",
      currency: "USD",
      minimimFractionDigits: 2,
    }).format;

    for (let perf of invoices.performances) {
      volumeCredits += Math.max(perf.audience - 30, 0);
      if ("comedy" == playFor(perf).type)
        volumeCredits += Math.floor(perf.audience / 5);

      result += `${playFor(perf).name}: ${format(amountFor(perf) / 100)} (${perf.audience}석)\n`;
      totalAmount += amountFor(perf);
    }
    result += `총액: ${format(totalAmount / 100)}\n`;
    result += `적립 포인트: ${volumeCredits}점\n`;
    return result;
  }

  const fs = require("fs");

  const invoices = JSON.parse(fs.readFileSync("invoices.json"));
  const plays = JSON.parse(fs.readFileSync("plays.json"));

  const result = statement(invoices, plays);

  console.log(result);
}
