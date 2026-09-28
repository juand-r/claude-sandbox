# Report: stranger-than-history

## 1. The argument in three sentences

Three invented claims (paint that reverses gravity, flying spheres that sell sex, spanking
instead of jail) sound crazy. A person in 1901 asked to choose between them and three claims
true in 2007 (relativity, the internet and its pornography, a moral change about race and the
presidency) would find the true ones just as crazy. The idea comes from Robin Hanson's wish
for a fiction that shows how surprising the truth turned out to be; the post states no further
lesson.

## 2. Sources checked

Saved in `data/sources/raz_b2b_narrow/`.

- Hanson's comment on "Making History Available", via the LessWrong GraphQL API
  (comments of post TLKPj4GDXetZuPDH5; `mha_comments.json`), comment _id yWtaX2A8vuAaT9mLA,
  legacyId 19312 (base-36 "ewg" = 19312, matching the post's link), user Robin_Hanson2,
  2007-08-31T23:26:42Z: "That sense of "so strange yet true" is very hard to convey in fiction,
  exactly because it seems too strange to be believable. Which is exactly why we say "truth is
  stranger than fiction." I wonder if one could describe in enough detail a fictional story of
  an alternative reality, a reality that our ancestors could not distinguish from the truth, in
  order to make it very clear how surprising the truth turned out to be." The post's quotation
  matches the last sentence exactly.
- Length contraction and local time: Wikipedia "Length contraction" (raw,
  `wiki_Length_contraction.txt`): "Length contraction was postulated by George FitzGerald
  (1889) and Hendrik Antoon Lorentz (1892) to explain the negative outcome of the
  Michelson–Morley experiment"; "Lorentz proposed a new time variable, the "local time""
  (cited to Lorentz 1895); "Lorentz considered local time not to be "real"". Secondary source,
  cited as such in the note.
- Watkins 1900: BBC News, Tom Geoghegan, "Ten 100-year predictions that came true",
  11 January 2012, https://www.bbc.co.uk/news/magazine-16444966 (`bbc_watkins.txt`):
  "In December of that year ... John Elfreth Watkins wrote a piece published on page eight ...
  Ladies' Home Journal, entitled What May Happen in the Next Hundred Years. He began the article
  with the words: "These prophecies will seem strange, almost impossible,""; and "Man will see
  around the world. Persons and things of all kinds will be brought within focus of cameras
  connected electrically with screens at opposite ends of circuits, thousands of miles at a
  span." Both matched. I did not see the original scan; the note says "as quoted by BBC News,
  2012". Wikipedia ("J. Elfreth Watkins", `wiki_J_Elfreth_Watkins.txt`) attributes the article
  to the curator's son, John Elfreth Watkins Jr.; the note gives the name without "Jr." as the
  BBC does.

## 3. Arithmetic

- Speed of light in mph: 299,792,458 m/s x 3600 s/h / 1609.344 m/mi = 670,616,629.384 mph
  (exact fraction has denominator 1397, so the decimal does not terminate). The post's
  "exactly 670,616,629.2" is off by 0.18 mph and is not exact. Too small to matter (STANDARDS
  2.4 numbers rule); no note.

## 4. Claims about other posts

- "Making History Available", Posted: 2007-08-31; this post Posted: 2007-09-01, so "posted the
  day before" is right. The comment is on that post.

## 5. Items not verified

- The original Ladies' Home Journal scan (only the BBC's quotations).
- Whether the second list's claim about pornography as "one of the primary uses" of the network
  holds; it is a joke (fair defender 3), no note.

## 6. Judgment calls for the editor

1. The selection note (second paragraph) and Response: "the lists are chosen ... The
   comparison ... cannot show how often claims that sound crazy turn out true, and the post
   does not claim that it does." The last clause concedes the fair defender's reply; the note
   exists because readers of the book (Seeing with Fresh Eyes) may take the lesson to be about
   absurdity as evidence. If the editor thinks that is attacking a claim the post does not
   make, the note can be cut to its first two sentences.
2. "worded in ways that make them sound odder": an earlier draft said "worded to sound odd",
   which reads intent; changed to describe effect (2.2.9).
3. The 1901 physics note concedes the public/specialist distinction; the fair defender may say
   the post addresses "you", an ordinary person. The note says as much in its last sentence.
4. Pronouns "he" (Lorentz) are for a historical figure. Watkins: restructured to avoid pronouns.

## Checks

- check_verbatim: OK. raz_check: run, every flag read (see section 6). audit: OK.
- `annotated/preview.sh posts stranger-than-history` builds (build-preview/stranger-than-history.pdf).
- `annotated/notes/stranger-than-history.json` not exported (brief did not ask; editor may run notes_backup.py export).
