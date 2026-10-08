# Customer Journey Map

**Status:** English reconstruction of T1 pp. 17–18. The original map uses a persona and a broad hotel journey from booking to post-stay review. The following retains those stages but removes identifiable imagery and avoids pretending persona copy is a verbatim interview quote. Emotion descriptions are qualitative interpretations, not a measured curve.

| Dimension | Booking | Check-in | Stay / room | Service request | Check-out | Post-stay review |
| --- | --- | --- | --- | --- | --- | --- |
| Guest goal | Find suitable stay and understand services | Arrive and access room | Use facilities comfortably | Receive a clear, timely service | Settle account and depart | Share experience |
| Touchpoints in thesis | Hotel/booking platform | Reception | Room, Wi-Fi, restaurant, facilities | Room phone, reception, staff | Reception/payment | Review platform |
| Reported friction | Navigation and service information | Waiting and inconsistent staff information | Wi-Fi/service quality and limited comfort details | Delays, repeated requests, unclear fulfillment | Waiting and billing questions | Limited guest feedback loop |
| Interpreted experience | Uncertainty | Impatience | Expectations meet actual service | Frustration if request is lost | Desire for a smooth exit | Reflection on the whole stay |
| Opportunity in thesis | Clearer service information | Digital arrival/support processes | Training and facility/service improvements | Better service coordination and personalization | More consistent departure process | Structured feedback review |
| Current product scope | Out of scope | Self-reported room registration only | Structured service catalog | Intake, ownership, status/history, operational measurement | Out of scope | Per-request CSAT only |

## Focus journey: request a room service

Guest notices a need → opens Telegram → selects category/service → adds detail → receives a request ID → staff acknowledge/fulfill → guest checks status and rates after resolution. The detailed interaction is a reconstruction/new design, not the complete original hotel's live journey.

| Moment | Intended support | Failure condition | Evidence/validation |
| --- | --- | --- | --- |
| Choosing service | Plain catalog labels | Guest cannot classify need | Original catalog; future usability task |
| Submitting | Clear durable confirmation | False success or duplicate request | New transactional/idempotency tests |
| Waiting | Retrievable status | Status does not match actual staff action | New lookup; staff procedure needed |
| Fulfillment | Clear responsibility | Assignment fails across departments | Reconstructed workflow; role/assignment tests |
| Feedback | Simple 1–5 service rating | Old rating reused after reopening | New rating rules; unit/integration checks |

Priority is the request portion of the journey. The software does not address every cause of dissatisfaction in the broader thesis map.
