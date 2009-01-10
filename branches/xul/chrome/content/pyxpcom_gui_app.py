import mozutils
from backend.bibleinterface import biblemgr
import sys

def pyxpcom_gui_app_doCommand(event):
    item_name = event.target.id
    if item_name == "menu_FileQuitItem":
        mozutils.doQuit(forceQuit=False)
    elif item_name == "menu_About":
        arguments = None
        window.openDialog("chrome://pyxpcom_gui_app/content/about.xul", "about", "centerscreen,modal", arguments)
    elif item_name == "menu_Extensions":
        arguments = None
        window.openDialog("chrome://mozapps/content/extensions/extensions.xul?type=extensions", "about", "centerscreen,modal", arguments)		

def go(event):
	print "HERE"
	item = document.getElementById("toolbar_location")
	assert item
	#item.value = item.value + "test"
	print item.value
	t = biblemgr.bible.GetChapter(
		item.value
	)
	try:
		text = (t.replace(
			'br class="verse_per_line"','br /'))
		
		print `text`
		#open("text", "w").write(text)
		#text = open("text").read()

		#.replace(
#			'&', '&amp;'))#* 0 + \
		'''
<a href = "#1" name="1" target="1"><small><sup>1</sup></small></a> 
The revelation of Jesus Christ, which God  
<small><a href="bible:John 17:7-8">John 17:7-8</a> <a href="bible:John 8:26">John 8:26</a> <a href="bible:John 14:10">John 14:10</a></small> 
gave him  
<small><a href="bible:Rev 22:6">Rev 22:6</a></small> 
to show to his servants the things that must soon take place.  
<small><a href="bible:Rev 22:16">Rev 22:16</a></small> 
He made it known by sending his angel to his servant John, 
<br />
		<a href = "#2" name="2" target="2"><small><sup>2</sup></small></a>  
<small><a href="bible:John 19:35">John 19:35</a></small> who bore witness to the word of God and to  
		<small>
		<a href="bible:Rev 6:9">Rev 6:9</a>
		<a href="bible:Rev 12:17">Rev 12:17</a> 
		<b>
			<a href= "bible:?values=2&amp;val0=Rev+19%3A10&amp;val1=1Cor+1%3A6">...</a>
		</b>
		</small>
		the testimony of Jesus Christ, even  
		
<small><a href="bible:Rev 1:11">Rev 1:11</a> <a href="bible:Rev 1:19">Rev 1:19</a></small> to all that he saw. <br />
		<a href = "#3" name="3" target="3"> 
		<small><sup>3</sup></small></a> 
<small><a href="bible:Rev 22:7">Rev 22:7</a> <a href="bible:Luke 11:28">Luke 11:28</a> <b><a href = "bible:?values=2&amp;val0=John+8%3A51&amp;val1=1John+2%3A3">...</a></b></small> Blessed is the one who reads aloud the words of this prophecy, and blessed are those who hear, and who keep what is written in it,  
<small><a href="bible:Rev 22:10">Rev 22:10</a> <a href="bible:1John 2:18">1John 2:18</a> <a href="bible:Rom 13:11">Rom 13:11</a></small> for the time is near. <br /> <br />
<a href = "#4" name="4" target="4">
<small><sup>4</sup></small></a>     John to the seven churches that are in Asia:<br /><br />Grace to you and peace from  
<small><a href="bible:Rev 1:8">Rev 1:8</a> <a href="bible:Rev 4:8">Rev 4:8</a> <a href="bible:Heb 13:8">Heb 13:8</a></small> him  
<small><a href="bible:Exod 3:14">Exod 3:14</a></small> who is and  
<small><a href="bible:John 1:1">John 1:1</a></small> who was and who is to come, and from  
<small><a href="bible:Rev 3:1">Rev 3:1</a> <a href="bible:Rev 4:5">Rev 4:5</a> <a href="bible:Rev 5:6">Rev 5:6</a></small> the seven spirits who are before his throne, <br />
<a href = "#5" name="5" target="5">
<small><sup>5</sup></small></a> and from Jesus Christ  
<small><a href="bible:Rev 3:14">Rev 3:14</a> <a href="bible:John 18:37">John 18:37</a> <b><a href = "bible:?values=4&amp;val0=1Tim+6%3A13&amp;val1=Rev+2%3A13&amp;val2=Ps+89%3A37&amp;val3=Isa+55%3A4">...</a></b></small> the faithful witness,  
<small><a href="bible:Col 1:18">Col 1:18</a> <a href="bible:Ps 89:27">Ps 89:27</a> <b><a href = "bible:?values=2&amp;val0=Acts+26%3A23&val1=1Cor+15%3A20">...</a></b></small> the firstborn of the dead, and  
<small><a href="bible:Rev 17:14">Rev 17:14</a> <a href="bible:Rev 19:16">Rev 19:16</a> <a href="bible:Ps 89:27">Ps 89:27</a></small> the ruler of kings on earth.<br /><br />To  
<small><a href="bible:John 13:34">John 13:34</a> <a href="bible:John 15:9">John 15:9</a></small> him who loves us and  
<small><a href="bible:1Pet 1:18-19">1Pet 1:18-19</a></small> has freed us from our sins by his blood <br />
<a href = "#6" name="6" target="6">
<small><sup>6</sup></small></a> and made us  
<small><a href="bible:Rev 5:10">Rev 5:10</a> <a href="bible:Rev 20:6">Rev 20:6</a> <a href="bible:1Pet 2:9">1Pet 2:9</a></small> a kingdom,  
<small><a href="bible:Rev 5:10">Rev 5:10</a> <a href="bible:Rev 20:6">Rev 20:6</a> <a href="bible:1Pet 2:9">1Pet 2:9</a></small> priests to  
<small><a href="bible:Rom 15:6">Rom 15:6</a></small> his God and Father, to him be  
<small><a href="bible:Rom 11:36">Rom 11:36</a></small> glory and  
<small><a href="bible:1Pet 4:11">1Pet 4:11</a></small> dominion forever and ever. Amen. <br />
<a href = "#7" name="7" target="7">
<small><sup>7</sup></small></a> Behold,  
<small><a href="bible:Dan 7:13">Dan 7:13</a> <a href="bible:Matt 16:27">Matt 16:27</a></small> he is coming with the clouds, and  
<small><a href="bible:Zech 12:10">Zech 12:10</a> <a href="bible:John 19:37">John 19:37</a></small> every eye will see him, even those who pierced him, and all tribes of the earth will wail on account of him. Even so. Amen. <br /> <br />
<a href = "#8" name="8" target="8">
<small><sup>8</sup></small></a>  
<small><a href="bible:Rev 21:6">Rev 21:6</a> <a href="bible:Rev 22:13">Rev 22:13</a> <b><a href = "bible:?values=3&val0=Isa+41%3A4&val1=Isa+43%3A10&val2=Isa+44%3A6">...</a></b></small> &#8220;I am the Alpha and the Omega,&#8221; says the Lord God,  
<small><a href="bible:Rev 1:4">Rev 1:4</a></small> &#8220;who is and who was and who is to come, the Almighty.&#8221; <br /> <br />
<a href = "#9" name="9" target="9">
<small><sup>9</sup></small></a> I, John, your brother and  
<small><a href="bible:Phil 4:14">Phil 4:14</a></small> partner in  
<small><a href="bible:John 16:33">John 16:33</a></small> the tribulation and  
<small><a href="bible:2Tim 2:12">2Tim 2:12</a></small> the kingdom and  
<small><a href="bible:Rev 3:10">Rev 3:10</a></small> the patient endurance that are in Jesus, was on the island called Patmos  
<small><a href="bible:Rev 1:2">Rev 1:2</a></small> on account of the word of God and the testimony of Jesus. <br />
<a href = "#10" name="10" target="10">
<small><sup>10</sup></small></a>  
<small><a href="bible:Rev 4:2">Rev 4:2</a> <a href="bible:Rev 17:3">Rev 17:3</a> <b><a href = "bible:?values=5&val0=Rev+21%3A10&val1=1Kgs+18%3A12&val2=Ezek+3%3A12&val3=Matt+22%3A43&val4=2Cor+12%3A2">...</a></b></small> I was in the Spirit  
<small><a href="bible:Acts 20:7">Acts 20:7</a> <a href="bible:1Cor 16:2">1Cor 16:2</a></small> on the Lord\'s day, and I heard behind me a loud voice  
<small><a href="bible:Rev 4:1">Rev 4:1</a></small> like a trumpet <br />
<a href = "#11" name="11" target="11">
<small><sup>11</sup></small></a> saying,  
<small><a href="bible:Rev 1:2">Rev 1:2</a> <a href="bible:Rev 1:19">Rev 1:19</a></small> &#8220;Write what you see in a book and send it to the seven churches, to Ephesus and to Smyrna and to Pergamum and to Thyatira and to Sardis and to Philadelphia and to Laodicea.&#8221; <br /> <br />
<a href = "#12" name="12" target="12">
<small><sup>12</sup></small></a> Then I turned to see the voice that was speaking to me, and on turning I saw  
<small><a href="bible:Rev 1:20">Rev 1:20</a> <a href="bible:Rev 2:1">Rev 2:1</a> <b><a href = "bible:?values=4&val0=Exod+25%3A37&val1=2Chr+4%3A20&val2=Zech+4%3A2&val3=Rev+11%3A4">...</a></b></small> seven golden lampstands, <br />
<a href = "#13" name="13" target="13">
<small><sup>13</sup></small></a> and in the midst of the lampstands  
<small><a href="bible:Dan 7:13">Dan 7:13</a></small> one like  
<small><a href="bible:Rev 14:14">Rev 14:14</a> <a href="bible:Dan 10:16">Dan 10:16</a></small> a son of man,  
<small><a href="bible:Dan 10:5">Dan 10:5</a></small> clothed with a long robe and  
<small><a href="bible:Rev 15:6">Rev 15:6</a></small> with a golden sash around his chest. <br />
<a href = "#14" name="14" target="14">
<small><sup>14</sup></small></a>  
<small><a href="bible:Dan 7:9">Dan 7:9</a></small> The hairs of his head were white like wool, as white as snow.  
<small><a href="bible:Rev 2:18">Rev 2:18</a> <a href="bible:Rev 19:12">Rev 19:12</a> <a href="bible:Dan 10:6">Dan 10:6</a></small> His eyes were like a flame of fire, <br />
<a href = "#15" name="15" target="15">
<small><sup>15</sup></small></a>  
<small><a href="bible:Ezek 1:7">Ezek 1:7</a> <a href="bible:Dan 10:6">Dan 10:6</a></small> his feet were like burnished bronze, refined in a furnace, and  
<small><a href="bible:Rev 14:2">Rev 14:2</a> <a href="bible:Rev 19:6">Rev 19:6</a> <a href="bible:Ezek 43:2">Ezek 43:2</a></small> his voice was like the roar of many waters. <br />
<a href = "#16" name="16" target="16">
<small><sup>16</sup></small></a>  
<small><a href="bible:Rev 1:20">Rev 1:20</a> <a href="bible:Rev 2:1">Rev 2:1</a> <a href="bible:Rev 3:1">Rev 3:1</a></small> In his right hand he held seven stars,  
<small><a href="bible:Rev 19:15">Rev 19:15</a> <a href="bible:Rev 2:12">Rev 2:12</a> <b><a href = "bible:?values=4&val0=Rev+2%3A16&val1=Isa+49%3A2&val2=Eph+6%3A17&val3=Heb+4%3A12">...</a></b></small> from his mouth came a sharp two-edged sword, and  
<small><a href="bible:Matt 17:2">Matt 17:2</a></small> his face was like the sun shining  
<small><a href="bible:Judg 5:31">Judg 5:31</a></small> in full strength. <br /> <br />
<a href="#17" name="17" target="17">
<small><sup>17</sup></small></a>  
<small><a href="bible:Dan 8:17-18">Dan 8:17-18</a> <a href="bible:Dan 10:9-10">Dan 10:9-10</a> <b><a href = "bible:?values=3&val0=Dan+10%3A15&val1=Luke+24%3A37&val2=John+21%3A12">...</a></b></small> When I saw him, I fell at his feet as though dead. But  
<small><a href="bible:Dan 8:17-18">Dan 8:17-18</a> <a href="bible:Dan 10:9-10">Dan 10:9-10</a> <b><a href = "bible:?values=3&val0=Dan+10%3A15&val1=Luke+24%3A37&val2=John+21%3A12">...</a></b></small> he laid his right hand on me,  
<small><a href="bible:Matt 17:7">Matt 17:7</a></small> saying, &#8220;Fear not,  
<small><a href="bible:Rev 2:8">Rev 2:8</a> <a href="bible:Rev 22:13">Rev 22:13</a> <b><a href = "bible:?values=3&val0=Isa+41%3A4&val1=Isa+44%3A6&val2=Isa+48%3A12">...</a></b></small> I am the first and the last, <br />
<a href = "#18" name="18" target="18">
<small><sup>18</sup></small></a> and the living one.  
<small><a href="bible:Rom 6:9">Rom 6:9</a> <a href="bible:Rom 14:9">Rom 14:9</a></small> I died, and behold I am alive forevermore, and  
<small><a href="bible:Rev 9:1">Rev 9:1</a> <a href="bible:Rev 20:1">Rev 20:1</a></small> I have the keys of Death and Hades. <br />
<a href = "#19" name="19" target="19">
<small><sup>19</sup></small></a>  
<small><a href="bible:Rev 1:2">Rev 1:2</a> <a href="bible:Rev 1:11">Rev 1:11</a></small> Write therefore  
<small><a href="bible:Rev 1:12-16">Rev 1:12-16</a></small> the things that you have seen, those that are and those that are to take place after this. <br />
<a href = "#20" name="20" target="20">
<small><sup>20</sup></small></a> As for the mystery of the seven stars that you saw in my right hand, and  
<small><a href="bible:Rev 1:12">Rev 1:12</a></small> the seven golden lampstands, the seven stars are the angels of the seven churches, and  
<small><a href="bible:Matt 5:14-15">Matt 5:14-15</a></small> the seven lampstands are the seven churches.'''#  <br /ss="verse_per_line"', "br /")
		document.getElementById("browser").contentWindow.document.body.innerHTML = text

	except Exception, e:
		print e, dir(e), e.args, e.errno, e.message
		UMAX = 2*(sys.maxint+1)
		print hex(e.errno+UMAX)
		raise

	# Write something to the textbox
def write( msg, *args):
    tb = document.getElementById("output_box")
    tb.value = tb.value + (msg % args) + "\n"
	
