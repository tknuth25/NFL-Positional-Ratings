# NFL-Positional-Ratings
This project takes the QBR rating commonly used in the NFL today and carries similar metrics to each position. Teams are then compiled as a set number of starters for each position. Player performance is measured against an average performer at the position between 2000 and 2010.

## General
### Adjusted to 2000s standard ratings
-	66.7 set as rating for average performer across all categories in 2000-2010.
- QBs for average calculation limited to those with 50 or more attempts.
	- RBs limited to those with 30 or more attempts.
	- WRs limited to those with 15 or more receptions.
	- Defensive players are limited to players who appeared in at least 10 games.
-	Coefficients set to 1 as average for the 2000-2010 period.
	- Range set to between 0 and 2.375.
	- Values less than 0 are set to 0.
	- Values greater than 2.375 are set to 2.375.
-	All scales standardized to between 0 and 158.3.
-	The denominator of each rating calculation is set so that, after limiting each coefficient to the range of 0 to 2.375, the average rating in the 2000-2010 period is set to 66.7.
-	Position Allocations (ranked and selected by Games Started, Games Played, and Rating):
	- 	QB: 1
	- 	RB: 2
	- 	WR: 3
	- 	TE: 1
	- 	DE: 2
	- 	DT: 2
	- 	LB: 4
	- 	CB: 3
	- 	S: 4
-	Data build limited to 1999-present to accommodate receiver and defense ratings, which are not applicable until 1999 due to statistical availability.

## Position Assignments
Pro-Football Reference listed many positions that not all teams had (eg. BB, ROLB, RILB, etc). To correct for this, several players and positions have been reassigned to improve data coverage and the quality of the regression.
### Reassigned positions
-	DE
	- LDE
	- RDE
	- RDE/LDE
	- LDT/LDE
	- LDE/RDE
	- RDE/LOLB
	- LDE/LDT
	- RDE/LDT
	- DE/DT
	- DL
	- RE
 - FS
	- DB/FS
-	SS
	- SS/LH
	- RH/SS
	- CB/SS
	- SS/RLB
-	FB
	- FB/HB
	- FB/LDE
	- FB/LH
	- FB/RB
	- FB/RDH
	- FB/RH
	- FB/RHB
	- LLB/FB
	- TE/FB
-	DT
	- RDT
	- LDT
	- NT
	- LDT/RDT
	- RDT/LDT
	- NT/DT
	- DT/NT
	- RDE/NT
	- NT/RDT
	- RDT/NT
	- NT/LDT
	- LDE/NT
- CB
	- FS/RCB
	- LCB/RCB
	- RCB/LCB
	- RCB/CB
	- RCB/DB
	- LCB
	- RCB
	- SS/LCB
	- RCB/WR
	- DB
-	HB
	- FS/LH
	- HB/FB
	- LHB/RHB
	- LHB
	- LH/RH
	- LH/RDH
	- LH
	- RH
	- LH/FB
	- LH/QB
	- RH/RE
	- RH/DB
	- RH/LH/FS
	- RH/FB
	- RDH/LH
	- LHB/FB
	- RHB/LHB
	- FL/HB
	- RB/FB
	- HB/LE
	- RHB
	- LDH
	- RDH
-	LLB
	- RCB/LLB
-	QB
	- WR/QB
-	WR
	- WR/WR
-	TE
	- TE/TE
-	LOLB
	- LLB/RDE
	- LBODE
	- LOLB/LLB
	- LLB/ROLB
	- LOLB/ROL
	- LLB/LOLB
-	ROLB
	- RLB/LDE
	- RLB/ROLB
	- ROLB/RIL
	- ROLB/LOL
	- RLB/LLB
	- ROLB/LIL
-	LILB
	- LILB/MLB
	- LILB/RIL
	- LILB/ROL
-	RILB
	- RILB/RLB
	- RILB/LIL
	- RLB/LILB
	- ILB
-	MLB
	- MLB/ROLB
	- LLB/MLB
	- MLB/RLB
	- MLB/LLB
	- MLB/RILB
	- MLB/LILB

### Players Reassigned
-	CB: Darryl Roberts, Avonte Maddox, Rashean Mathis, Brandon Carr, Logan Ryan
-	FS: Xavier McKinney, Kurt Schulz, Cory Hall, Dwight Smith, Devin McCourty, Brent Alexander, James Sanders, Calvin Lowry, Michael Griffin, Erik Harris, C.C. Brown, Reed Doughty, Morgan Burnett, Jordan Babineaux, Earl Thomas, Kyle Dugger, Jabrill Peppers
-	SS: Ainsley Battles, Nick Ferguson, Mike Adams, Quintin Mikell, Bryan Scott, Craig Dahl, Lamar Campbell, Donte Whitner, Calvin Pryor, Daniel Sorensen, Ashtyn Davis, Amani Hooker, Taylor Rapp
-	DT: Chris Jones, Cory Redding, John Browning, Junior Bryant, Cletidus Hunt, John Randle, Sheldon Richardson, Nick Williams, Dexter Lawrence, Christian Barmore, Kenny Clark, Maliek Collins, Leonard Williams, Vita Vea
-	DE: Orpheus Roye, John Copeland, Andre Branch, Mike Wright, Deatrich Wise Jr.
-	MLB: Barry Minter, Jon Beason, Dont'a Hightower, Isaiah Kacyvenski, Paris Lenon
-	ROLB: Pisa Tinoisamoa, Carlos Emmons
-	RILB: Daryl Smith, Paul Worrilow, Jeff Ulbrich, Sean Harris
-	LILB: A.J. Hawk, Josh Bynes
-	LOLB: Rocky Boiman, Jamie Collins, Kevin Hardy, Clint Ingram
-	WR: Olabisi Johnson, Troy Brown, Brad Smith

### Consolidation
-	Removed: BB, B, TB, P, LS, PR, KR, WB, /, C, FL, Missing
-	RB
	- FB
	- HB
-	LB
	- LILB
	- LLB
	- LOLB
	- MLB
	- OLB
	- ROLB
	- RLB
	- RILB
-	S
	- FS
	- SS

## Offense
Calculated coefficients are listed in bold. Any non-bolded figure is set so that approximately 10% of the players receive a perfect score in any one coefficient. In some low variance categories, such as forced fumbles per attempt, the coefficient has been moulded as close to this distribution as possible. The formula for each coefficient and final rating calculation has been listed below.

### Quarterback
-	a = ((Completions/Attempts) - 0.3)***3.466**
-	b = ((Yards/Attempts) - 3)***0.272**
-	c = (Touchdowns/Attempts)***26.453**
-	d = (Interceptions/Attempts)***41.527**
-	Rating = ((a+b+c+d)/**6.044**)*100

### Running back
-	a = ((Yards/Attempts) - 2)***0.914**
-	b = (Touchdowns/Attempts)***32.431**
-	c = 2.375 – ((Fumbles/Attempts)***28.946**)
-	Rating = ((a+b+c)/**4.498**)*100

### Wide Receiver/Tight End
-	a = ((Receptions/Targets) – 0.5)***7.467**
-	b = ((Yards/Receptions) - 7.2)***0.252**
-	c = ((Touchdowns/Receptions) + 0.003)***14.933**
-	Rating = ((a+b+c)/**4.501**)*100

## Defense

### Defensive Line
-	a = (((Tackles for Loss + Sacks)/Games Played) - 0.08))***2.111**
-	b = ((Forced Fumbles/Games Played) + 0.02)***14.510**
-	c = ((Tackles/Games Played) - 1.2)***0.968**
-	d = (Passes Deflected/Games Played)***8.856**
-	Rating = ((a+b+c+d)/**5.568**)*100

### Linebacker
-	a = (((Tackles for Loss + Sacks)/Games Played) - 0.08))***2.698**
-	b = (((Interceptions + Forced Fumbles)/Games Played) + 0.015)***10.624**
-	c = ((Tackles/Games Played) - 1.15)***0.379**
-	d = ((Passes Deflected/Games Played) + 0.04)***4.971**
-	Rating = ((a+b+c+d)/**5.588**)*100

### Defensive Back
-	a = ((Interceptions/Games Played) + 0.05)***6.532**
-	b = ((Passes Deflected/Games Played) + 0.03)***2.422**
-	c = ((Tackles/Games Played) - 1.3)***0.577**
-	Rating = ((a+b+c)/**4.418**)*100

