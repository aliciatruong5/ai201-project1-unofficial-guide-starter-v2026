# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->
Alicia Truong - corpus: city_guides

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them. adding line

---

# Unit 1

## What This Does

This is a retrieval-augmented question-answering system built on the
`city_guides` corpus — a set of travel guides for a handful of small,
fictional towns, plus regional pages on transport, walking, eating, and
seasons. It answers concrete, factual questions about those towns: train and
bus schedules, how long a walk or museum visit takes, when a town is busiest
or quietest, what things cost, and practical details like cash vs. card or
where the nearest hospital is. Given a question, it retrieves the most
relevant passages from the guides, checks they're actually close enough to be
useful, and generates an answer that names its source — or says it doesn't
have enough information if nothing in the corpus is relevant.


## Chunking Strategy

**Chunk size: 2700 characters (started at 800)**
**Overlap: 150 characters**

I started at the starter's default of 800/120 and changed both numbers after
actually reading the chunks it produced: about two-thirds of them (33 of 51)
ended mid-sentence, because 800 characters lands inside a section on
documents this short. Every guide in `city_guides` is one town written as
4-8 short, self-contained sections (*Getting there*, *Eat and drink*, *When
to go*, each a paragraph or two), and the longest document in the whole
corpus is only 2,510 characters. So rather than hunt for a size that happens
to respect sentence boundaries, I picked a chunk size bigger than any single
document, with an overlap large enough that no document produces a leftover
sliver chunk. That makes "one document" and "one chunk" the same thing — 14
documents in, 14 chunks out, 0 of 14 ending mid-sentence.

The trade-off: a retrieved chunk is now a whole guide rather than just the
relevant section, so on a couple of questions a different Brightwater-
adjacent document edges out the "right" one for the #1 spot by a small
margin. It didn't cost anything in practice — at `TOP_K = 5` the document
that actually contains the answer was still retrieved for all five of my
test questions, just not always ranked first. Given how short these
documents are, finishing every sentence was worth more to me than
finer-grained ranking.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::fallback_split`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

## Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.

## Mixed

**Pellew Sands** has a two-mile seafront that is flat the whole way, and
everything of interest is on it or one street back. The land train runs the
length of the promenade hourly between Easter and September. The beach itself is
hard sand and manageable at low tide.

**Givens Mill** is one flat street along the river. The mill tour involves
stairs and the machinery floor is not accessible; the tearoom and riverside are.

## Difficult

**Kestrelford** is built on a slope and the walk up from the lower car park is
steeper than it looks on a map. There is no transport within the town.

**Halden Bay** is built on three levels connected by stepped lanes. The harbour
front is level; everything above it is not. This is hard going with luggage or a
pushchair, let alone a wheelchair.

**Corry Vale** has no public transport, villages two to four miles apart, and
footpaths rather than pavements. **Elder Ness** is shingle and a single street.

## Practical

The nearest full hospital is in Marchwood. Brightwater has a hospital;
Kestrelford, Halden Bay, Corry Vale, Givens Mill and Elder Ness have minor
injuries units with limited hours or nothing at all.

Mobile coverage is good in the town centres and patchy on the outskirts, and
genuinely absent in parts of Corry Vale.
```

**Chunk 2** — source: `guide_corry_vale.md#0` — produced by: `chunker.py::fallback_split`

```
# Corry Vale

Corry Vale is not a town but a valley containing four villages strung along eleven miles of road. Visitors treat it as one destination and locals emphatically do not. The largest village has 900 people and the smallest has 140.

## Getting there

There is no public transport into the valley beyond a school bus that will carry passengers if there is room. Driving from Brightwater takes 35 minutes on a good road as far as the valley mouth and then 20 more on a poor one. Cycling in is a serious undertaking; the road climbs 400 metres in the first four miles.

## Getting around

Nothing within the valley is walkable from anything else — the villages are two to four miles apart. There is one taxi, based in the largest village, and it must be booked a day ahead. Most visitors drive between villages and walk the footpaths in between.

## Eat and drink

One pub in the largest village serves food seven days a week. A second, in the third village, opens Thursday to Sunday. There is a farm shop at the valley mouth that sells bread, cheese and little else, and it closes at 4pm. Bring supplies; this is not a place with options.

## What to see

The valley itself is the attraction. The footpath network is dense and well marked, and a circuit taking in three of the four villages is about nine miles with 500 metres of ascent. The chapel in the second village is 12th century and always unlocked.

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.

## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

**Chunk 3** — source: `guide_elder_ness.md#0` — produced by: `chunker.py::fallback_split`

```
# Elder Ness

Elder Ness is a headland with a village of 300 on it, a lighthouse, a bird observatory, and very little else. People come for one of three reasons — birds, walking, or a deliberate absence of things to do.

## Getting there

A single road in, which floods at the highest spring tides roughly six times a year for about two hours either side of high water. Tide tables are posted at the turning and are worth reading. No public transport of any kind. Nearest station is Pellew Sands, 40 minutes by road.

## Getting around

On foot. The village is one street. The lighthouse is a 25-minute walk along the shingle, which is harder going than the distance suggests. There is one car park at the village and parking anywhere else on the headland is prohibited and enforced.

## Eat and drink

One pub, serving food 12 to 2 and 6 to 8, closed Mondays. A shop that sells basics and closes at 5pm and all day Sunday. That is the complete list. Visitors staying more than a night bring food with them.

## What to see

The bird observatory takes day visitors and the wardens are generous with their time; spring and autumn migration are the reasons to come. The lighthouse is not open to the public but the walk to it is the point. The shingle beach is dramatic and swimming is genuinely dangerous — there is a strong offshore current and no lifeguard.

## Where to stay

The pub has four rooms and the observatory has dormitory accommodation for members and their guests. Both book up entirely for the migration seasons a year ahead. There is nothing else.

## When to go

April to May and September to October for birds, which is what most visitors come for. Midsummer is pleasant and quiet. Winter is severe, the road floods more often, and the pub reduces to weekends only.

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

**Chunk 4** — source: `guide_halden_bay.md#0` — produced by: `chunker.py::fallback_split`

```
# Halden Bay

Halden Bay is a working fishing port of 8,000 that has picked up a second life as a weekend destination. The two economies sit somewhat awkwardly beside each other and the town is candid about it.

## Getting there

The coast road is the only approach and it is slow — 40 minutes for 22 miles, with the last stretch cut into the cliff. Buses run four times a day. Parking in the town itself is limited to two small lots that fill by 10am on summer weekends; the overflow lot is a 12-minute walk up a hill.

## Getting around

The town is small enough to cross in fifteen minutes but is built on three levels connected by stepped lanes, which makes it hard going with luggage or a pushchair. The harbour front is level; everything above it is not.

## Eat and drink

Seafood, unsurprisingly, and it is genuinely fresh — the boats land in the early morning and the two harbour restaurants buy directly. Prices on the harbour front are roughly double those on Fell Street, one level up, for comparable food. Everything closes by 9pm and much of it closes entirely from November to February.

## What to see

The harbour at 6am when the boats come in is the thing worth setting an alarm for. The coastal path runs in both directions, north to a lighthouse in about two hours and south along the cliffs for as far as you want. The small museum on Fell Street covers the fishing industry and takes 40 minutes.

## Where to stay

Almost entirely holiday lets rather than hotels, which means minimum stays of two or three nights in summer. There is one inn on the harbour. Prices roughly halve outside July and August.

## When to go

June and September are the sweet spot. July and August are busy enough that the parking problem becomes the defining feature of the visit. Winter is dramatic and largely closed. The coastal path is genuinely dangerous in high wind and gets shut.

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

**Chunk 5** — source: `guide_marchwood.md#0` — produced by: `chunker.py::fallback_split`

```
# Marchwood

Marchwood is the regional hub — 180,000 people, the junction everyone changes trains at, and a city most visitors pass through rather than stop in. That is a mistake, though an understandable one, since almost nothing of interest is near the station.

## Getting there

Every railway line in the region meets here, which is the city's defining feature. Trains to Brightwater run every 40 minutes until 11pm. The airport is 20 minutes out by a dedicated bus that runs every 15 minutes and costs more than the equivalent taxi shared between three people.

## Getting around

A tram network of four lines, running every 8 minutes on weekdays and every 15 at weekends, until midnight. A day ticket costs less than two single fares and nobody tells you this at the machine. The centre is walkable but the interesting districts are not adjacent to each other.

## Eat and drink

The best eating is in the Northgate district, a 12-minute tram ride from the station, where about thirty restaurants sit within four streets. The area immediately around the station is uniformly poor and expensive. Marchwood keeps later hours than anywhere else in the region — kitchens serve until 10:30pm, and until midnight on Fridays and Saturdays.

## What to see

The city museum is free and genuinely excellent, particularly the industrial floor. The covered market has operated since 1863 and is at its best on a weekday morning. The canal walk from Northgate to the old lock is 40 minutes and is the thing residents recommend when asked.

## Where to stay

Plentiful and, outside conference weeks, cheap. Northgate is the district worth staying in. Station-area hotels are convenient for an early train and dispiriting for anything else.

## When to go

Any time. This is the one place in the region that works in winter, since almost everything is indoors and nothing closes seasonally. Conference weeks in March and October fill the hotels and double the prices; check before booking.

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question: When is the cheapest time to buy a train ticket from Brightwater?**

**Answer:**

```
(best distance 0.438, cutoff 0.6)

Based on the documents, train tickets are considerably cheaper when booked a week ahead (and are also cheaper booked the day before than on the day). (Source: `guide_regional_transport.md`)

Sources retrieved: guide_brightwater.md, guide_kestrelford.md, guide_regional_transport.md, guide_seasons.md, guide_walking.md
```

**My relevance cutoff: 0.6**

I ran my five in-corpus questions and the five `OUT_OF_SCOPE` questions through
`app.py retrieve` and recorded the top result's distance for each, using the
2700/150 chunking above. The in-corpus group topped out at 0.564; the
out-of-scope group bottomed out at 0.841 — a clean gap of about 0.28 with
nothing on either side of it, so 0.6 sits comfortably in the middle rather
than right against either group. (These numbers moved slightly from an
earlier pass at 800/120 chunking, but the size and location of the gap barely
changed, so I kept the cutoff at 0.6.)

| Question | In corpus? | Best distance |
|---|---|---|
| How many trains run between Brightwater and the regional hub on Sundays? | Yes | 0.381 |
| How often does the Kestrelford bus service run on Saturdays? | Yes | 0.408 |
| What used to occupy the building that is now Brightwater's museum, and when did it close? | Yes | 0.564 |
| When is the cheapest time to buy a train ticket from Brightwater? | Yes | 0.438 |
| What time do most restaurants in Brightwater stop serving food, and what happens on Sundays? | Yes | 0.429 |
| What is the capital of Mongolia? | No | 0.896 |
| How do I change the oil in a diesel engine? | No | 0.908 |
| Who won the 1994 World Cup? | No | 1.060 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.841 |
| How do I write a for loop in Rust? | No | 0.875 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** 
I asked Claude to help me with the chunking strategy like getting the sample chunks. It then started to rewrite the whole chunker.py file. So I just ended up using the command that was given. 


**2.**
I asked Claude to help me test different chunks and overlap sizes to get the answer look more seemless and not cutoff as much. It then started to test different sizes and I would analyze each result to see what size would fit best for what I was looking for. 

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Cited chunk actually contains the section that answers the question | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Named source actually backs the specific fact used | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Full transcript in `results/run_2026-09-23_1644_before.md`. Criterion 3 is a single deterministic pass, so the same number appears in all three run columns.

```
### What used to occupy the building that is now Brightwater's museum, and when did it close? — run 1

- Best distance: 0.5638 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_brightwater.md, guide_regional_transport.md, guide_seasons.md, guide_walking.md

A mill occupied the building that is now Brightwater's museum, and it closed in 1974.

Source: `guide_brightwater.md`
```

This one row is evidence for four of the five criteria at once: the answer
is right (1), it names a source (2), and that source — `guide_brightwater.md`
— is the document that actually contains both the mill/1974 fact and the
museum description, not just a plausible-looking guess (4 and 5). Criterion
3's evidence is the out-of-scope table above: the gate refused all 5 of 5
`OUT_OF_SCOPE` questions with distances (0.841–1.060) well clear of the
0.564 highest in-corpus distance.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Target was 4 of 5; all three runs came back 5 of 5. Not close — every question's answer was traceable to a retrieved chunk in all three runs, not just most of the time. |
| 2 | Every answer names a source | MET | Target was 5 of 5, all three runs came back 5 of 5. Every one of the 15 answers across the three runs included an explicit `Source:`-style line. |
| 3 | Gate stops out-of-corpus questions | MET | Target was 4 of 5; the gate refused 5 of 5. The lowest out-of-scope distance (0.841) was well clear of the highest in-corpus distance (0.564), so this wasn't a borderline call. |
| 4 | Cited chunk actually contains the section that answers the question | MET | Target was 4 of 5; came back 5 of 5 on all three runs. I checked this by hand for each question — e.g. the museum question cites `guide_brightwater.md`, and that document's own text contains both the mill/1974 fact and the museum description, not just the right town in general. |
| 5 | Named source actually backs the specific fact used | MET | Target was 4 of 5; came back 5 of 5 on all three runs. Same manual check as criterion 4: for every question, the document named in the answer was the one that literally contained the cited fact, even though `TOP_K=5` retrieves several similar-looking town guides at once. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

I missed nothing — all five criteria came back 5 of 5 on all three runs. But
two of them (4 and 5) were set specifically to catch a risk I introduced
myself in Milestone 3: my chunk size is bigger than any document, so a
retrieved chunk is a whole guide, not just the section that answers the
question. That should make it *easier* for the model to cite a plausible-
looking but wrong document when two towns share a similar fact. My five test
questions never actually test that: each one asks about a fact that's
distinctive enough (a specific number, a specific closure date) that only
one document was ever a real candidate, so criteria 4 and 5 never had a
chance to be missed — they were never really at stake.

That means "4 of 5" for criteria 4 and 5 was set too low, in the sense that
it's not really measuring what I meant it to measure. I'd tighten it by
adding a sixth-and-seventh kind of test question I don't currently have: one
where two different towns both mention a similar-sounding fact (e.g. two
guides both close "at 9pm," or two both used to be built around a mill), so
retrieval has an actual chance to hand back the wrong document and citation
5 of 5 becomes a real target instead of a foregone one.

## The Improvement

**What I changed:**

Switched `chunker.py::split_documents` from whole-document chunks (2700/150)
to one chunk per `##` section, instead of reverting to the original
800/120 fixed-size window. Every section in `city_guides` is already a
short, complete, self-contained paragraph (*Getting there*, *Eat and
drink*, *When to go*), so splitting on the heading keeps the "no
mid-sentence cuts" property of my current chunking while giving each
chunk back a single, focused topic instead of an entire town's worth of
unrelated sections mixed together.


**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

This is a direct response to a failure I found while testing the Diagnoses
section's own prediction. I asked a harder question designed to stress the
exact risk criteria 4 and 5 were meant to catch: *"Which town's mill closed
down and became a museum, as opposed to a town where the mill is still
working?"* The system answered that there was no such town — wrong.
`guide_brightwater.md`, which literally says its mill "closed in 1974" and
"is now a museum," never made it into the top-5 retrieved chunks at all.
The single sentence that answers the question was diluted inside a
~2,000-character embedding covering six unrelated topics, and `guide_givens_mill.md` —
about a still-*working* mill, topically closer to the question's wording —
out-ranked it instead. Section-level chunking directly targets that
mechanism: it would put "Brightwater's mill closed in 1974, now a museum"
in its own chunk, with nothing else diluting its embedding.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Cited chunk actually contains the section that answers the question | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Named source actually backs the specific fact used | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Full transcript in `results/run_2026-09-25_1603_after.md`.

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

Yes, on the specific thing I changed it for. All five original criteria
still hold at a clean 5 of 5 — switching chunkers didn't break anything —
but the real evidence is the question that motivated the change in the
first place: *"Which town's mill closed down and became a museum, as
opposed to a town where the mill is still working?"* Before the change,
this failed — `guide_brightwater.md` never made it into the top 5 retrieved
chunks, and the system answered that no such town existed. After switching
to section-level chunking, the same question now correctly retrieves
`guide_brightwater.md` and answers "The mill in Brightwater closed down and
is now a museum... whereas Givens Mill is built around a working watermill
that still grinds flour commercially," citing both documents by name.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

Criteria 4 and 5 are only proven against one hard case, not five. The mill/museum question that exposed the original chunking bug, and then confirmed the fix, isn't one of my five official test questions — I found it by hand while writing the Diagnoses section. All five official questions still ask about single, distinctive facts, so 5 of 5 on criteria 4 and 5 is real but narrower evidence than the table makes it look. I ran out of time to add a genuinely ambiguous cross-town question to the official set and re-run the full before/after comparison with it included.


## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I rewrite criteria 4 and 5 with a mixed set of questions from the
start: some asking about a distinctive fact (safe, low ambiguity) and at
least one deliberately built to make two documents look equally relevant,
the way the mill/museum question did by accident. Writing the criteria
before Milestone 3 meant I had no way to know that whole-document chunking
would create that specific risk — but I could still have hedged by
including a harder, more adversarial question up front rather than writing
one for the Diagnoses section after the fact.
