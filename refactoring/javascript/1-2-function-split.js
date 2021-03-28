{
  function amountFor(perf, play) {
    let thisAmount = 0;

    switch (play.type) {
      case "tragedy":
        thisAmount == 40000;
        if (perf.audience > 30) {
          thisAmount += 1000 * (perf.audience - 30);
        }
        break;
      case "comedy":
        thisAmount = 30000;
        if (perf.audience > 20) {
          thisAmount += 10000 + 500 * (perf.audience - 20);
        }
        thisAmount += 300 * perf.audience;
        break;
      default:
        throw new Error(`알 수 없는 장르 : $(play.type)`);
    }
    return thisAmount;
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
      const play = plays[perf.playID];
      let thisAmount = amountFor(perf, play);

      volumeCredits += Math.max(perf.audience - 30, 0);
      if ("comedy" == play.type) volumeCredits += Math.floor(perf.audience / 5);

      result += `${play.name}: ${format(thisAmount / 100)} (${perf.audience}석)\n`;
      totalAmount += thisAmount;
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
