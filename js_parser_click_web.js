items = document.querySelectorAll('[class="C6elUkpjAU1xq4ntlQuUMw=="]');
result = [];

yearElement = document.querySelector('div[class="tIXK4SGrK53HT1kOYRoVsA== Mxv5rNWRqhU1ta0CbgLiKQ=="]');
yearText = yearElement ? yearElement.textContent.trim().replace(/\s+/g, ' ') : '';
year = yearText.split(' ')[1] || '1970';

items.forEach(item => {
  const dateElement = item.closest('div[class="_2ACjU8QQdEDky-BFegYT9w=="]').querySelector('span');
  const dateTimeString = dateElement.textContent.trim();
  const [dateString, timeString] = dateTimeString.split(", ");
  
  const [day, month] = dateString.split(' ');
  const dayFormatted = day.padStart(2, '0');
  
  const months = {
    "January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06",
    "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"
  };
  const monthNumber = months[month];

  const dateFormatted = `${year}-${monthNumber}-${dayFormatted}`;

  const timeElement = item.querySelector('div[class="HfSoSyAsHGXbnL61eIYMTw=="] div');
  const time = timeElement ? timeElement.textContent.trim() : "";
  const [hour, minute] = time.split(':');
  const timeFormatted = `${hour.padStart(2, '0')}:${minute.padStart(2, '0')}`;

  const title = item.querySelector('[class="e7a430cJZvOgampuks98fQ=="]').textContent.trim();

  const amountElement = item.querySelector('#amount');
  let amount = amountElement ? amountElement.textContent.trim() : "0";
  
  // Проверяем знак (плюс или минус)
  const parent = amountElement.closest('span');
  const isNegative = parent.textContent.includes('-');
  const isPositive = parent.textContent.includes('+');
  
  if (isNegative) {
    amount = `-${amount}`;
  } else if (!isPositive) {
    // Если знака "+" нет, оставляем как есть (считаем положительным)
    amount = amount;
  }

  result.push(`${dateFormatted} ${timeFormatted} - ${title} - ${amount}`);
});

console.log(result.reverse().join('\n'));
