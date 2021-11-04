# DiceRollingBot (Fate) v1.2
Simple dice rolling bot for discord (for dnd and stuff). Trying to improve my Python skills!<br />	
It's just a discord bot which rolls the dice... FOR NOW!<br />
Fate is capable of playing music from YouTube, thanks to <br /> 
https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
<h2>Text channel commands:</h2>
!fate - to see this message;<br />
!files - generates server JSON file (type it in as first command!);<br />
!tracker - to see tracker;<br />
!add [Name] [Initiative mod] [Dex score] - to add character to the tracker (initiative roll);<br />
!delete [Name] - to delete character from the tracker;<br />
!clear - to clear the tracker (and end battle if it's turned on);<br />
!battle - to turn on the battle mode (only works while tracker isn't empty);<br />
!done - to end turn in battle mode;<br />
!r [dice] - to roll the dice. Example: d20, 2d20 (two d20), 2d20A (advantage roll), 2d20D (disadvantage roll), d20+10 (roll with mod);<br />
<h2>Voice channel commands:</h2>
!join - bot will join users voice channel;<br />
!play [url] - starts playing music from given YouTube URL;<br />
!leave - bot will disconnect from voice channel;<br />
!pause - you know what it does;<br />
!resume - you know what it does;<br />
