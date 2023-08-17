# Pipes Bot 🤖

Discord bot hobby project turned into useful online assistant. Permanently deployed on a low-power arm based SBC in my home lab. 

Key features include:
- a spotify keyword search for finding relevant music
- OpenAI's GPT implementation
- gas price reporting
- pollen count reporting (Georgia)
- setting reminders
- a weekday morning news report to my subscribed friends
- wishing people happy birthday
- various fun responses to group chat messages

![pipes bot profile picture](./doc/images/pfp_small.PNG)
<br />
**Pipes Bot's Profile**

## Usage
The bot runs permanently on my home server. Chat with it by messaging `Pipes Bot#8120` on Discord (ID 924431531777359943). Try the following commands:
- `$pollen`: to see Atlanta's pollen count
- `$gas [state]`: to see average state gas prices. Replace [state] with a state name or 2-letter initials
- `$spotify [keyword]`: to perform a spotify search for music relating to a keyword of your choice. It might take 5 or more minutes due to rate limiting.
- `$pipesbot, [query]`: to ask davinci gpt-3 a query.
- `$uptime`: to get bot uptime 
- `dennys`: surprise classic
- `$birthday [mm-dd-yyyy]`: Pipes Bot will remember your birthday and wish you a happy birthday on your birthday
- `$remindme, [mm-dd-yyyy], [hh-mm], [reminder]`: Pipes Bot will remind you on a specified date and time of your reminder
- `$reminders`: will return all self-made reminders
- `$reminders delete [num]`: will delete a reminder when passed in the reminder number (1-N)

## Screenshots

**Scheduled Reports**
<br />
![morning report](./doc/images/morning_report.PNG)

**Davinci GPT Implmentation**
<br />
![gpt-3](./doc/images/davinci_gpt.PNG)

**Pipes Bot occasionally reacts to random text in group chats.**
<br />
![sheeesh](./doc/images/sheeesh.PNG)

**Gas Price Command**
<br />
![gas prices](./doc/images/gas.PNG)

**Uptime Command**
<br />
![uptime](./doc/images/uptime.PNG)