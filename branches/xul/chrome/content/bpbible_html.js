$(document).ready(function() {
	var off = $(".currentverse").offset();
	var t = off.top;
	var l = off.left;
	/* Try and keep in middle
	 -40 is to correct for verse length, as we do not want start of 
	 verse to start half way down, but the middle to be in the middle */
	t -= window.innerHeight / 2 - 40;
	window.scrollTo(l, t);
});
