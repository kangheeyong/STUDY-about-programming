import createStatementData from './libs/createStatementDataV4.js';
import fs from "fs"

{
  function usd(aNumber) {
    return new Intl.NumberFormat("es-US", {
      style: "currency",
      currency: "USD",
      minimimFractionDigits: 2,
    }).format(aNumber / 100);
  }

  function renderPlainText(data) {
    let result = `청구 내역 (고객명: ${data.customer})\n`;
    for (let perf of data.performances) {
      result += `${perf.play.name}: ${usd(perf.amount)} (${perf.audience}석)\n`;
    }
    result += `총액: ${usd(data.totalAmount)}\n`;
    result += `적립 포인트: ${data.totalVolumeCredits}점\n`;
    return result;
  }

  function statement(invoices, plays) {
    return renderPlainText(createStatementData(invoices, plays));
  }

  function renderHtml(data) {
    let result = `<h1>청구 내역 (고객명: ${data.customer})</h1>\n`;
    result += "<table>\n";
    result += "<tr><th>연극</th><th>좌석 수</th><th>금엑</th></tr>";
    for (let perf of data.performances) {
      result += `<tr><td>${perf.play.name}</td>td>(${perf.audience}석)</td>`;
      result += `<td>${usd(perf.amount)}</td></tr>\n`;
    }
    result += "</table>\n";
    result += `<p>총액: <em>${usd(data.totalAmount)}</em></p>\n`;
    result += `<p>적립 포인트: <em>${data.totalVolumeCredits}</em>점</p>\n`;
    return result;
  }

  function htmlStatement(invoices, plays) {
    return renderHtml(createStatementData(invoices, plays));
  }
  const _invoices = JSON.parse(fs.readFileSync("invoices.json"));
  const _plays = JSON.parse(fs.readFileSync("plays.json"));

  const result = statement(_invoices, _plays);
  console.log(result);

  const result1 = htmlStatement(_invoices, _plays);
  console.log(result1);
}
