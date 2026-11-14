# Gallery

The first section shows grids grown step by step, where a line may hold several sentences. The other sections show the best grids of each scored set, chosen by `make_gallery.py` (combined score of `rank.py`, near duplicates removed). Every row and every column of those is a single sentence from the OpenSubtitles corpus; all words in a grid are distinct. Sentences are shown with the punctuation they most often have in the corpus.

## Grown grids: each line is a sequence of sentences

One growth run of `grow.py` from a 4x4 grid (4x4 -> 4x7 -> 7x7 -> 7x10 -> 10x10 -> 10x13 -> 13x13). All words of a grid are distinct. When the grid could not grow any more, rarer sentences were admitted (the next level). Shown: the largest grid of each level.

### 10x10, level 0

Sentences admitted at this level, by minimum corpus count: 3-word 50+, 4-word 10+, 5-word 10+, 6-word 10+, 7-word 10+. Fluency -4.48.

<pre class="wide">
oh     but    i       couldn't um     it's   okay  how'd they      do
no     it     cannot  be       well   not    all   we    saw       that
you    can't  trust   anyone   that's bad    right get   him       again
don't  hurt   anybody else     good   luck   then  there what      is
sure   come   in      what's   he     want   now   he's  a         she
you're on     the     inside   got    to     move  so    beautiful here
ok     kiddo  fire    me       better watch  out   big   day       today
just   like   his     daddy    she's  my     mom   i'll  find      one
call   your   father  i'm      too    young  let's have  another   beer
her    mother died    sorry    old    friend go    this  way       please
</pre>

Across:

- Oh, but I couldn't. Um, it's okay. How'd they do?
- No, it cannot be. Well, not all. We saw that.
- You can't trust anyone. That's bad, right? Get him again.
- Don't hurt anybody else. Good luck, then. There what is?
- Sure, come in. What's he want now? He's a she.
- You're on the inside. Got to move. So beautiful here.
- Ok, kiddo, fire me. Better watch out. Big day today.
- Just like his daddy. She's my mom. I'll find one.
- Call your father. I'm too young. Let's have another beer.
- Her mother died. Sorry, old friend. Go this way, please.

Down:

- Oh, no, you don't. Sure you're ok? Just call her.
- But it can't hurt. Come on, kiddo. Like your mother.
- I cannot trust anybody. In the fire. His father died.
- Couldn't be anyone else. What's inside me? Daddy, I'm sorry.
- Um, well that's good. He got better. She's too old.
- It's not bad luck. Want to watch? My young friend.
- Okay, all right then. Now move out! Mom, let's go!
- How'd we get there? He's so big. I'll have this.
- They saw him. What a beautiful day. Find another way.
- Do that again. Is she here today? One beer, please.

### 13x13, level 1

Sentences admitted at this level, by minimum corpus count: 2-word 500+, 3-word 20+, 4-word 7+, 5-word 7+, 6-word 7+, 7-word 7+. Fluency -4.72.

<pre class="wide">
oh       but         i            couldn't um      it's   okay       how'd    they      do     where's  everybody going
no       it          cannot       be       well    not    all        we       saw       that   dad      sit       down
you      can't       trust        anyone   that's  bad    right      get      him       again  hang     tight     everyone
don't    hurt        anybody      else     good    luck   then       there    what      is     up       and       back
sure     come        in           what's   he      want   now        he's     a         she    they're  cut       off
you're   on          the          inside   got     to     move       so       beautiful here   really   very      nice
ok       kiddo       fire         me       better  watch  out        big      day       today  pretty   hot       huh
just     like        his          daddy    she's   my     mom        i'll     find      one    two      four      six
call     your        father       i'm      too     young  let's      have     another   beer   maybe    five      minutes
her      mother      died         sorry    old     friend go         this     way       please three    months    ago
he'll    say         yes          we're    waiting yeah   we'll      see      uh        hey    stop     at        nothing
eat      something   everything's ready    for     who    hear       ye       last      man    standing which     was
anything interesting fine         sir      someone knew   everything tomorrow night     look   around   point     taken
</pre>

Across:

- Oh, but I couldn't. Um, it's okay. How'd they do? Where's everybody going?
- No, it cannot be. Well, not all. We saw that. Dad, sit down.
- You can't trust anyone. That's bad, right? Get him again. Hang tight, everyone.
- Don't hurt anybody else. Good luck, then. There what is? Up and back.
- Sure, come in. What's he want now? He's a she. They're cut off!
- You're on the inside. Got to move. So beautiful here. Really, very nice.
- Ok, kiddo, fire me. Better watch out. Big day today. Pretty hot, huh?
- Just like his daddy. She's my mom. I'll find one. Two, four, six.
- Call your father. I'm too young. Let's have another beer. Maybe five minutes.
- Her mother died. Sorry, old friend. Go this way, please. Three months ago.
- He'll say yes. We're waiting. Yeah, we'll see. Uh, hey. Stop at nothing.
- Eat something. Everything's ready. For who? Hear ye! Last man standing. Which was?
- Anything interesting? Fine, sir. Someone knew everything. Tomorrow night. Look around. Point taken.

Down:

- Oh, no, you don't. Sure you're ok? Just call her. He'll eat anything.
- But it can't hurt. Come on, kiddo. Like your mother. Say something interesting.
- I cannot trust anybody. In the fire. His father died. Yes, everything's fine.
- Couldn't be anyone else. What's inside me? Daddy, I'm sorry. We're ready, sir.
- Um, well that's good. He got better. She's too old. Waiting for someone?
- It's not bad luck. Want to watch? My young friend. Yeah, who knew?
- Okay, all right then. Now move out! Mom, let's go! We'll hear everything.
- How'd we get there? He's so big. I'll have this. See ye tomorrow.
- They saw him. What a beautiful day. Find another way. Uh, last night.
- Do that again. Is she here today? One beer, please. Hey, man, look.
- Where's dad? Hang up. They're really pretty. Two, maybe three. Stop standing around!
- Everybody sit tight. And cut. Very hot. Four, five months? At which point?
- Going down. Everyone, back off! Nice, huh? Six minutes ago. Nothing was taken.

## 4x4, sentences seen 7+ times, at least 5 uncommon words

265 grids scored; no names; uncommon = outside the 300 most frequent words.

```
oh       but      i        couldn't
no       it       cannot   be
you      can't    trust    anyone
don't    hurt     anybody  else
```

Across: Oh, but I couldn't. No, it cannot be. You can't trust anyone. Don't hurt anybody else.

Down: Oh, no, you don't. But it can't hurt. I cannot trust anybody. Couldn't be anyone else.

```
um        actually  uh        hey
no        i         can't     move
we        shouldn't do        it
don't     drink     that      asshole
```

Across: Um, actually, uh, hey. No, I can't move. We shouldn't do it. Don't drink that, asshole.

Down: Um, no, we don't. Actually, I shouldn't drink. Uh, can't do that. Hey, move it, asshole!

```
here's  what    we      found
where   exactly were    you
it      was     quite   easy
is      that    close   enough
```

Across: Here's what we found. Where exactly were you? It was quite easy. Is that close enough?

Down: Here's where it is. What exactly was that? We were quite close. Found you easy enough.

```
oh      and     you're  welcome
yeah    i'm     trying  to
it's    not     too     soon
me      working hard    enough
```

Across: Oh, and you're welcome. Yeah, I'm trying to. It's not too soon. Me, working hard enough?

Down: Oh, yeah, it's me. And I'm not working. You're trying too hard. Welcome to soon enough.

```
that's what   i      wish
where  d'you  want   me
you    call   this   luck
cut    it     out    dude
```

Across: That's what I wish. Where d'you want me? You call this luck? Cut it out, dude.

Down: That's where you cut. What d'you call it? I want this out. Wish me luck, dude.

```
oh        but       you       shouldn't
no        mom       don't     be
i         won't     accept    this
wouldn't  go        that      far
```

Across: Oh, but you shouldn't! No, mom, don't be. I won't accept this. Wouldn't go that far.

Down: Oh, no, I wouldn't. But mom won't go. You don't accept that? Shouldn't be this far.

```
it's    that    i       won't
what    happens will    happen
he      doesn't teach   anymore
is      it      him     though
```

Across: It's that I won't. What happens, will happen. He doesn't teach anymore. Is it him, though?

Down: It's what he is. That happens, doesn't it? I will teach him. Won't happen anymore, though.

```
ah      i       hear    you
i'd     hate    me      too
like    being   a       teacher
that    poor    little  boy
```

Across: Ah, I hear you. I'd hate me, too. Like being a teacher. That poor little boy.

Down: Ah, I'd like that. I hate being poor. Hear me a little. You too teacher boy.

```
and      now      it's     you
so       what     about    children
i        have     to       run
shall    we       start    upstairs
```

Across: And now it's you. So, what about children? I have to run. Shall we start upstairs?

Down: And so I shall. Now what have we? It's about to start. You children run upstairs.

```
but    i'm    no     fool
you    gonna  charge me
don't  answer at     once
forget it     all    right
```

Across: But I'm no fool. You gonna charge me? Don't answer at once. Forget it, all right?

Down: But you don't forget. I'm gonna answer it. No charge at all. Fool me once, right?

```
if      i       can't   sleep
you     cannot  go      inside
don't   lose    it      tonight
leave   him     alone   okay
```

Across: If I can't sleep. You cannot go inside. Don't lose it tonight. Leave him alone, okay?

Down: If you don't leave. I cannot lose him. Can't go it alone. Sleep inside tonight, okay?

```
well       apparently it         is
maybe      neither    was        he
they       are        all        gone
aren't     you        finished   yet
```

Across: Well, apparently it is. Maybe neither was he. They are all gone. Aren't you finished yet?

Down: Well, maybe they aren't. Apparently, neither are you. It was all finished. Is he gone yet?

```
but      i        don't    shoot
you      wouldn't push     him
never    touch    me       again
forget   it       right    now
```

Across: But I don't shoot. You wouldn't push him? Never touch me again. Forget it right now.

Down: But you never forget. I wouldn't touch it. Don't push me, right? Shoot him again now!

```
well      actually  you       can't
maybe     i         could     win
we        shouldn't eat       them
don't     drink     it        all
```

Across: Well, actually, you can't. Maybe I could win. We shouldn't eat them. Don't drink it all.

Down: Well, maybe we don't. Actually, I shouldn't drink. You could eat it. Can't win them all.

```
but      i        wouldn't anyway
what     do       you      wish
are      not      like     me
we       drink    to       luck
```

Across: But I wouldn't anyway. What do you wish? Are not like me. We drink to luck.

Down: But what are we? I do not drink. Wouldn't you like to? Anyway, wish me luck.

## 4x4, sentences seen 10+ times, at least 4 uncommon words

365 grids scored; no names; uncommon = outside the 300 most frequent words.

```
uh       actually i        don't
no       it       wouldn't work
you      might    say      so
can't    be       that     hard
```

Across: Uh, actually, I don't. No, it wouldn't work. You might say so. Can't be that hard.

Down: Uh, no, you can't. Actually, it might be. I wouldn't say that. Don't work so hard.

```
that's what   i      wish
where  d'you  want   me
you    call   this   luck
cut    it     out    dude
```

Across: That's what I wish. Where d'you want me? You call this luck? Cut it out, dude.

Down: That's where you cut. What d'you call it? I want this out. Wish me luck, dude.

```
oh       but      i        can't
no       you      couldn't be
we       didn't   walk     far
don't    run      away     now
```

Across: Oh, but I can't. No, you couldn't be. We didn't walk far. Don't run away now.

Down: Oh, no, we don't. But you didn't run. I couldn't walk away. Can't be far now.

```
but      he       never    did
i        wouldn't forget   you
didn't   have     a        name
dare     to       face     him
```

Across: But he never did. I wouldn't forget you. Didn't have a name. Dare to face him.

Down: But I didn't dare. He wouldn't have to. Never forget a face. Did you name him?

```
well      no        they      don't
obviously i         wouldn't  know
he        can't     accept    that
didn't    tell      you       either
```

Across: Well, no, they don't. Obviously, I wouldn't know. He can't accept that! Didn't tell you, either.

Down: Well, obviously he didn't. No, I can't tell. They wouldn't accept you. Don't know that either.

```
but      i        couldn't come
we       wouldn't be       here
don't    touch    that     please
forget   it       right    now
```

Across: But I couldn't come. We wouldn't be here. Don't touch that, please. Forget it right now.

Down: But we don't forget. I wouldn't touch it. Couldn't be that, right? Come here, please now.

```
well      maybe     you       shouldn't
no        we        can't     be
i         should    change    this
wouldn't  go        that      far
```

Across: Well, maybe you shouldn't. No, we can't be. I should change this. Wouldn't go that far.

Down: Well, no, I wouldn't. Maybe we should go. You can't change that. Shouldn't be this far.

```
but   he    read  you
it's  just  the   start
your  left  damn  it
turn  this  thing off
```

Across: But he read you. It's just the start. Your left, damn it. Turn this thing off.

Down: But it's your turn! He just left this. Read the damn thing. You start it off.

```
which  i      don't  get
we     won't  lose   them
can't  see    your   legs
do     you    mind   moving
```

Across: Which I don't get. We won't lose them. Can't see your legs. Do you mind moving?

Down: Which we can't do. I won't see you. Don't lose your mind. Get them legs moving!

```
then     what     are      they
who      did      you      hit
was      she      seeing   anyone
i        want     somebody else
```

Across: Then what are they? Who did you hit? Was she seeing anyone? I want somebody else.

Down: Then who was I? What did she want? Are you seeing somebody? They hit anyone else?

```
but    he     is     strong
i      got    your   stuff
get    his    ass    here
you    too    fat    boy
```

Across: But he is strong. I got your stuff. Get his ass here. You too, fat boy.

Down: But I get you. He got his, too. Is your ass fat? Strong stuff here, boy.

```
and      i        couldn't answer
you      might    get      me
better   do       it       right
hurry    that     up       now
```

Across: And I couldn't answer. You might get me. Better do it right. Hurry that up now.

Down: And you better hurry. I might do that. Couldn't get it up. Answer me right now!

```
that's  where   i       play
why     you     took    it
i'm     taking  her     back
leaving me      there   again
```

Across: That's where I play. Why you took it. I'm taking her back. Leaving me there again?

Down: That's why I'm leaving. Where you taking me? I took her there. Play it back again.

```
i      don't  trust  anyone
won't  let    me     in
push   him    on     that
you    leave  this   room
```

Across: I don't trust anyone. Won't let me in? Push him on that. You leave this room.

Down: I won't push you. Don't let him leave. Trust me on this. Anyone in that room.

```
how     can     we      not
could   i       have    another
you     read    every   word
forget  it      right   now
```

Across: How can we not? Could I have another? You read every word? Forget it right now.

Down: How could you forget? Can I read it? We have every right. Not another word now!

## 4x4, sentences seen 20+ times

8030 grids scored; names allowed.

```
oh       and      you      don't
no       it       couldn't be
she      didn't   do       this
doesn't  work     that     way
```

Across: Oh, and you don't? No, it couldn't be. She didn't do this. Doesn't work that way.

Down: Oh, no, she doesn't. And it didn't work. You couldn't do that. Don't be this way.

```
yeah   but    you    can't
well   it     might  be
i      didn't say    that
don't  work   so     hard
```

Across: Yeah, but you can't. Well, it might be. I didn't say that. Don't work so hard.

Down: Yeah, well, I don't. But it didn't work. You might say so. Can't be that hard.

```
oh       and      you      don't
no       i        wouldn't mind
we       wanna    do       it
can't    help     that     now
```

Across: Oh, and you don't? No, I wouldn't mind. We wanna do it. Can't help that now.

Down: Oh, no, we can't. And I wanna help. You wouldn't do that. Don't mind it, now.

```
oh      but     you     can't
no      i       never   do
they    didn't  believe it
don't   ask     me      anymore
```

Across: Oh, but you can't. No, I never do. They didn't believe it. Don't ask me anymore.

Down: Oh, no, they don't. But I didn't ask. You never believe me. Can't do it anymore.

```
oh       but      he       did
no       it       was      you
i        couldn't really   say
don't    be       upset    okay
```

Across: Oh, but he did. No, it was you. I couldn't really say. Don't be upset, okay?

Down: Oh, no, I don't. But it couldn't be. He was really upset. Did you say okay?

```
uh     no     it's   not
yeah   you    got    this
i      need   to     shit
did    it     happen again
```

Across: Uh, no, it's not. Yeah, you got this. I need to shit. Did it happen again?

Down: Uh, yeah, I did. No, you need it. It's got to happen. Not this shit again.

```
oh         no         we         can't
so         it's       just       you
i          really     don't      understand
did        not        know       that
```

Across: Oh, no, we can't. So it's just you? I really don't understand. Did not know that.

Down: Oh, so I did. No, it's really not. We just don't know. Can't you understand that?

```
that's what   i      did
why    you    want   it
we've  got    to     go
come   on     move   away
```

Across: That's what I did. Why you want it? We've got to go. Come on, move away.

Down: That's why we've come. What you got on? I want to move. Did it go away?

```
i     can't just  leave
don't you   get   this
wanna take  her   place
move  it    out   now
```

Across: I can't just leave. Don't you get this? Wanna take her place? Move it out now.

Down: I don't wanna move. Can't you take it? Just get her out! Leave this place now!

```
that's how    you    know
where  d'you  want   me
i      like   it     now
was    that   all    right
```

Across: That's how you know. Where d'you want me? I like it now. Was that all right?

Down: That's where I was. How d'you like that? You want it all? Know me now, right?

## 4x5, sentences seen 10+ times

752 grids scored; no names.

```
oh       but      it       couldn't help
no       you      can't    leave    me
i        gotta    get      him      out
don't    go       in       there    now
```

Across: Oh, but it couldn't help! No, you can't leave me! I gotta get him out. Don't go in there now.

Down: Oh, no, I don't. But you gotta go. It can't get in. Couldn't leave him there. Help me out now.

```
oh     yes    so     they   are
no     i      don't  know   you
we     can    do     this   guys
didn't see    that   shit   coming
```

Across: Oh, yes, so they are. No, I don't know you. We can do this, guys. Didn't see that shit coming.

Down: Oh, no, we didn't. Yes, I can see. So, don't do that. They know this shit. Are you guys coming?

```
so    what  did   he    see
why   don't we    ask   him
can't you   get   her   down
i     like  it    out   there
```

Across: So what did he see? Why don't we ask him? Can't you get her down? I like it out there.

Down: So why can't I? What don't you like? Did we get it? He ask her out? See him down there?

```
oh       no       don't    say      that
yes      i        believe  it       will
they     wanted   this     to       happen
have     you      shit     yourself again
```

Across: Oh, no, don't say that. Yes, I believe it will. They wanted this to happen. Have you shit yourself again?

Down: Oh, yes, they have. No, I wanted you. Don't believe this shit. Say it to yourself. That will happen again.

```
why     don't   we      all     go
do      you     have    the     right
i       know    another way     in
try     that    one     over    there
```

Across: Why don't we all go? Do you have the right? I know another way in. Try that one over there.

Down: Why do I try? Don't you know that? We have another one. All the way over. Go right in there.

```
well  what  do    i     say
why   would they  want  her
don't you   have  a     name
we    need  to    try   again
```

Across: Well, what do I say? Why would they want her? Don't you have a name? We need to try again.

Down: Well, why don't we? What would you need? Do they have to? I want a try. Say her name again.

```
and    no     i      don't  look
so     you    wanna  go     out
he     can't  come   in     here
should be     up     there  now
```

Across: And no, I don't look. So you wanna go out? He can't come in here. Should be up there now.

Down: And so he should. No, you can't be. I wanna come up. Don't go in there. Look out here now.

```
well      we        gotta     try       something
yeah      don't     get       me        wrong
i         want      to        come      with
did       it        work      on        you
```

Across: Well, we gotta try something! Yeah, don't get me wrong. I want to come with. Did it work on you?

Down: Well, yeah, I did. We don't want it. Gotta get to work. Try me, come on. Something wrong with you?

```
that's why    you've come   back
what   you    got    on     me
i      want   to     go     up
get    some   rest   out    here
```

Across: That's why you've come back. What you got on me? I want to go up. Get some rest out here.

Down: That's what I get. Why, you want some? You've got to rest. Come on, go out. Back me up here.

```
but   what  did   you   say
how   do    ya    like  it
can   i     hear  that  again
they  need  me    right now
```

Across: But what did you say? How do ya like it? Can I hear that again? They need me right now.

Down: But how can they? What do I need? Did ya hear me? You like that, right? Say it again now!

```
but      what     if       we're    not
how      are      they     doing    that
can      you      believe  this     shit
i        stuck    it       together again
```

Across: But what if we're not? How are they doing that? Can you believe this shit? I stuck it together again.

Down: But how can I? What, are you stuck? If they believe it. We're doing this together. Not that shit again.

```
well      what      did       you       say
why       would     he        do        it
can't     they      get       anything  right
i         want      something else      now
```

Across: Well, what did you say? Why would he do it? Can't they get anything right? I want something else now.

Down: Well, why can't I? What would they want? Did he get something? You do anything else? Say it right now.

## 3x5, rows seen 10+ times, columns 100+ times

873 grids scored; no names.

```
well  why   don't you   run
i     can't even  do    it
can   we    try   this  again
```

Across: Well, why don't you run? I can't even do it. Can we try this again?

Down: Well, I can. Why can't we? Don't even try. You do this. Run it again.

```
oh       why      didn't   you      ask
i        wouldn't have     hurt     him
say      it       to       me       again
```

Across: Oh, why didn't you ask? I wouldn't have hurt him. Say it to me again.

Down: Oh, I say. Why wouldn't it? Didn't have to. You hurt me. Ask him again.

```
but    i      can't  fuck   you
we     can    do     this   guys
didn't see    that   shit   coming
```

Across: But I can't fuck you. We can do this, guys. Didn't see that shit coming.

Down: But we didn't. I can see. Can't do that. Fuck this shit. You guys coming?

```
no     i      just   sit    in
you    can't  come   over   here
don't  go     up     there  please
```

Across: No, I just sit in. You can't come over here! Don't go up there, please.

Down: No, you don't. I can't go. Just come up. Sit over there. In here, please.

```
so     why    don't  you    leave
i      didn't even   miss   it
did    he     ask    her    out
```

Across: So why don't you leave? I didn't even miss it. Did he ask her out?

Down: So I did. Why didn't he? Don't even ask. You miss her. Leave it out.

```
because he      didn't  do      it
i       can     have    you     killed
can't   wait    to      see     him
```

Across: Because he didn't do it. I can have you killed. Can't wait to see him.

Down: Because I can't. He can wait. Didn't have to. Do you see? It killed him.

```
oh     no     you    did    not
i      can    smell  it     now
don't  do     that   again  please
```

Across: Oh, no, you did not! I can smell it now. Don't do that again, please.

Down: Oh, I don't. No can do. You smell that? Did it again. Not now, please.

```
i'm   sure  he'll call  you
okay  i'll  take  him   out
now   hold  it    up    there
```

Across: I'm sure he'll call you. Okay, I'll take him out. Now, hold it up there.

Down: I'm okay now. Sure, I'll hold. He'll take it. Call him up. You out there?

```
but   i     don't get   you
we    gotta talk  it    out
can't go    back  in    there
```

Across: But I don't get you. We gotta talk it out. Can't go back in there.

Down: But we can't. I gotta go. Don't talk back. Get it in. You out there?

```
no      i       can't   take    that
you     don't   believe me      right
didn't  like    it      down    there
```

Across: No, I can't take that. You don't believe me, right? Didn't like it down there?

Down: No, you didn't. I don't like. Can't believe it. Take me down. That right there.

## 3x5, sentences seen 20+ times, at least 2 uncommon words

2278 grids scored; no names; uncommon = outside the 200 most frequent words.

```
because he      didn't  do      it
i       can     have    you     killed
don't   try     to      follow  me
```

Across: Because he didn't do it. I can have you killed. Don't try to follow me.

Down: Because I don't. He can try. Didn't have to. Do you follow? It killed me.

```
but     i       can't   go      back
you     wanna   get     through this
don't   see     it      that    way
```

Across: But I can't go back. You wanna get through this? Don't see it that way.

Down: But you don't. I wanna see. Can't get it. Go through that. Back this way.

```
so    why   don't you   leave
we    can't even  touch him
shall i     try   it    on
```

Across: So why don't you leave? We can't even touch him. Shall I try it on?

Down: So we shall. Why can't I? Don't even try. You touch it. Leave him on.

```
no        i'm       sure      you       didn't
there's   something i         don't     get
nobody    else      could     answer    it
```

Across: No, I'm sure you didn't. There's something I don't get. Nobody else could answer it.

Down: No, there's nobody. I'm something else. Sure I could. You don't answer. Didn't get it.

```
no     you    can't  come   in
i      wanna  get    outta  here
don't  go     up     there  please
```

Across: No, you can't come in. I wanna get outta here. Don't go up there, please.

Down: No, I don't. You wanna go? Can't get up. Come outta there! In here, please.

```
well   why    don't  you    try
i      didn't even   see    it
did    he     ask    her    out
```

Across: Well, why don't you try? I didn't even see it. Did he ask her out?

Down: Well, I did. Why didn't he? Don't even ask. You see her? Try it out.

## 3x6, sentences seen 10+ times

1096 grids scored; no names; many 3-word columns are fragments, see the report.

```
oh     no     i      don't  think  so
can    we     just   forget about  this
you    can't  do     it     that   way
```

Across: Oh, no, I don't think so. Can we just forget about this? You can't do it that way.

Down: Oh, can you? No, we can't. I just do. Don't forget it. Think about that. So this way.

```
then   why    can't  we     talk   now
i      don't  even   have   to     look
didn't you    tell   me     that   honey
```

Across: Then why can't we talk now? I don't even have to look. Didn't you tell me that, honey?

Down: Then I didn't. Why don't you? Can't even tell. We have me. Talk to that. Now, look, honey.

```
well   i'm    glad   that   you're here
it's   good   to     be     back   right
you    guys   hear   me     in     there
```

Across: Well, I'm glad that you're here. It's good to be back, right? You guys hear me in there?

Down: Well, it's you. I'm good, guys. Glad to hear. That be me. You're back in. Here, right there.

```
oh    no    you   don't have  to
can't we    just  let   it    go
i     won't leave her   here  alone
```

Across: Oh, no, you don't have to. Can't we just let it go? I won't leave her here alone.

Down: Oh, can't I? No, we won't. You just leave. Don't let her. Have it here. To go alone.

```
well    he      never   told    me      that
i       don't   want    you     doing   it
can't   wait    to      see     what    happens
```

Across: Well, he never told me that. I don't want you doing it. Can't wait to see what happens.

Down: Well, I can't. He don't wait. Never want to. Told you, see? Me, doing what? That it happens?

```
but   it's  not   why   i'm   here
i     got   to    go    all   right
don't you   die   on    me    now
```

Across: But it's not why I'm here. I got to go, all right? Don't you die on me now.

Down: But I don't. It's got you. Not to die. Why go on? I'm all me. Here right now.
