# DiceRollingBot (Fate) v1.2
1.0v Simple dice rolling bot for discord (for dnd and stuff). Trying to improve my Python skills!<br />	
It's just a discord bot which rolls the dice... FOR NOW!<br />
1.1v Added error handling<br />
1.2v Fate is capable of playing music from YouTube, thanks to <br /> 
https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
<h2>Text channel commands:</h2>
!fate - Shows this message;<br />
!files - Generates server JSON file (type it in as first command!);<br />
!tracker - Shows battle tracker;<br />
!add [Name] [Initiative mod] [Dex score] - Adds character to the battle tracker (initiative roll);<br />
!delete [Name] - Deletes character from the battle tracker;<br />
!clear - Clears the battle tracker (and end battle if it's turned on);<br />
!battle - Turns on/off battle mode (only works while tracker isn't empty);<br />
!done - Ends turn of a player while in battle mode;<br />
!r [dice] - Rolls the dice. Example: d20, 2d20 (two d20), 2d20A (advantage roll), 2d20D (disadvantage roll), d20+10 (roll with mod);<br />
<h2>Voice channel commands:</h2>
!join - Connects bot to the voice channel;<br />
!play [url] - Starts to play music from given YouTube URL;<br />
!leave - Disconnects bot from the voice channel (stops the music);<br />
!pause - Pauses playback of music;<br />
!resume - Resumes playback of music;<br />
