# Firecast Test Results

**Run at:** 2026-05-15 08:15:35 UTC  
**Score:** 3 / 5 passed

## Suite summary

| Case | Result |
|------|--------|
| `fire_distance` | PASS |
| `location_change` | FAIL |
| `budget_update` | PASS |
| `allergy_contradiction` | FAIL |
| `additive_control` | PASS |

---

## fire_distance — PASS

**Wildfire distance escalates from 5 miles to 2 miles**

| Field | Value |
|-------|-------|
| User ID | `firecast_fire_user` |
| Search query | 'How far is the fire from my house?' |
| Expect additive | False |
| Memories stored | 4 |
| Search hits | 4 |
| STALE in search | False |
| CURRENT in search | True |
| Step 1 `add()` events | ADD, ADD, ADD |
| Step 2 `add()` events | UPDATE, ADD, UPDATE |

### Markers in search

- **[CURRENT]** Wildfire is now only 2 miles from the house


### Verdict

> PASS (conditional): Only current fact returned in search.
> Check Step 2 — did Mem0 use UPDATE or only rank the newer embedding higher?
> WARNING: Both facts still stored; pass is fragile (ranking-dependent).

<details>
<summary>Raw Step 1 — initial add()</summary>

```json
{
  "results": [
    {
      "id": "cd48a98b-e3f0-4f73-b122-fcc0b0580416",
      "memory": "The wildfire is currently 5 miles away from the user's house",
      "event": "ADD"
    },
    {
      "id": "6c155cd1-0634-4f06-b7e6-7858bd9e1b68",
      "memory": "Winds are calm",
      "event": "ADD"
    },
    {
      "id": "bab1a8f7-2c8f-4475-95ed-b5c6a87d5f69",
      "memory": "Evacuation advisory is in effect",
      "event": "ADD"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 2 — update add()</summary>

```json
{
  "results": [
    {
      "id": "cd48a98b-e3f0-4f73-b122-fcc0b0580416",
      "memory": "Wildfire is now only 2 miles from the house",
      "event": "UPDATE",
      "previous_memory": "The wildfire is currently 5 miles away from the user's house"
    },
    {
      "id": "4681f3eb-a2a5-4801-8c28-1035426bf0e1",
      "memory": "Mandatory evacuation order issued",
      "event": "ADD"
    },
    {
      "id": "6c155cd1-0634-4f06-b7e6-7858bd9e1b68",
      "memory": "Winds have picked up",
      "event": "UPDATE",
      "previous_memory": "Winds are calm"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 3 — search results</summary>

```json
{
  "results": [
    {
      "id": "cd48a98b-e3f0-4f73-b122-fcc0b0580416",
      "memory": "Wildfire is now only 2 miles from the house",
      "hash": "fbc3689026507f32835759a5eb2159bf",
      "metadata": {
        "event": "fire_update",
        "ts": "T+30min",
        "distance_miles": 2
      },
      "score": 0.675216794013977,
      "created_at": "2026-05-15T08:15:04.230814+00:00",
      "updated_at": "2026-05-15T08:15:15.836099+00:00",
      "user_id": "firecast_fire_user"
    },
    {
      "id": "4681f3eb-a2a5-4801-8c28-1035426bf0e1",
      "memory": "Mandatory evacuation order issued",
      "hash": "8bea56d4f1d2d3baa97d88ad183480ad",
      "metadata": {
        "distance_miles": 2,
        "event": "fire_update",
        "ts": "T+30min"
      },
      "score": 1.5113928318023682,
      "created_at": "2026-05-15T08:15:15.844897+00:00",
      "updated_at": "2026-05-15T08:15:15.844897+00:00",
      "user_id": "firecast_fire_user"
    },
    {
      "id": "bab1a8f7-2c8f-4475-95ed-b5c6a87d5f69",
      "memory": "Evacuation advisory is in effect",
      "hash": "890b2aec56cab68f5b4bc97dc19a7c0f",
      "metadata": {
        "ts": "T+0",
        "event": "fire_update",
        "distance_miles": 5
      },
      "score": 1.575289011001587,
      "created_at": "2026-05-15T08:15:04.250083+00:00",
      "updated_at": "2026-05-15T08:15:04.250083+00:00",
      "user_id": "firecast_fire_user"
    },
    {
      "id": "6c155cd1-0634-4f06-b7e6-7858bd9e1b68",
      "memory": "Winds have picked up",
      "hash": "5556355324dcad2b9f48595c71b11b3e",
      "metadata": {
        "distance_miles": 2,
        "ts": "T+30min",
        "event": "fire_update"
      },
      "score": 1.6620136499404907,
      "created_at": "2026-05-15T08:15:04.246240+00:00",
      "updated_at": "2026-05-15T08:15:15.851564+00:00",
      "user_id": "firecast_fire_user"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 4 — all stored memories</summary>

```json
{
  "results": [
    {
      "id": "cd48a98b-e3f0-4f73-b122-fcc0b0580416",
      "memory": "Wildfire is now only 2 miles from the house",
      "hash": "fbc3689026507f32835759a5eb2159bf",
      "metadata": {
        "ts": "T+30min",
        "distance_miles": 2,
        "event": "fire_update"
      },
      "created_at": "2026-05-15T08:15:04.230814+00:00",
      "updated_at": "2026-05-15T08:15:15.836099+00:00",
      "user_id": "firecast_fire_user"
    },
    {
      "id": "6c155cd1-0634-4f06-b7e6-7858bd9e1b68",
      "memory": "Winds have picked up",
      "hash": "5556355324dcad2b9f48595c71b11b3e",
      "metadata": {
        "ts": "T+30min",
        "distance_miles": 2,
        "event": "fire_update"
      },
      "created_at": "2026-05-15T08:15:04.246240+00:00",
      "updated_at": "2026-05-15T08:15:15.851564+00:00",
      "user_id": "firecast_fire_user"
    },
    {
      "id": "bab1a8f7-2c8f-4475-95ed-b5c6a87d5f69",
      "memory": "Evacuation advisory is in effect",
      "hash": "890b2aec56cab68f5b4bc97dc19a7c0f",
      "metadata": {
        "ts": "T+0",
        "event": "fire_update",
        "distance_miles": 5
      },
      "created_at": "2026-05-15T08:15:04.250083+00:00",
      "updated_at": "2026-05-15T08:15:04.250083+00:00",
      "user_id": "firecast_fire_user"
    },
    {
      "id": "4681f3eb-a2a5-4801-8c28-1035426bf0e1",
      "memory": "Mandatory evacuation order issued",
      "hash": "8bea56d4f1d2d3baa97d88ad183480ad",
      "metadata": {
        "ts": "T+30min",
        "distance_miles": 2,
        "event": "fire_update"
      },
      "created_at": "2026-05-15T08:15:15.844897+00:00",
      "updated_at": "2026-05-15T08:15:15.844897+00:00",
      "user_id": "firecast_fire_user"
    }
  ]
}
```

</details>


## location_change — FAIL

**User relocates from Austin to Denver**

| Field | Value |
|-------|-------|
| User ID | `firecast_location_user` |
| Search query | 'Where do I live?' |
| Expect additive | False |
| Memories stored | 4 |
| Search hits | 4 |
| STALE in search | True |
| CURRENT in search | True |
| Step 1 `add()` events | ADD, ADD |
| Step 2 `add()` events | ADD, ADD |

### Markers in search

- **[STALE]** Lives in Austin, Texas
- **[CURRENT]** Moved to Denver, Colorado last month


### Verdict

> FAIL: Both stale and current facts returned. No conflict resolution.
> Mem0 treated this as additive, not superseding.

<details>
<summary>Raw Step 1 — initial add()</summary>

```json
{
  "results": [
    {
      "id": "09c7d8e5-5c72-4cf7-ad45-7de243b0aa25",
      "memory": "Lives in Austin, Texas",
      "event": "ADD"
    },
    {
      "id": "80e87b34-992c-4fe1-9026-ea583af09d75",
      "memory": "Works downtown",
      "event": "ADD"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 2 — update add()</summary>

```json
{
  "results": [
    {
      "id": "cbd6b884-0277-4919-95ed-e9c39e9e008e",
      "memory": "Moved to Denver, Colorado last month",
      "event": "ADD"
    },
    {
      "id": "aac48d5f-8c4f-4633-9085-5360fcd76425",
      "memory": "Loves the mountains",
      "event": "ADD"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 3 — search results</summary>

```json
{
  "results": [
    {
      "id": "09c7d8e5-5c72-4cf7-ad45-7de243b0aa25",
      "memory": "Lives in Austin, Texas",
      "hash": "4a4788e85514da046c7cb58443ba5ef3",
      "metadata": {
        "event": "location",
        "city": "Austin"
      },
      "score": 1.2085931301116943,
      "created_at": "2026-05-15T08:15:18.904344+00:00",
      "updated_at": "2026-05-15T08:15:18.904344+00:00",
      "user_id": "firecast_location_user"
    },
    {
      "id": "cbd6b884-0277-4919-95ed-e9c39e9e008e",
      "memory": "Moved to Denver, Colorado last month",
      "hash": "6f38b113df73f223fe5b1531f90d0330",
      "metadata": {
        "event": "location",
        "city": "Denver"
      },
      "score": 1.285175085067749,
      "created_at": "2026-05-15T08:15:21.193534+00:00",
      "updated_at": "2026-05-15T08:15:21.193534+00:00",
      "user_id": "firecast_location_user"
    },
    {
      "id": "80e87b34-992c-4fe1-9026-ea583af09d75",
      "memory": "Works downtown",
      "hash": "fa0e1b7565af2c2d44a471b1aff3474b",
      "metadata": {
        "city": "Austin",
        "event": "location"
      },
      "score": 1.4627997875213623,
      "created_at": "2026-05-15T08:15:18.913719+00:00",
      "updated_at": "2026-05-15T08:15:18.913719+00:00",
      "user_id": "firecast_location_user"
    },
    {
      "id": "aac48d5f-8c4f-4633-9085-5360fcd76425",
      "memory": "Loves the mountains",
      "hash": "16359c2e67924dc62b0eebc74147ac00",
      "metadata": {
        "event": "location",
        "city": "Denver"
      },
      "score": 1.5586256980895996,
      "created_at": "2026-05-15T08:15:21.197352+00:00",
      "updated_at": "2026-05-15T08:15:21.197352+00:00",
      "user_id": "firecast_location_user"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 4 — all stored memories</summary>

```json
{
  "results": [
    {
      "id": "09c7d8e5-5c72-4cf7-ad45-7de243b0aa25",
      "memory": "Lives in Austin, Texas",
      "hash": "4a4788e85514da046c7cb58443ba5ef3",
      "metadata": {
        "event": "location",
        "city": "Austin"
      },
      "created_at": "2026-05-15T08:15:18.904344+00:00",
      "updated_at": "2026-05-15T08:15:18.904344+00:00",
      "user_id": "firecast_location_user"
    },
    {
      "id": "80e87b34-992c-4fe1-9026-ea583af09d75",
      "memory": "Works downtown",
      "hash": "fa0e1b7565af2c2d44a471b1aff3474b",
      "metadata": {
        "city": "Austin",
        "event": "location"
      },
      "created_at": "2026-05-15T08:15:18.913719+00:00",
      "updated_at": "2026-05-15T08:15:18.913719+00:00",
      "user_id": "firecast_location_user"
    },
    {
      "id": "cbd6b884-0277-4919-95ed-e9c39e9e008e",
      "memory": "Moved to Denver, Colorado last month",
      "hash": "6f38b113df73f223fe5b1531f90d0330",
      "metadata": {
        "event": "location",
        "city": "Denver"
      },
      "created_at": "2026-05-15T08:15:21.193534+00:00",
      "updated_at": "2026-05-15T08:15:21.193534+00:00",
      "user_id": "firecast_location_user"
    },
    {
      "id": "aac48d5f-8c4f-4633-9085-5360fcd76425",
      "memory": "Loves the mountains",
      "hash": "16359c2e67924dc62b0eebc74147ac00",
      "metadata": {
        "city": "Denver",
        "event": "location"
      },
      "created_at": "2026-05-15T08:15:21.197352+00:00",
      "updated_at": "2026-05-15T08:15:21.197352+00:00",
      "user_id": "firecast_location_user"
    }
  ]
}
```

</details>


## budget_update — PASS

**Project budget increases from $10k to $50k**

| Field | Value |
|-------|-------|
| User ID | `firecast_budget_user` |
| Search query | 'What is my project budget?' |
| Expect additive | False |
| Memories stored | 1 |
| Search hits | 1 |
| STALE in search | False |
| CURRENT in search | True |
| Step 1 `add()` events | ADD |
| Step 2 `add()` events | UPDATE |

### Markers in search

- **[CURRENT]** Finance approved a revised project budget of $50,000 for this quarter


### Verdict

> PASS (conditional): Only current fact returned in search.
> Check Step 2 — did Mem0 use UPDATE or only rank the newer embedding higher?

<details>
<summary>Raw Step 1 — initial add()</summary>

```json
{
  "results": [
    {
      "id": "4d40e88f-9ef6-4760-9d19-06119537a8e4",
      "memory": "Project budget is $10,000 for this quarter",
      "event": "ADD"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 2 — update add()</summary>

```json
{
  "results": [
    {
      "id": "4d40e88f-9ef6-4760-9d19-06119537a8e4",
      "memory": "Finance approved a revised project budget of $50,000 for this quarter",
      "event": "UPDATE",
      "previous_memory": "Project budget is $10,000 for this quarter"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 3 — search results</summary>

```json
{
  "results": [
    {
      "id": "4d40e88f-9ef6-4760-9d19-06119537a8e4",
      "memory": "Finance approved a revised project budget of $50,000 for this quarter",
      "hash": "16200c95d11fa368fc961360564aa2ae",
      "metadata": {
        "event": "budget",
        "amount": 50000
      },
      "score": 0.9331811666488647,
      "created_at": "2026-05-15T08:15:23.234371+00:00",
      "updated_at": "2026-05-15T08:15:25.552122+00:00",
      "user_id": "firecast_budget_user"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 4 — all stored memories</summary>

```json
{
  "results": [
    {
      "id": "4d40e88f-9ef6-4760-9d19-06119537a8e4",
      "memory": "Finance approved a revised project budget of $50,000 for this quarter",
      "hash": "16200c95d11fa368fc961360564aa2ae",
      "metadata": {
        "event": "budget",
        "amount": 50000
      },
      "created_at": "2026-05-15T08:15:23.234371+00:00",
      "updated_at": "2026-05-15T08:15:25.552122+00:00",
      "user_id": "firecast_budget_user"
    }
  ]
}
```

</details>


## allergy_contradiction — FAIL

**Allergy to peanuts vs now eating peanut butter**

| Field | Value |
|-------|-------|
| User ID | `firecast_allergy_user` |
| Search query | 'Can I eat peanuts or peanut butter?' |
| Expect additive | False |
| Memories stored | 0 |
| Search hits | 0 |
| STALE in search | False |
| CURRENT in search | False |
| Step 1 `add()` events | ADD |
| Step 2 `add()` events | DELETE |

### Markers in search

_None matched in search results._


### Verdict

> INCONCLUSIVE: Neither fact clearly returned in search.

<details>
<summary>Raw Step 1 — initial add()</summary>

```json
{
  "results": [
    {
      "id": "12df7938-8ed5-4b9d-a1ba-e6862e63b5c5",
      "memory": "Allergic to peanuts and avoids all peanut products",
      "event": "ADD"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 2 — update add()</summary>

```json
{
  "results": [
    {
      "id": "12df7938-8ed5-4b9d-a1ba-e6862e63b5c5",
      "memory": "Allergic to peanuts and avoids all peanut products",
      "event": "DELETE"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 3 — search results</summary>

```json
{
  "results": []
}
```

</details>

<details>
<summary>Raw Step 4 — all stored memories</summary>

```json
{
  "results": []
}
```

</details>


## additive_control — PASS

**Non-conflicting preferences (hiking + coffee) should coexist**

| Field | Value |
|-------|-------|
| User ID | `firecast_additive_user` |
| Search query | 'What are my hobbies and interests?' |
| Expect additive | True |
| Memories stored | 2 |
| Search hits | 2 |
| FIRST in search | True |
| SECOND in search | True |
| Step 1 `add()` events | ADD |
| Step 2 `add()` events | ADD |

### Markers in search

- **[FIRST]** Loves hiking on weekends in the mountains
- **[SECOND]** Loves drinking coffee every morning


### Verdict

> PASS: Both non-conflicting facts returned and stored.
> Mem0 correctly kept additive memories separate.

<details>
<summary>Raw Step 1 — initial add()</summary>

```json
{
  "results": [
    {
      "id": "c9c9bfb6-175a-421a-ba35-ca139ff59404",
      "memory": "Loves hiking on weekends in the mountains",
      "event": "ADD"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 2 — update add()</summary>

```json
{
  "results": [
    {
      "id": "36246ce8-3645-436a-8d2d-c3ab163306c5",
      "memory": "Loves drinking coffee every morning",
      "event": "ADD"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 3 — search results</summary>

```json
{
  "results": [
    {
      "id": "c9c9bfb6-175a-421a-ba35-ca139ff59404",
      "memory": "Loves hiking on weekends in the mountains",
      "hash": "bb0079f53bfabf7289672854b5ac3648",
      "metadata": {
        "topic": "hiking",
        "event": "preference"
      },
      "score": 1.3711527585983276,
      "created_at": "2026-05-15T08:15:32.360725+00:00",
      "updated_at": "2026-05-15T08:15:32.360725+00:00",
      "user_id": "firecast_additive_user"
    },
    {
      "id": "36246ce8-3645-436a-8d2d-c3ab163306c5",
      "memory": "Loves drinking coffee every morning",
      "hash": "7d10327120f495de61dc0825377d6256",
      "metadata": {
        "event": "preference",
        "topic": "coffee"
      },
      "score": 1.5957244634628296,
      "created_at": "2026-05-15T08:15:34.662911+00:00",
      "updated_at": "2026-05-15T08:15:34.662911+00:00",
      "user_id": "firecast_additive_user"
    }
  ]
}
```

</details>

<details>
<summary>Raw Step 4 — all stored memories</summary>

```json
{
  "results": [
    {
      "id": "c9c9bfb6-175a-421a-ba35-ca139ff59404",
      "memory": "Loves hiking on weekends in the mountains",
      "hash": "bb0079f53bfabf7289672854b5ac3648",
      "metadata": {
        "topic": "hiking",
        "event": "preference"
      },
      "created_at": "2026-05-15T08:15:32.360725+00:00",
      "updated_at": "2026-05-15T08:15:32.360725+00:00",
      "user_id": "firecast_additive_user"
    },
    {
      "id": "36246ce8-3645-436a-8d2d-c3ab163306c5",
      "memory": "Loves drinking coffee every morning",
      "hash": "7d10327120f495de61dc0825377d6256",
      "metadata": {
        "topic": "coffee",
        "event": "preference"
      },
      "created_at": "2026-05-15T08:15:34.662911+00:00",
      "updated_at": "2026-05-15T08:15:34.662911+00:00",
      "user_id": "firecast_additive_user"
    }
  ]
}
```

</details>


