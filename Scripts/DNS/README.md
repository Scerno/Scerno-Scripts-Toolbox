# 123-reg zonefile creation

This historical script reads the records already visible in the legacy 123-reg Advanced DNS table and prints a zonefile-style listing. It makes no network requests and does not edit DNS. Current 123-reg compatibility has not been verified.

1. Open the Advanced DNS page for a domain you manage.
2. Read [the script](123-reg-zonefile-creation.js), then run it in your browser's developer console on that page.
3. Copy the output to a local file and review it against the provider's records. Check the origin, default TTL, and record formatting before attempting any import. The output includes visible records only.

Adapted from [zonefile-extract](https://github.com/Scerno/zonefile-extract) and its contributors. The script retains the [upstream Unlicense](123-reg-zonefile-creation.UNLICENSE).
