# Announcement drafts

Staging area for the Fall 2026 announcements, carried over from Spring 2026.

Quarto ignores any directory whose name starts with `_`, so nothing in here is
rendered or listed on the site. When an announcement is ready to go live, move
the file into `../posts/`:

```bash
mv _post-drafts/2026-08-30-Welcome_to_DATA_622.qmd posts/
```

The relative links inside the drafts (`../modules/...`, `../images/...`) already
point at the right place from `posts/`, since both directories sit one level
below `website/`. The `.png` files here are copies of the ones the drafts
reference in their `image:` front matter; move the matching image across too.

## How the dates were assigned

Each Spring post was matched to the meetup week it belonged to and shifted by
that week's Spring→Fall offset, so the day of the week is preserved (a Sunday
"Week N" post is still a Sunday). Spring's break week (Apr 6) is dropped and
Fall's Thanksgiving break (Nov 23) is inserted between Week 12 and Week 13.

That repositioning matters: the break moved from after Week 10 to after Week 12.
Any "break is starting / break has ended" language in the Week 10 and Week 11
drafts is therefore in the wrong post now, and has been flagged with a `NOTE`
comment rather than silently reworded.

## What was left in place

Links to the Spring 2026 YouTube recordings were **kept**, since they are the
substance of the vignette posts and may be worth reusing. Every draft containing
one opens with a `TODO` comment. Dead links — the past seminar registration and
the dated event flyers — were removed outright.
