### mdex-chap-count
##### Counts unread chapters translated in English in Mangadex

Mangadex provides excellent [API](https://api.mangadex.org/docs) for using it with different clients beside the beautiful Mangadex website. It has got many functionalities. But, sometimes one may have been not reading manga in Mangadex for a long time. If they want to have a count of how many unread chapters for each manga in their follow list have piled up, they need to look no further! 

In this python script, using Mangadex [personal API token](https://api.mangadex.org/docs/02-authentication/personal-clients/), one can do the counting of all unread chapters, both for each manga and in total. 
- First we activate the API token/refresh it.
- Then we call feed API to create a list of all manga in the follow list, their name, id, chapter count
- Now we do the actual counting of how many chapters are unread
  - first we count total chapter using another API again if needed
  - then we count total read chapters using our final api call
  - And we have got unread chapter counts from these two steps

With the same calls, detail list of unread chapters could also be made.

How many unread chapters I got you don't ask? Its 17783 T_T.

**NOTE: the refresh rate for personal token is 15 minutes, and we have total 0.6s of delay to not trip the rate limiter. So if you have over 800-900 manga in follows, a solution using segmentation of the calls over multiple API tokens is needed.**

**WARNING: I did my counting using different scripts for different parts and combined these scripts together. So yeah, I have yet to run _this_ script per se, but feel free to give it a try.**
